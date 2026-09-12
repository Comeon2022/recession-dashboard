"""Valuation context helpers; these values never enter the recession score."""

from __future__ import annotations

import io
import re
from datetime import datetime

import pandas as pd
import requests

YALE_URLS = (
    "https://www.econ.yale.edu/~shiller/data/ie_data.xls",
    "http://www.econ.yale.edu/~shiller/data/ie_data.xls",
)


def historical_percentile(value: float, history: list[float]) -> float:
    """Return the weakly-inclusive percentile of value within a valid history."""
    values = sorted(float(item) for item in history if item is not None)
    if not values:
        raise ValueError("valuation history is empty")
    return round(sum(item <= value for item in values) / len(values) * 100, 1)


def percentile_label(percentile: float) -> str:
    if percentile > 97:
        return "Historically Extreme"
    if percentile >= 90:
        return "Extreme"
    if percentile >= 70:
        return "Elevated"
    return "Normal"


def build_public_equity_gdp_history(equity: list[dict], gdp: list[dict]) -> list[dict]:
    """Align Z.1 millions with nominal GDP billions and calculate percent."""
    gdp_by_date = {item["date"]: item["value"] for item in gdp}
    history = []
    for item in equity:
        denominator = gdp_by_date.get(item["date"])
        if denominator and denominator > 0:
            history.append({"date": item["date"], "value": item["value"] / 1000 / denominator * 100})
    return history


def _find_cape_column(frame: pd.DataFrame):
    for column in frame.columns:
        normalized = str(column).lower().replace(" ", "")
        if normalized in {"cape", "p/e10", "pe10", "p/e10ratio"} or "cape" in normalized:
            return column
    return None


def parse_yale_cape(content: bytes) -> list[dict]:
    """Parse the official Yale workbook, tolerating header/layout changes."""
    frames = pd.read_excel(io.BytesIO(content), sheet_name=None, header=None)
    candidates = []
    for frame in frames.values():
        for header_row in range(min(12, len(frame))):
            candidate = frame.iloc[header_row + 1 :].copy()
            candidate.columns = frame.iloc[header_row]
            cape_column = _find_cape_column(candidate)
            if cape_column is None:
                continue
            date_column = next((column for column in candidate.columns if "date" in str(column).lower()), candidate.columns[0])
            for _, row in candidate.iterrows():
                raw_date, raw_value = row.get(date_column), row.get(cape_column)
                try:
                    value = float(str(raw_value).replace(",", ""))
                    if isinstance(raw_date, (int, float)):
                        parsed = pd.Timestamp("1899-12-30") + pd.to_timedelta(float(raw_date), unit="D")
                    else:
                        parsed = pd.to_datetime(raw_date)
                    if 1 < value < 200 and not pd.isna(parsed) and parsed.year >= 1871:
                        candidates.append({"date": parsed.strftime("%Y-%m-%d"), "value": value})
                except (TypeError, ValueError):
                    continue
            if candidates:
                return sorted({item["date"]: item for item in candidates}.values(), key=lambda item: item["date"], reverse=True)
    raise ValueError("official Yale workbook did not contain a parseable CAPE column")


def fetch_yale_cape(timeout: int = 20) -> list[dict]:
    last_error = None
    for url in YALE_URLS:
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            parsed = parse_yale_cape(response.content)
            latest = datetime.strptime(parsed[0]["date"], "%Y-%m-%d")
            if latest.year < 2000 or parsed[0]["value"] < 5:
                raise ValueError("official Yale workbook produced an invalid CAPE date/value")
            return parsed
        except (requests.RequestException, ValueError, OSError, ImportError) as error:
            last_error = error
    raise ValueError(f"official Yale CAPE unavailable: {type(last_error).__name__}")


def cape_reference_month(date: str) -> str:
    return datetime.strptime(date, "%Y-%m-%d").strftime("%B %Y")
