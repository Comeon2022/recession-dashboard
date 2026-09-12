"""Best-effort parser for the official FINRA Margin Statistics webpage."""

from __future__ import annotations

import re
from html.parser import HTMLParser

import requests

FINRA_URL = "https://www.finra.org/rules-guidance/key-topics/margin-accounts/margin-statistics"


class _TableParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.rows=[]; self.row=[]; self.cell=[]; self.in_cell=False
    def handle_starttag(self, tag, attrs):
        if tag in ("td", "th"): self.in_cell=True; self.cell=[]
        elif tag == "tr": self.row=[]
    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.in_cell: self.row.append("".join(self.cell).strip()); self.in_cell=False
        elif tag == "tr" and self.row: self.rows.append(self.row)
    def handle_data(self, data):
        if self.in_cell: self.cell.append(data)


def fetch_margin_debt(timeout: int = 20) -> dict:
    response = requests.get(FINRA_URL, timeout=timeout, headers={"User-Agent": "recession-dashboard/1.0"})
    response.raise_for_status()
    parser = _TableParser(); parser.feed(response.text)
    header_index = next((index for index, row in enumerate(parser.rows) if any("debit balances" in cell.lower() for cell in row)), None)
    if header_index is None:
        raise ValueError("FINRA margin statistics table could not be parsed")
    data_rows = [row for row in parser.rows[header_index + 1:] if len(row) >= 2]
    for row in data_rows:
        debit = re.sub(r"[^0-9.]", "", row[1])
        if debit:
            return {"debit_balance_millions": float(debit), "reference_month": row[0], "source": "FINRA", "source_url": FINRA_URL}
    raise ValueError("FINRA margin statistics table has no debit balance rows")
