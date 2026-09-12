"""Small FRED API client used by the local dashboard build."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

import requests

FRED_URL = "https://api.stlouisfed.org/fred/series/observations"

RECENCY_WINDOWS = {"daily": 14, "weekly": 45, "monthly": 120, "quarterly": 450}


def validate_observation_date(observation_date: str, frequency: str) -> None:
    """Reject only observations beyond a frequency-appropriate publication window."""
    age_days = (date.today() - datetime.strptime(observation_date, "%Y-%m-%d").date()).days
    if age_days > RECENCY_WINDOWS[frequency]:
        raise ValueError(f"observation {observation_date} is stale for {frequency} data ({age_days} days old)")


def fetch_fred_series(series_id: str, api_key: str, timeout: int = 15) -> list[dict[str, Any]]:
    """Return validated, newest-first FRED observations for one series."""
    if not api_key:
        raise ValueError("FRED_API_KEY is not configured")

    try:
        response = requests.get(
            FRED_URL,
            params={"series_id": series_id, "api_key": api_key, "file_type": "json", "sort_order": "desc"},
            timeout=timeout,
        )
        response.raise_for_status()
    except requests.RequestException as error:
        raise requests.RequestException(f"FRED request failed for {series_id}: {error.__class__.__name__}") from error
    payload = response.json()
    if payload.get("error_code") or "observations" not in payload:
        raise ValueError(payload.get("error_message", "FRED returned an invalid response"))

    observations = []
    for item in payload["observations"]:
        if item.get("value") in (None, ".", ""):
            continue
        try:
            observations.append({"date": item["date"], "value": float(item["value"])})
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(f"Invalid observation in FRED series {series_id}") from error
    if not observations:
        raise ValueError(f"FRED series {series_id} has no numeric observations")
    return observations


def latest_observation(series_id: str, api_key: str) -> dict[str, Any]:
    return fetch_fred_series(series_id, api_key)[0]


def latest_change(series_id: str, api_key: str) -> tuple[float, str]:
    """Return the latest monthly level change for a monthly level series."""
    observations = fetch_fred_series(series_id, api_key)
    if len(observations) < 2:
        raise ValueError(f"FRED series {series_id} lacks a prior observation")
    return observations[0]["value"] - observations[1]["value"], observations[0]["date"]


def latest_yoy(series_id: str, api_key: str) -> tuple[float, str]:
    """Calculate a 12-month percent change from the latest monthly observations."""
    observations = fetch_fred_series(series_id, api_key)
    latest = observations[0]
    latest_date = datetime.strptime(latest["date"], "%Y-%m-%d")
    prior = next(
        (item for item in observations[1:] if (latest_date - datetime.strptime(item["date"], "%Y-%m-%d")).days >= 330),
        None,
    )
    if prior is None or prior["value"] == 0:
        raise ValueError(f"FRED series {series_id} lacks a usable 12-month comparison")
    return ((latest["value"] / prior["value"]) - 1) * 100, latest["date"]
