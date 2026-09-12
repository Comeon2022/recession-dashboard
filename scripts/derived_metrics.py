"""Canonical derived metrics shared by dashboard engines."""

from __future__ import annotations

import math


def derive_vix_metrics(observations: list[dict]) -> dict:
    """Use 20 valid observations for the average and a 20-observation change.

    Inputs are normalized, newest-first FRED observations. They are sorted
    ascending and missing/non-numeric values are discarded identically for all
    consumers. The change requires 21 valid observations: latest minus the
    observation exactly 20 valid observations earlier.
    """
    valid = []
    for item in observations:
        try:
            value = float(item["value"])
            date = str(item["date"])
        except (KeyError, TypeError, ValueError):
            continue
        if math.isfinite(value) and date:
            valid.append({"date": date, "value": value})
    ordered = sorted(valid, key=lambda item: item["date"])
    if len(ordered) < 21:
        raise ValueError("VIX requires at least 21 valid observations for 20D change")
    window = ordered[-21:]
    latest = window[-1]
    average20 = sum(item["value"] for item in window[-20:]) / 20
    change20 = latest["value"] - window[0]["value"]
    return {"current": latest["value"], "observation_date": latest["date"], "average20": average20, "change20": change20, "valid_observations": 21}
