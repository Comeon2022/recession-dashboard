"""Context-only market inflation expectations around the latest CPI release."""
from __future__ import annotations

from datetime import datetime


SERIES = {"five_year_breakeven": "T5YIE", "five_year_forward": "T5YIFR"}
ONE_DAY_STATE_BP = 5.0


def _ordered(rows):
    return sorted((r for r in rows if r.get("value") is not None), key=lambda r: r["date"])


def _at_or_before(rows, target):
    eligible = [r for r in _ordered(rows) if r["date"] <= target]
    return eligible[-1] if eligible else None


def _changes(rows, target):
    ordered = _ordered(rows)
    index = next((i for i, row in enumerate(ordered) if row["date"] == target), None)
    current = _at_or_before(rows, target)
    if current is None:
        return None
    index = ordered.index(current)
    out = {"value": current["value"], "date": current["date"]}
    for label, offset in (("change_1d_bp", 1), ("change_5d_bp", 5), ("change_20d_bp", 20)):
        prior = ordered[index - offset] if index >= offset else None
        out[label] = round((current["value"] - prior["value"]) * 100, 3) if prior else None
    return out


def _direction(change):
    if change is None:
        return "Unavailable"
    if change >= ONE_DAY_STATE_BP:
        return "Expectations rising"
    if change <= -ONE_DAY_STATE_BP:
        return "Expectations falling"
    return "Stable"


def _expectation_state(primary_change, forward_change):
    primary = _direction(primary_change)
    if primary == "Unavailable":
        return primary
    opposite = ((primary == "Expectations rising" and forward_change is not None and forward_change <= -ONE_DAY_STATE_BP) or
                (primary == "Expectations falling" and forward_change is not None and forward_change >= ONE_DAY_STATE_BP))
    return "Mixed" if opposite else primary


def build_inflation_expectations(fetch, cpi_release):
    release_date = cpi_release.get("release_date") or cpi_release.get("headline", {}).get("date")
    if not release_date:
        return {"source": "FRED / Federal Reserve", "source_status": "unavailable", "state": "Unavailable", "release_date": None, "series": {}}
    series = {}
    warnings = []
    for name, series_id in SERIES.items():
        try:
            rows = fetch(series_id)
            metric = _changes(rows, release_date)
            if metric:
                series[name] = {"series_id": series_id, **metric, "release_day_marker": metric["date"] == release_date, "state": _direction(metric["change_1d_bp"]), "history": [{"date": r["date"], "value": r["value"]} for r in _ordered(rows)[-30:]]}
            else:
                warnings.append(f"{series_id}: no observation on or before CPI release date")
        except Exception as error:
            warnings.append(f"{series_id}: unavailable ({error.__class__.__name__})")
    primary = series.get("five_year_breakeven", {})
    forward = series.get("five_year_forward", {})
    primary_change, forward_change = primary.get("change_1d_bp"), forward.get("change_1d_bp")
    if primary_change is None:
        state = "Unavailable"
    else:
        state = _expectation_state(primary_change, forward_change)
    mom = cpi_release.get("headline", {}).get("mom")
    breadth = cpi_release.get("breadth", {})
    hotter = isinstance(mom, (int, float)) and mom >= 0.3 and breadth.get("rising_mom", 0) > breadth.get("eligible_components", 0) / 2
    if state == "Unavailable" or mom is None:
        divergence = "Mixed market signal"
    elif hotter and state == "Expectations rising":
        divergence = "Market concern broadening"
    elif hotter and state == "Expectations falling":
        divergence = "Market doubts persistence"
    elif not hotter and state == "Expectations falling":
        divergence = "Disinflation confirmation"
    elif not hotter and state == "Expectations rising":
        divergence = "Future pressure still priced"
    else:
        divergence = "Mixed market signal"
    return {"source": "FRED / Federal Reserve", "source_status": "live" if series else "unavailable", "release_date": release_date, "cpi_reference_month": release_date[:7], "state": state, "divergence": divergence, "cpi_context": {"headline_mom": mom, "headline_yoy": cpi_release.get("headline", {}).get("yoy"), "core_mom": cpi_release.get("core", {}).get("mom"), "breadth": breadth, "firm_broad": hotter}, "series": series, "methodology": "Breakevens are market-implied inflation pricing, not a pure forecast. 1D/5D/20D changes use valid observations, not calendar days. Project-defined primary threshold: 5Y 1D change >= +5 bp is rising, <= -5 bp is falling, otherwise stable. Mixed overrides the primary state only when the primary is threshold-qualified rising/falling and 5Y5Y moves at least 5 bp in the opposite direction. 5Y5Y remains a separate long-run persistence qualifier.", "two_year_series": {"status": "omitted", "reason": "No suitable approved official/public daily 2-year breakeven series identified; no proprietary screenshot or unsupported synthesis used."}, "warnings": warnings}
