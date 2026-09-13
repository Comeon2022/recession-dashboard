"""Deterministic recession-window comparisons for the dashboard's card metrics."""

from __future__ import annotations

from datetime import datetime
from typing import Any

WINDOWS = {
    "recession_2020": ("2020-02-01", "2020-04-30"),
    "recession_2008": ("2007-12-01", "2009-06-30"),
    "recession_2001": ("2001-03-01", "2001-11-30"),
}

SERIES = {
    "payrolls": ("PAYEMS", "monthly_change", "lower_is_worse"),
    "sahm-rule": ("UNRATE", "unemployment_rate", "higher_is_worse"),
    "initial-claims": ("ICSA", "claims_level", "higher_is_worse"),
    "jolts-hires": ("JTSHIR", "level", "lower_is_worse"),
    "jolts-quits": ("JTSQUR", "level", "lower_is_worse"),
    "wage-growth": ("CES0500000003", "yoy", "lower_is_worse"),
    "yield-curve": ("T10Y2Y", "spread", "custom_curve_stress"),
    "housing-starts": ("HOUST", "level", "lower_is_worse"),
    "building-permits": ("PERMIT", "level", "lower_is_worse"),
    "new-home-sales": ("HSN1F", "level", "lower_is_worse"),
    "mortgage-delinquency": ("DRSFRMACBS", "level", "higher_is_worse"),
    "months-supply": ("MSACSR", "level", "higher_is_worse"),
    "fhfa-home-prices": ("USSTHPI", "level", "lower_is_worse"),
    "mortgage-rate-30y": ("MORTGAGE30US", "level", "higher_is_worse"),
    "mortgage-debt-service": ("MDSP", "level", "higher_is_worse"),
    "vix": ("VIXCLS", "level", "higher_is_worse"),
    "financial-stress": ("STLFSI4", "level", "higher_is_worse"),
    "credit-conditions": ("NFCICREDIT", "level", "higher_is_worse"),
}

NA_REASONS = {
    "ism-employment": "N/A — manual/sample indicator; no approved historical source series",
    "ism-activity": "N/A — manual/sample indicator; no approved historical source series",
    "lei": "N/A — manual/sample indicator; no approved current historical source",
    "margin-debt-gdp": "N/A — quarterly FINRA context is not a meaningful recession-state comparator here",
    "public-equity-gdp": "N/A — valuation context is not a meaningful recession-state comparator",
    "shiller-cape": "N/A — valuation context is not a meaningful recession-state comparator",
    "berkshire-positioning": "N/A — filing-period positioning is not a recession-state comparator",
}


def _date(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%d")


def _yoy(observations: list[dict[str, Any]], index: int) -> float | None:
    current = observations[index]
    current_date = _date(current["date"])
    prior = next((item for item in observations[index + 1:] if (current_date - _date(item["date"])).days >= 330), None)
    if not prior or prior["value"] == 0:
        return None
    return (current["value"] / prior["value"] - 1) * 100


def _metric_observations(observations: list[dict[str, Any]], metric: str) -> list[dict[str, Any]]:
    chronological = list(reversed(observations))
    result = []
    for index, item in enumerate(chronological):
        value = item["value"]
        if metric == "monthly_change":
            if index == 0:
                continue
            value -= chronological[index - 1]["value"]
        elif metric == "yoy":
            value = _yoy(observations, len(observations) - 1 - index)
            if value is None:
                continue
        elif metric == "spread":
            value *= 100
        result.append({"date": item["date"], "value": value})
    return list(reversed(result))


def _format(indicator_id: str, value: float) -> str:
    if indicator_id == "payrolls":
        return f"{value:+,.0f}K"
    if indicator_id == "initial-claims":
        return f"{value:,.0f}"
    if indicator_id in {"sahm-rule", "wage-growth", "mortgage-delinquency", "mortgage-rate-30y", "mortgage-debt-service"}:
        return f"{value:.1f}%" if indicator_id != "sahm-rule" else f"{value:.1f}%"
    if indicator_id == "yield-curve":
        return f"{value:+.0f} bp"
    if indicator_id in {"housing-starts", "building-permits", "new-home-sales"}:
        return f"{value / 1000:.2f}M"
    if indicator_id in {"jolts-hires", "jolts-quits"}:
        return f"{value:.1f}%"
    if indicator_id in {"vix", "financial-stress", "credit-conditions"}:
        return f"{value:.2f}"
    if indicator_id == "fhfa-home-prices":
        return f"{value:.1f}"
    return f"{value:.2f}"


def build_historical_comparisons(indicators: list[dict[str, Any]], fetch_series, api_key: str) -> tuple[list[dict[str, Any]], list[str]]:
    """Return indicators with comparison objects and a coverage-audit warning list."""
    cache: dict[str, list[dict[str, Any]]] = {}
    warnings: list[str] = []
    for indicator in indicators:
        indicator_id = indicator["id"]
        if indicator_id not in SERIES:
            indicator["historical_comparison"] = {"method": "unavailable", "metric": "n/a", "direction": "n/a", "reason": NA_REASONS.get(indicator_id, "N/A — no approved historical source")}
            continue
        series_id, metric, direction = SERIES[indicator_id]
        try:
            cache.setdefault(series_id, fetch_series(series_id, api_key))
            values = _metric_observations(cache[series_id], metric)
            today_metric = values[0] if values else {"value": indicator["value"], "date": indicator["observation_date"]}
            comparison: dict[str, Any] = {"method": "recession_stress_extreme", "metric": metric, "direction": direction, "series_id": series_id, "history_start_date": values[-1]["date"] if values else None, "today": {"value": today_metric["value"], "date": today_metric["date"], "display": _format(indicator_id, today_metric["value"])} }
            for key, (start, end) in WINDOWS.items():
                window = [item for item in values if start <= item["date"] <= end]
                if not window:
                    comparison[key] = {"value": None, "date": None, "display": "N/A", "reason": f"N/A — {series_id} has no valid observations in the fixed window"}
                    continue
                if direction == "lower_is_worse":
                    selected = min(window, key=lambda item: item["value"])
                elif direction == "higher_is_worse":
                    selected = max(window, key=lambda item: item["value"])
                else:
                    selected = min(window, key=lambda item: item["value"])
                comparison[key] = {"value": selected["value"], "date": selected["date"], "display": _format(indicator_id, selected["value"])}
            indicator["historical_comparison"] = comparison
        except Exception as error:  # preserve dashboard generation if a historical request fails
            indicator["historical_comparison"] = {"method": "unavailable", "metric": metric, "direction": direction, "series_id": series_id, "reason": f"N/A — historical fetch failed for {series_id}"}
            warnings.append(f"{indicator_id}: historical comparison unavailable ({error.__class__.__name__})")
    return indicators, warnings


def coverage_markdown(indicators: list[dict[str, Any]]) -> str:
    lines = ["# Historical comparison coverage audit", "", "| Indicator | Metric | Source | History start | 2020 | 2008 | 2001 | Method / N/A reason |", "|---|---|---|---|---|---|---|---|"]
    for indicator in indicators:
        comparison = indicator.get("historical_comparison", {})
        cells = [comparison.get(key, {}).get("display", "N/A") if isinstance(comparison.get(key), dict) else "N/A" for key in WINDOWS]
        reason = comparison.get("reason", comparison.get("method", "unavailable"))
        lines.append(f"| {indicator['id']} | {comparison.get('metric', 'n/a')} | {comparison.get('series_id', 'see methodology')} | {comparison.get('history_start_date', 'n/a')} | {'yes' if cells[0] != 'N/A' else 'no'} | {'yes' if cells[1] != 'N/A' else 'no'} | {'yes' if cells[2] != 'N/A' else 'no'} | {reason} |")
    return "\n".join(lines) + "\n"
