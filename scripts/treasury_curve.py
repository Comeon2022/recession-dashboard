"""Full Treasury constant-maturity curve context; never affects scoring."""
from __future__ import annotations

from datetime import datetime

TENORS = [
    ("1M", "DGS1MO"), ("3M", "DGS3MO"), ("6M", "DGS6MO"), ("1Y", "DGS1"),
    ("2Y", "DGS2"), ("3Y", "DGS3"), ("5Y", "DGS5"), ("7Y", "DGS7"),
    ("10Y", "DGS10"), ("20Y", "DGS20"), ("30Y", "DGS30"),
]
SPREADS = [("10Y_3M", "10Y - 3M", "10Y", "3M"), ("10Y_2Y", "10Y - 2Y", "10Y", "2Y"), ("30Y_5Y", "30Y - 5Y", "30Y", "5Y"), ("30Y_2Y", "30Y - 2Y", "30Y", "2Y"), ("30Y_10Y", "30Y - 10Y", "30Y", "10Y")]
WINDOWS = {"2020": ("2020-02-01", "2020-04-30"), "2008": ("2007-12-01", "2009-06-30"), "2001": ("2001-03-01", "2001-11-30")}

def _ordered(series):
    return sorted(({item["date"]: float(item["value"]) for item in series}).items())

def _nearest(items, target):
    eligible = [(date, value) for date, value in items if date <= target]
    return eligible[-1] if eligible else (None, None)

def _shape(values):
    short = values.get("3M"); belly = values.get("5Y"); long = values.get("30Y"); two = values.get("2Y"); ten = values.get("10Y")
    if any(value is None for value in (short, belly, long, two, ten)):
        return "mixed"
    if ten < short and long < belly:
        return "inverted"
    if abs(ten - short) < 0.10 and abs(long - belly) < 0.10:
        return "flat"
    if ten > short and long > belly and ten - short >= 1.00:
        return "steep"
    if ten > short and long >= belly:
        return "normal_upward"
    return "mixed"

def _movement(deltas):
    d2 = deltas.get("2Y", {}).get("20D"); d10 = deltas.get("10Y", {}).get("20D")
    d5 = deltas.get("5Y", {}).get("20D"); d30 = deltas.get("30Y", {}).get("20D")
    if None in (d2, d10, d5, d30): return "mixed"
    tolerance = 5.0  # basis points: movements this close are parallel
    primary = _movement_pair(d2, d10, tolerance)
    secondary = _movement_pair(d5, d30, tolerance)
    if primary.startswith("parallel_") and secondary.startswith("parallel_"):
        return primary if primary == secondary else "mixed"
    if primary == secondary:
        return primary
    return "mixed"

def _movement_pair(short, long, tolerance):
    if short > 0 and long > 0:
        return "parallel_up" if abs(short - long) <= tolerance else ("bear_steepening" if long > short else "bear_flattening")
    if short < 0 and long < 0:
        return "parallel_down" if abs(short - long) <= tolerance else ("bull_flattening" if long < short else "bull_steepening")
    return "mixed"

def build_treasury_curve(series):
    ordered = {series_id: _ordered(series.get(series_id, [])) for _, series_id in TENORS}
    latest = {label: (items[-1][1] if items else None) for label, series_id in TENORS for items in [ordered[series_id]]}
    dates = {label: (items[-1][0] if items else None) for label, series_id in TENORS for items in [ordered[series_id]]}
    curve = [{"label": label, "series_id": series_id, "yield": latest[label], "observation_date": dates[label]} for label, series_id in TENORS]
    valid_dates = [value for value in dates.values() if value]
    current_spreads = [{"id": key, "label": label, "percentage_points": round(latest[long] - latest[short], 4) if latest.get(long) is not None and latest.get(short) is not None else None, "basis_points": round((latest[long] - latest[short]) * 100, 2) if latest.get(long) is not None and latest.get(short) is not None else None} for key, label, long, short in SPREADS]
    deltas = {}
    for label, series_id in TENORS:
        items = ordered[series_id]; deltas[label] = {}
        for name, offset in (("1D", 1), ("5D", 5), ("20D", 20)):
            deltas[label][name] = round((items[-1][1] - items[-1-offset][1]) * 100, 2) if len(items) > offset else None
    historical = {}
    dgs2 = dict(ordered["DGS2"]); dgs10 = dict(ordered["DGS10"])
    spread_items = [(date, dgs10[date] - dgs2[date]) for date in sorted(set(dgs2) & set(dgs10))]
    for key, (start, end) in WINDOWS.items():
        candidates = [(date, value) for date, value in spread_items if start <= date <= end]
        representative = min(candidates, key=lambda item: item[1])[0] if candidates else None
        snapshot = [{"label": label, "series_id": series_id, "yield": _nearest(ordered[series_id], representative)[1], "observation_date": _nearest(ordered[series_id], representative)[0]} for label, series_id in TENORS] if representative else []
        historical[key] = {"representative_date": representative, "coverage": f"{sum(item['yield'] is not None for item in snapshot)}/{len(TENORS)}", "tenors": snapshot}
    return {"as_of": max(valid_dates) if valid_dates else None, "mixed_dates": len(set(valid_dates)) > 1, "tenors": curve, "spreads": current_spreads, "shape": _shape(latest), "shape_rule": "steep requires 10Y-3M >= 100 bp plus upward 30Y-5Y slope; otherwise positive upward curves are normal_upward", "dynamics": deltas, "movement": _movement(deltas), "movement_tolerance_bp": 5, "historical": historical}
