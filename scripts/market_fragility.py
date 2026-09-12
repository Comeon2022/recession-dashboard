"""Derived market-fragility calculations. These never affect the recession score."""

from __future__ import annotations

from datetime import date, datetime


def _runs(values: list[tuple[str, float]], predicate) -> list[list[tuple[str, float]]]:
    runs, current = [], []
    for item in values:
        if predicate(item[1]):
            current.append(item)
        elif current:
            runs.append(current)
            current = []
    if current:
        runs.append(current)
    return runs


def _months_since(iso_date: str) -> int:
    start = datetime.strptime(iso_date, "%Y-%m-%d").date()
    today = date.today()
    return max(0, (today.year - start.year) * 12 + today.month - start.month)


def build_yield_curve_regime(series: dict[str, list[dict]]) -> dict:
    values = {key: {item["date"]: item["value"] for item in observations} for key, observations in series.items()}
    dates = sorted(set(values["DGS2"]) & set(values["DGS10"]) & set(values["T10Y2Y"]))
    spread_2s10s = [(d, values["T10Y2Y"][d]) for d in dates]
    spread_3m10y = [(d, values["T10Y3M"][d]) for d in sorted(values["T10Y3M"])]
    inverted_runs = [run for run in _runs(spread_2s10s, lambda value: value < 0) if len(run) >= 10]
    inversion = inverted_runs[-1] if inverted_runs else []
    inversion_start = inversion[0][0] if inversion else None
    uninversion_date = None
    if inversion:
        after = [(d, value) for d, value in spread_2s10s if d > inversion[-1][0]]
        positive_runs = [run for run in _runs(after, lambda value: value >= 0) if len(run) >= 10]
        if positive_runs:
            uninversion_date = positive_runs[0][0][0]
    current_spread = spread_2s10s[-1][1]
    phase = "currently_inverted" if current_spread < 0 else "positive_no_recent_inversion"
    months_since = None
    if uninversion_date:
        months_since = _months_since(uninversion_date)
        if months_since <= 18:
            phase = "recently_uninverted"

    trading_dates = sorted(set(values["DGS2"]) & set(values["DGS10"]) & set(values["T10Y2Y"])); steepening = "neutral_or_mixed"
    delta_2y = delta_10y = spread_change = None
    if len(trading_dates) >= 21:
        old, new = trading_dates[-21], trading_dates[-1]
        delta_2y = values["DGS2"][new] - values["DGS2"][old]
        delta_10y = values["DGS10"][new] - values["DGS10"][old]
        spread_change = values["T10Y2Y"][new] - values["T10Y2Y"][old]
        if spread_change >= 10 and delta_2y < 0 and delta_2y < delta_10y:
            steepening = "bull_steepening"
        elif spread_change >= 10 and delta_10y > 0 and delta_10y > delta_2y:
            steepening = "bear_steepening"
        elif spread_change <= -10:
            steepening = "flattening"

    return {
        "spread_2s10s_bp": round(current_spread * 100, 2),
        "spread_3m10y_bp": round(spread_3m10y[-1][1] * 100, 2) if spread_3m10y else None,
        "deepest_2s10s_inversion_bp": round(min((value for _, value in spread_2s10s), default=0) * 100, 2),
        "deepest_3m10y_inversion_bp": round(min((value for _, value in spread_3m10y), default=0) * 100, 2),
        "inversion_start_date": inversion_start,
        "uninversion_date": uninversion_date,
        "months_since_uninversion": months_since,
        "curve_phase": phase,
        "steepening_type": steepening,
        "delta_2y_20d_bp": round(delta_2y * 100, 2) if delta_2y is not None else None,
        "delta_10y_20d_bp": round(delta_10y * 100, 2) if delta_10y is not None else None,
        "spread_change_20d_bp": round(spread_change * 100, 2) if spread_change is not None else None,
        "treasury_yields": {key: values[key][sorted(values[key])[-1]] for key in ("DGS1", "DGS2", "DGS5", "DGS10", "DGS30")},
    }
