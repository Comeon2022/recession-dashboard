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
from market_fragility import build_yield_curve_regime

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

    def attempt(indicator_id: str, loader) -> None:
        try:
            loader()
        except (OSError, ValueError, requests.RequestException) as error:
            warnings.append(f"{indicator_id}: FRED unavailable; sample value retained ({error})")

    if not api_key:
        return raw, [], ["FRED_API_KEY is not configured; sample values retained for all indicators."]

    def payrolls():
        value, date = latest_change("PAYEMS", api_key)
        update("payrolls", value * 1000, f"Monthly change {value:+,.0f}K (PAYEMS)", date, "monthly")

    def sahm():
        sahm = latest_observation("SAHMREALTIME", api_key)
        unemployment = latest_observation("UNRATE", api_key)
        validate_observation_date(unemployment["date"], "monthly")
        update("sahm-rule", sahm["value"], f"Unemployment {unemployment['value']:.1f}% | Sahm = {sahm['value']:+.2f}", sahm["date"], "monthly")

    def simple(indicator_id, series_id, formatter, frequency, multiplier=1):
        item = latest_observation(series_id, api_key)
        update(indicator_id, item["value"] * multiplier, formatter(item["value"] * multiplier), item["date"], frequency)

    def yoy(indicator_id, series_id, formatter, frequency="monthly"):
        value, date = latest_yoy(series_id, api_key)
        update(indicator_id, value, formatter(value), date, frequency)

    def jolts(indicator_id, series_id):
        item = latest_observation(series_id, api_key)
        update(indicator_id, item["value"], f"{item['value']:.1f}%", item["date"], "monthly")

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

    def curve_loader():
        curve_series = {series: fetch_fred_series(series, api_key) for series in ("DGS1", "DGS2", "DGS5", "DGS10", "DGS30", "T10Y2Y", "T10Y3M")}
        for observations in curve_series.values():
            validate_observation_date(observations[0]["date"], "daily")
        raw["_yield_curve_regime"] = build_yield_curve_regime(curve_series)
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

    attempt("payrolls", payrolls)
    attempt("sahm-rule", sahm)
    attempt("initial-claims", lambda: simple("initial-claims", "ICSA", lambda value: f"{value:,.0f}", "weekly"))
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
    attempt("vix", lambda: stress_window("vix", "VIXCLS", lambda value, average, change: f"{value:.2f} close | 20D avg {average:.2f} | 20D change {change:+.2f}"))
    attempt("financial-stress", lambda: stress_window("financial-stress", "STLFSI4", lambda value, average, change: f"{value:+.2f} | 4W avg {average:+.2f} | 12W change {change:+.2f}"))
    attempt("credit-conditions", lambda: stress_window("credit-conditions", "NFCICREDIT", lambda value, average, change: f"{value:+.2f} | 4W avg {average:+.2f} | 12W change {change:+.2f}"))
    attempt("margin-debt-gdp", margin_ratio)
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
        if indicator["id"] == "yield-curve" and "_yield_curve_regime" in raw:
            indicator["yield_curve_regime"] = raw["_yield_curve_regime"]
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
        "country": raw["country"], "total_score": total_score, "max_score": max_score,
        "risk_score": risk_score, "regime": get_regime_from_risk_score(risk_score),
        "summary": "Labor-market weakness is visible, while housing, credit, and market-fragility indicators add context to the cycle.",
        "yield_curve_regime": raw.get("_yield_curve_regime"),
        "categories": build_categories(indicators), "data_status": data_status, "warnings": warnings, "indicators": indicators,
    }


def update_history(current: dict) -> list[dict]:
    history = read_json(HISTORY_PATH, [])
    date = current["generated_at"][:10]
    history = [entry for entry in history if entry.get("date") != date]
    history.append({"date": date, "total_score": current["total_score"], "max_score": current["max_score"], "risk_score": current["risk_score"], "regime": current["regime"]})
    return sorted(history, key=lambda entry: entry["date"])


def main() -> None:
    load_dotenv()
    api_key = os.getenv("FRED_API_KEY", "")
    raw, live_ids, warnings = apply_fred_data(read_json(RAW_PATH, {}), api_key)
    status = "sample" if not api_key else ("ok" if not warnings else "partial")
    current = build_current(raw, status, warnings)
    write_json(DATA_PATH, current)
    write_json(HISTORY_PATH, update_history(current))
    shutil.copyfile(DATA_PATH, FRONTEND_DATA_PATH / "current.json")
    shutil.copyfile(HISTORY_PATH, FRONTEND_DATA_PATH / "history.json")
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
