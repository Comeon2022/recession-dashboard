"""Fetch and defensively parse Berkshire Hathaway's official quarterly report."""

from __future__ import annotations

import re
from io import BytesIO

import requests
from pypdf import PdfReader

BERKSHIRE_Q2_2026_URL = "https://www.berkshirehathaway.com/qtrly/2ndqtr26.pdf"


def _amount(text: str) -> float:
    value = float(text.replace(",", "").replace("(", "").replace(")", ""))
    return -value if "(" in text else value


def _row_value(text: str, label: str, occurrence: int = 0) -> float:
    pattern = re.compile(rf"{re.escape(label)}[^\n]*?(\(?[\d,]+\)?)")
    matches = pattern.findall(text)
    if len(matches) <= occurrence:
        raise ValueError(f"Berkshire row not found: {label}")
    return _amount(matches[occurrence])


def parse_berkshire_report(pdf_bytes: bytes, source_url: str = BERKSHIRE_Q2_2026_URL) -> dict:
    text = "\n".join(page.extract_text() or "" for page in PdfReader(BytesIO(pdf_bytes)).pages)
    if "June 30, 2026" not in text:
        raise ValueError("Berkshire report period was not found")
    insurance_cash = _row_value(text, "Cash and cash equivalents*", 0)
    treasury_bills = _row_value(text, "Short-term investments in U.S. Treasury Bills**", 0)
    railroad_cash = _row_value(text, "Cash and cash equivalents*", 1)
    total_assets = _row_value(text, "Total assets", 0)
    purchases = abs(_row_value(text, "Purchases of equity securities", 0))
    sales = _row_value(text, "Sales of equity securities", 0)
    values = [insurance_cash, treasury_bills, railroad_cash, total_assets, purchases, sales]
    if not all(0 < value < 2_000_000 for value in values) or total_assets < 500_000:
        raise ValueError("Berkshire parsed values failed plausibility checks")
    liquidity = insurance_cash + treasury_bills + railroad_cash
    return {
        "source": "Berkshire Hathaway official Q2 2026 report",
        "source_url": source_url,
        "source_status": "live",
        "report_period": "Q2 2026",
        "report_date": "2026-06-30",
        "insurance_cash_millions": insurance_cash,
        "treasury_bills_millions": treasury_bills,
        "railroad_cash_millions": railroad_cash,
        "total_assets_millions": total_assets,
        "liquidity_millions": liquidity,
        "liquidity_to_assets_pct": liquidity / total_assets * 100,
        "equity_purchases_ytd_millions": purchases,
        "equity_sales_ytd_millions": sales,
        "net_equity_flow_ytd_millions": purchases - sales,
        "liquidity_label": "Very High" if liquidity / total_assets * 100 > 27 else "High",
        "equity_flow_label": "Net Buyer" if purchases - sales > 5000 else "Neutral / Balanced" if purchases - sales >= -5000 else "Net Seller",
    }


def fetch_berkshire_report(timeout: int = 30) -> dict:
    response = requests.get(BERKSHIRE_Q2_2026_URL, timeout=timeout)
    response.raise_for_status()
    return parse_berkshire_report(response.content)
