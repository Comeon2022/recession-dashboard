"""Build normalized dashboard JSON from sample data with optional FRED overlays."""

import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

import requests

from calculate_scores import SCORERS, get_regime_from_risk_score
from fetch_fred import fetch_fred_series, latest_change, latest_observation, latest_yoy, validate_observation_date
from fetch_finra import fetch_margin_debt
from fetch_berkshire import fetch_berkshire_report
from market_fragility import build_yield_curve_regime
from treasury_curve import TENORS, build_treasury_curve
from current_stress import build_current_stress
from derived_metrics import derive_claims_metrics, derive_jolts_metrics, derive_payroll_metrics, derive_vix_metrics, derive_wage_metrics
from valuation import cape_reference_month, fetch_yale_cape, historical_percentile, percentile_label, build_public_equity_gdp_history
from historical_comparisons import build_historical_comparisons, coverage_markdown
from cpi_analyzer import build_cpi_release
from wage_inflation import build_wage_inflation

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = lambda: None

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "sample_raw.json"
DATA_PATH = ROOT / "data" / "current.json"
HISTORY_PATH = ROOT / "data" / "history.json"
FRONTEND_DATA_PATH = ROOT / "frontend" / "src" / "data"


def read_json(path: Path, default):
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)
        file.write("\n")


def apply_fred_data(raw: dict, api_key: str) -> tuple[dict, list[str], list[str]]:
    """Overlay approved FRED series; preserve each sample value when a request fails."""
    live, warnings = [], []
    by_id = {indicator["id"]: indicator for indicator in raw["indicators"]}

    def update(indicator_id: str, value: float, display_value: str, date: str, frequency: str) -> None:
        validate_observation_date(date, frequency)
        by_id[indicator_id].update({"value": value, "display_value": display_value, "source": "FRED", "observation_date": date})
        live.append(indicator_id)

    def attempt(indicator_id: str, loader, source_name: str = "FRED") -> None:
        try:
            loader()
        except (OSError, ValueError, requests.RequestException) as error:
            if indicator_id in by_id:
                by_id[indicator_id]["source_status"] = "fallback"
            if indicator_id == "berkshire-positioning":
                raw.setdefault("berkshire_positioning", {})["source_status"] = "fallback"
            warnings.append(f"{indicator_id}: {source_name} unavailable; sample value retained ({error})")

    if not api_key:
        return raw, [], ["FRED_API_KEY is not configured; sample values retained for all indicators."]

    def payrolls():
        metrics = derive_payroll_metrics(fetch_fred_series("PAYEMS", api_key))
        value = metrics["latest_monthly_change"]
        update("payrolls", value * 1000, f"Monthly change {value:+,.0f}K (PAYEMS)", metrics["observation_date"], "monthly")
        by_id["payrolls"]["trend_metrics"] = {"Latest monthly change": f"{value:+,.0f}K", "3M average change": f"{metrics['three_month_average_monthly_change']:+,.0f}K", "12M average change": f"{metrics['twelve_month_average_monthly_change']:+,.0f}K", "Payroll level": f"{metrics['level']:,.0f}K"}

    def sahm():
        sahm = latest_observation("SAHMREALTIME", api_key)
        unemployment = latest_observation("UNRATE", api_key)
        unemployment_series = fetch_fred_series("UNRATE", api_key)
        latest_date = datetime.strptime(unemployment["date"], "%Y-%m-%d")
        prior_year = next((item for item in unemployment_series[1:] if (latest_date - datetime.strptime(item["date"], "%Y-%m-%d")).days >= 330), None)
        validate_observation_date(unemployment["date"], "monthly")
        update("sahm-rule", sahm["value"], f"Unemployment {unemployment['value']:.1f}% | Sahm = {sahm['value']:+.2f}", sahm["date"], "monthly")
        by_id["sahm-rule"]["trend_metrics"] = {"Unemployment rate": f"{unemployment['value']:.1f}%", "3M average unemployment": f"{sum(item['value'] for item in unemployment_series[:3]) / 3:.1f}%", "12M change": f"{unemployment['value'] - prior_year['value']:+.1f} pp" if prior_year else "n/a", "Sahm threshold reference": "0.50"}

    def simple(indicator_id, series_id, formatter, frequency, multiplier=1):
        item = latest_observation(series_id, api_key)
        update(indicator_id, item["value"] * multiplier, formatter(item["value"] * multiplier), item["date"], frequency)

    def claims():
        metrics = derive_claims_metrics(fetch_fred_series("ICSA", api_key))
        update("initial-claims", metrics["latest_claims"], f"{metrics['latest_claims']:,.0f}", metrics["observation_date"], "weekly")
        by_id["initial-claims"]["trend_metrics"] = {"Latest claims": f"{metrics['latest_claims']:,.0f}", "4-week average": f"{metrics['four_week_average']:,.0f}", "4-week avg 13 weeks ago": f"{metrics['four_week_average_13_weeks_ago']:,.0f}", "13-week change": f"{metrics['thirteen_week_change_pct']:+.1f}%"}

    def yoy(indicator_id, series_id, formatter, frequency="monthly"):
        metrics = derive_wage_metrics(fetch_fred_series(series_id, api_key))
        update(indicator_id, metrics["latest_yoy"], formatter(metrics["latest_yoy"]), metrics["observation_date"], frequency)
        by_id[indicator_id]["trend_metrics"] = {"Latest YoY": f"{metrics['latest_yoy']:+.1f}%", "3M average YoY": f"{metrics['three_month_average_yoy']:+.1f}%", "12M change in growth rate": f"{metrics['twelve_month_change_pp']:+.1f} pp"}

    def jolts(indicator_id, series_id):
        metrics = derive_jolts_metrics(fetch_fred_series(series_id, api_key))
        update(indicator_id, metrics["latest"], f"{metrics['latest']:.1f}%", metrics["observation_date"], "monthly")
        by_id[indicator_id]["trend_metrics"] = {"Latest": f"{metrics['latest']:.1f}%", "3M average": f"{metrics['three_month_average']:.1f}%", "12M average": f"{metrics['twelve_month_average']:.1f}%", "Trend": metrics["trend"]}

    def window_stats(indicator_id, series_id, formatter, frequency, window=20):
        observations = fetch_fred_series(series_id, api_key)
        validate_observation_date(observations[0]["date"], frequency)
        values = [item["value"] for item in observations[:window]]
        average = sum(values) / len(values)
        change = values[0] - values[-1] if len(values) > 1 else 0
        update(indicator_id, values[0], formatter(values[0], average, change), observations[0]["date"], frequency)

    def stress_window(indicator_id, series_id, formatter):
        observations = fetch_fred_series(series_id, api_key)
        validate_observation_date(observations[0]["date"], "weekly")
        values = [item["value"] for item in observations[:12]]
        average = sum(values[:4]) / min(4, len(values))
        change = values[0] - values[-1] if len(values) > 1 else 0
        update(indicator_id, values[0], formatter(values[0], average, change), observations[0]["date"], "weekly")

    def vix_window():
        metrics = derive_vix_metrics(fetch_fred_series("VIXCLS", api_key))
        update("vix", metrics["current"], f"{metrics['current']:.2f} close | 20D avg {metrics['average20']:.2f} | 20D change {metrics['change20']:+.2f}", metrics["observation_date"], "daily")
        raw["_vix_metrics"] = metrics

    def curve_loader():
        curve_series = {series: fetch_fred_series(series, api_key) for series in ("DGS1MO", "DGS3MO", "DGS6MO", "DGS1", "DGS2", "DGS3", "DGS5", "DGS7", "DGS10", "DGS20", "DGS30", "T10Y2Y", "T10Y3M")}
        for observations in curve_series.values():
            validate_observation_date(observations[0]["date"], "daily")
        raw["_yield_curve_regime"] = build_yield_curve_regime(curve_series)
        raw["_treasury_curve"] = build_treasury_curve(curve_series)
        curve = by_id["yield-curve"]
        curve["yield_curve_regime"] = raw["_yield_curve_regime"]
        curve["display_value"] = f"{curve['display_value']} · {raw['_yield_curve_regime']['curve_phase']} / {raw['_yield_curve_regime']['steepening_type']}"

    def margin_ratio():
        finra = fetch_margin_debt()
        gdp = latest_observation("GDP", api_key)
        margin_billions = finra["debit_balance_millions"] / 1000
        ratio = margin_billions / gdp["value"] * 100
        update("margin-debt-gdp", ratio, f"{ratio:.2f}% of GDP | ${finra['debit_balance_millions']:,.0f}M margin debt", gdp["date"], "quarterly")
        by_id["margin-debt-gdp"].update({"source": "FINRA + FRED", "source_reference_month": finra["reference_month"], "gdp_observation_date": gdp["date"]})

    def current_stress_loader():
        vix = fetch_fred_series("VIXCLS", api_key)
        financial = fetch_fred_series("STLFSI4", api_key)
        credit = fetch_fred_series("NFCICREDIT", api_key)
        claims = fetch_fred_series("ICSA", api_key)
        sahm = latest_observation("SAHMREALTIME", api_key)
        unemployment = latest_observation("UNRATE", api_key)
        curve = raw.get("_yield_curve_regime")
        if not curve:
            raise ValueError("yield curve regime unavailable for Current Stress")
        raw["_current_stress"] = build_current_stress(vix, financial, credit, claims, sahm, unemployment, curve, raw.get("_vix_metrics"), derive_claims_metrics(claims))

    def berkshire_loader():
        raw["_berkshire_positioning"] = fetch_berkshire_report()

    def public_equity_gdp():
        equity = fetch_fred_series("BOGZ1FL883164115Q", api_key)
        gdp = fetch_fred_series("GDP", api_key)
        validate_observation_date(equity[0]["date"], "quarterly")
        validate_observation_date(gdp[0]["date"], "quarterly")
        history = build_public_equity_gdp_history(equity, gdp)
        if not history:
            raise ValueError("Z.1 public equities and GDP have no aligned observations")
        latest = history[0]
        percentile = historical_percentile(latest["value"], [item["value"] for item in history])
        update("public-equity-gdp", latest["value"], f"{latest['value']:.1f}% of GDP | {percentile:.0f}th percentile", latest["date"], "quarterly")
        by_id["public-equity-gdp"].update({
            "source": "Federal Reserve Z.1 + FRED GDP",
            "methodology": "BOGZ1FL883164115Q public corporate equities in millions divided by nominal GDP in billions after converting equities to billions",
            "equity_observation_date": latest["date"], "gdp_observation_date": latest["date"],
            "historical_percentile": percentile, "percentile_label": percentile_label(percentile),
        })

    def shiller_cape():
        history = fetch_yale_cape()
        latest = history[0]
        percentile = historical_percentile(latest["value"], [item["value"] for item in history])
        median = round(sorted(item["value"] for item in history)[len(history) // 2], 1)
        update("shiller-cape", latest["value"], f"{latest['value']:.1f} | {percentile:.0f}th percentile | median {median:.1f}", latest["date"], "monthly")
        by_id["shiller-cape"].update({
            "source": "Robert Shiller / Yale",
            "source_status": "live",
            "methodology": "Cyclically adjusted price/earnings ratio from the official Yale Shiller data workbook",
            "reference_month": cape_reference_month(latest["date"]), "historical_percentile": percentile,
            "percentile_label": percentile_label(percentile), "long_run_median": median,
        })

    attempt("payrolls", payrolls)
    attempt("sahm-rule", sahm)
    attempt("initial-claims", claims)
    attempt("jolts-hires", lambda: jolts("jolts-hires", "JTSHIR"))
    attempt("jolts-quits", lambda: jolts("jolts-quits", "JTSQUR"))
    attempt("wage-growth", lambda: yoy("wage-growth", "CES0500000003", lambda value: f"{value:+.1f}% YoY"))
    attempt("yield-curve", lambda: simple("yield-curve", "T10Y2Y", lambda value: f"{value:+.0f} bp", "daily", multiplier=100))
    attempt("yield-curve-regime", curve_loader)
    attempt("housing-starts", lambda: simple("housing-starts", "HOUST", lambda value: f"{value:.2f}M annualized", "monthly", multiplier=1 / 1000))
    attempt("building-permits", lambda: simple("building-permits", "PERMIT", lambda value: f"{value:.2f}M annualized", "monthly", multiplier=1 / 1000))
    attempt("new-home-sales", lambda: simple("new-home-sales", "HSN1F", lambda value: f"{value:.2f}M annualized", "monthly", multiplier=1 / 1000))
    attempt("months-supply", lambda: simple("months-supply", "MSACSR", lambda value: f"{value:.1f} months", "monthly"))
    attempt("fhfa-home-prices", lambda: simple("fhfa-home-prices", "USSTHPI", lambda value: f"Index {value:.1f}", "quarterly"))
    attempt("mortgage-rate-30y", lambda: simple("mortgage-rate-30y", "MORTGAGE30US", lambda value: f"{value:.2f}%", "weekly"))
    attempt("mortgage-delinquency", lambda: simple("mortgage-delinquency", "DRSFRMACBS", lambda value: f"{value:.2f}%", "quarterly"))
    attempt("mortgage-debt-service", lambda: simple("mortgage-debt-service", "MDSP", lambda value: f"{value:.2f}% of disposable income", "quarterly"))
    attempt("vix", vix_window)
    attempt("financial-stress", lambda: stress_window("financial-stress", "STLFSI4", lambda value, average, change: f"{value:+.2f} | 4W avg {average:+.2f} | 12W change {change:+.2f}"))
    attempt("credit-conditions", lambda: stress_window("credit-conditions", "NFCICREDIT", lambda value, average, change: f"{value:+.2f} | 4W avg {average:+.2f} | 12W change {change:+.2f}"))
    attempt("margin-debt-gdp", margin_ratio)
    attempt("public-equity-gdp", public_equity_gdp)
    attempt("shiller-cape", shiller_cape, "official Yale")
    attempt("current-stress", current_stress_loader)
    attempt("berkshire-positioning", berkshire_loader, "Berkshire official filing")
    # LEI intentionally remains manual/sample. USSLIND is not used.
    return raw, live, warnings


def build_categories(indicators: list[dict]) -> list[dict]:
    categories = {}
    for indicator in indicators:
        category_id = indicator["category"].lower().replace(" / ", "-").replace(" ", "-")
        bucket = categories.setdefault(category_id, {"id": category_id, "name": indicator["category"], "score": 0, "max_score": 0})
        if indicator["scored"]:
            bucket["score"] += indicator["score"]
            bucket["max_score"] += 2
    for category in categories.values():
        category["risk_score"] = round(category["score"] / category["max_score"] * 100) if category["max_score"] else None
        category["regime"] = get_regime_from_risk_score(category["risk_score"]) if category["risk_score"] is not None else "Context"
    return list(categories.values())


def build_current(raw: dict, data_status: str, warnings: list[str]) -> dict:
    indicators = []
    for raw_indicator in raw["indicators"]:
        indicator = dict(raw_indicator)
        if indicator["id"] in {"sahm-rule", "jolts-quits"}:
            indicator["scored"] = False
        if indicator["id"] == "yield-curve" and "_yield_curve_regime" in raw:
            indicator["yield_curve_regime"] = raw["_yield_curve_regime"]
            indicator["treasury_curve"] = raw.get("_treasury_curve")
        indicator.setdefault("scored", True)
        if indicator["scored"]:
            try:
                indicator["score"] = SCORERS[indicator["id"]](indicator["value"])
            except KeyError as error:
                raise ValueError(f"No scoring function configured for {indicator['id']}") from error
            indicator["risk_score"] = round(indicator["score"] / 2 * 100)
        else:
            indicator["score"] = None
            indicator["risk_score"] = None
        indicators.append(indicator)

    scored = [indicator for indicator in indicators if indicator["scored"]]
    total_score = sum(indicator["score"] for indicator in scored)
    max_score = len(scored) * 2
    risk_score = round(total_score / max_score * 100) if max_score else 0
    return {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "score_model_version": 2,
        "country": raw["country"], "total_score": total_score, "max_score": max_score,
        "risk_score": risk_score, "regime": get_regime_from_risk_score(risk_score),
        "summary": "Labor-market weakness is visible, while housing, credit, and market-fragility indicators add context to the cycle.",
        "yield_curve_regime": raw.get("_yield_curve_regime"),
        "treasury_curve": raw.get("_treasury_curve"),
        "current_stress": raw.get("_current_stress"),
        "berkshire_positioning": raw.get("_berkshire_positioning", raw.get("berkshire_positioning")),
        "categories": build_categories(indicators), "data_status": data_status, "warnings": warnings, "indicators": indicators,
    }


def update_history(current: dict, warnings: list[str] | None = None) -> list[dict]:
    history = read_json(HISTORY_PATH, [])
    date = current["generated_at"][:10]
    current_version = current.get("score_model_version", 1)
    replacement = {"date": date, "total_score": current["total_score"], "max_score": current["max_score"], "risk_score": current["risk_score"], "regime": current["regime"], "score_model_version": current_version}
    existing_index = next((index for index, entry in enumerate(history) if entry.get("date") == date), None)
    if existing_index is None:
        history.append(replacement)
    else:
        existing_version = history[existing_index].get("score_model_version", 1)
        if existing_version == current_version:
            history[existing_index] = replacement
        elif warnings is not None:
            warnings.append(f"history: same-date score model version conflict for {date} (existing v{existing_version}, current v{current_version}); existing row preserved")
    return sorted(history, key=lambda entry: entry["date"])


def main() -> None:
    load_dotenv()
    api_key = os.getenv("FRED_API_KEY", "")
    raw, live_ids, warnings = apply_fred_data(read_json(RAW_PATH, {}), api_key)
    status = "sample" if not api_key else ("ok" if not warnings else "partial")
    current = build_current(raw, status, warnings)
    try:
        current["inflation_release"] = build_cpi_release()
    except (OSError, ValueError, requests.RequestException) as error:
        warnings.append(f"inflation-release: BLS CPI analyzer unavailable ({error.__class__.__name__})")
        current["inflation_release"] = {"source": "BLS", "source_status": "fallback", "warnings": ["CPI release analyzer unavailable; no CPI context generated."]}
    try:
        ahe_rows = fetch_fred_series("CES0500000003", api_key)
        current["wage_inflation"] = build_wage_inflation(lambda series_id: fetch_fred_series(series_id, api_key), ahe_rows, current.get("inflation_release", {}).get("headline", {}))
    except (OSError, ValueError, requests.RequestException) as error:
        warnings.append(f"wage-inflation: FRED transmission context unavailable ({error.__class__.__name__})")
        current["wage_inflation"] = {"source": "FRED / BLS", "source_status": "fallback", "state": "Mixed", "warnings": ["Wage/inflation transmission context unavailable; existing wage indicator unchanged."]}
    current["indicators"], comparison_warnings = build_historical_comparisons(current["indicators"], fetch_fred_series, api_key)
    warnings.extend(comparison_warnings)
    current["warnings"] = warnings
    current["data_status"] = status if not comparison_warnings else "partial"
    current["historical_comparison_methodology"] = {
        "method": "recession_stress_extreme",
        "windows": {key: {"start": start, "end": end} for key, (start, end) in __import__("historical_comparisons").WINDOWS.items()},
        "note": "Each card compares its displayed primary metric with the most stressed observation in the fixed window; unavailable values remain N/A.",
    }
    write_json(DATA_PATH, current)
    write_json(HISTORY_PATH, update_history(current, warnings))
    shutil.copyfile(DATA_PATH, FRONTEND_DATA_PATH / "current.json")
    shutil.copyfile(HISTORY_PATH, FRONTEND_DATA_PATH / "history.json")
    (ROOT / "research" / "historical_comparison_coverage.md").write_text(coverage_markdown(current["indicators"]), encoding="utf-8")
    for indicator in current["indicators"]:
        print(f"{indicator['name']}: {indicator['score'] if indicator['scored'] else 'context'}")
    print(f"Total Score: {current['total_score']} / {current['max_score']}")
    print(f"Risk Score: {current['risk_score']} / 100")
    print(f"Regime: {current['regime']}")
    print("current.json updated\nhistory.json updated\nfrontend/src/data synchronized")
    print(f"Live FRED indicators: {len(live_ids)}")
    print(f"Manual/sample indicators: {len(current['indicators']) - len(live_ids)}")
    for warning in warnings:
        print(f"Warning: {warning}")


if __name__ == "__main__":
    main()
