"""Canonical derived metrics shared by dashboard engines."""

from __future__ import annotations

import math


def _valid_newest_first(observations: list[dict]) -> list[dict]:
    valid = []
    for item in observations:
        try:
            value = float(item["value"])
            date = str(item["date"])
        except (KeyError, TypeError, ValueError):
            continue
        if math.isfinite(value) and date:
            valid.append({"date": date, "value": value})
    return sorted(valid, key=lambda item: item["date"], reverse=True)


def _average_monthly_changes(observations: list[dict], periods: int) -> float:
    ordered = _valid_newest_first(observations)
    changes = [ordered[index]["value"] - ordered[index + 1]["value"] for index in range(len(ordered) - 1)]
    if len(changes) < periods:
        raise ValueError(f"series requires {periods + 1} valid observations")
    return sum(changes[:periods]) / periods


def derive_payroll_metrics(observations: list[dict]) -> dict:
    ordered = _valid_newest_first(observations)
    if len(ordered) < 13:
        raise ValueError("PAYEMS requires 13 valid observations")
    return {"latest_monthly_change": ordered[0]["value"] - ordered[1]["value"],
            "three_month_average_monthly_change": _average_monthly_changes(ordered, 3),
            "twelve_month_average_monthly_change": _average_monthly_changes(ordered, 12),
            "level": ordered[0]["value"], "observation_date": ordered[0]["date"]}


def derive_claims_metrics(observations: list[dict]) -> dict:
    ordered = _valid_newest_first(observations)
    if len(ordered) < 17:
        raise ValueError("ICSA requires 17 valid observations")
    current = sum(item["value"] for item in ordered[:4]) / 4
    prior = sum(item["value"] for item in ordered[13:17]) / 4
    change = (current / prior - 1) * 100 if prior else 0.0
    return {"latest_claims": ordered[0]["value"], "four_week_average": current,
            "four_week_average_13_weeks_ago": prior, "thirteen_week_change_pct": change,
            "observation_date": ordered[0]["date"]}


def derive_jolts_metrics(observations: list[dict]) -> dict:
    ordered = _valid_newest_first(observations)
    if len(ordered) < 12:
        raise ValueError("JOLTS requires 12 valid observations")
    latest = ordered[0]["value"]
    avg3 = sum(item["value"] for item in ordered[:3]) / 3
    avg12 = sum(item["value"] for item in ordered[:12]) / 12
    trend = "accelerating" if avg3 > avg12 * 1.01 else "decelerating" if avg3 < avg12 * 0.99 else "stable"
    return {"latest": latest, "three_month_average": avg3, "twelve_month_average": avg12,
            "trend": trend, "observation_date": ordered[0]["date"]}


def derive_wage_metrics(observations: list[dict]) -> dict:
    ordered = _valid_newest_first(observations)
    if len(ordered) < 24:
        raise ValueError("wage series requires 24 valid observations")
    yoy = []
    for index in range(len(ordered) - 12):
        prior = ordered[index + 12]["value"]
        if prior:
            yoy.append((ordered[index]["value"] / prior - 1) * 100)
    if len(yoy) < 12:
        raise ValueError("wage series lacks enough YoY observations")
    return {"latest_yoy": yoy[0], "three_month_average_yoy": sum(yoy[:3]) / 3,
            "twelve_month_change_pp": yoy[0] - yoy[12 - 1], "observation_date": ordered[0]["date"]}


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
