from __future__ import annotations

import os
import time
import datetime as dt
from typing import Any, Dict, List, Set, Tuple, Optional

import requests


FINNHUB_KEY = os.getenv("FINNHUB_API_KEY") or "PUT_YOUR_KEY_HERE"
BASE = "https://finnhub.io/api/v1"


# Adjust if you want to be stricter/looser.
US_EXCH_KEYWORDS = (
    "NYSE",
    "NASDAQ",
    "AMEX",
    "ARCA",
    "BATS",
    "IEX",
    "NYSE MKT",
)

SESSION = requests.Session()
SESSION.headers.update({"Accept": "application/json"})


def finnhub_get(path: str, params: Dict[str, Any]) -> Any:
    params = dict(params)
    params["token"] = FINNHUB_KEY
    r = SESSION.get(f"{BASE}{path}", params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def is_us_exchange(exchange_str: Optional[str]) -> bool:
    if not exchange_str:
        return False
    ex = exchange_str.upper()
    return any(k in ex for k in US_EXCH_KEYWORDS)


def forward_split_events(symbol: str, start: dt.date, end: dt.date) -> List[Dict[str, Any]]:
    """
    Finnhub stock splits response includes factors (commonly fromFactor/toFactor).
    Forward split: toFactor > fromFactor
    Reverse split: toFactor < fromFactor
    """
    data = finnhub_get(
        "/stock/split",
        {"symbol": symbol, "from": start.isoformat(), "to": end.isoformat()},
    )

    events = []
    if not isinstance(data, list):
        return events

    for ev in data:
        try:
            ff = float(ev.get("fromFactor"))
            tf = float(ev.get("toFactor"))
        except (TypeError, ValueError):
            continue

        # Forward split only
        if tf > ff:
            events.append(ev)

    return events


def main(days_ahead: int = 10, price_threshold: float = 1000.0) -> List[Dict[str, Any]]:
    if not FINNHUB_KEY or FINNHUB_KEY == "PUT_YOUR_KEY_HERE":
        raise RuntimeError("Set FINNHUB_API_KEY env var or put your key in FINNHUB_KEY.")

    start = dt.date.today()
    end = start + dt.timedelta(days=days_ahead)

    # 1) Earnings calendar for next N days
    cal = finnhub_get("/calendar/earnings", {"from": start.isoformat(), "to": end.isoformat()})
    earnings = cal.get("earningsCalendar", []) if isinstance(cal, dict) else []
    symbols: Set[str] = {row.get("symbol") for row in earnings if row.get("symbol")}
    symbols = {s.strip().upper() for s in symbols if s and isinstance(s, str)}

    results: List[Dict[str, Any]] = []

    for i, sym in enumerate(sorted(symbols)):
        # crude rate limiting (free tier is limited; tune as needed)
        if i and i % 25 == 0:
            time.sleep(1.2)

        # 2) Check for forward split in the same date window
        try:
            split_events = forward_split_events(sym, start, end)
        except requests.HTTPError:
            continue

        if not split_events:
            continue

        # 3) Check US exchange
        try:
            prof = finnhub_get("/stock/profile2", {"symbol": sym})
        except requests.HTTPError:
            continue

        exchange = prof.get("exchange") if isinstance(prof, dict) else None
        if not is_us_exchange(exchange):
            continue

        # 4) Check current price
        try:
            q = finnhub_get("/quote", {"symbol": sym})
        except requests.HTTPError:
            continue

        last_price = q.get("c") if isinstance(q, dict) else None
        try:
            last_price = float(last_price)
        except (TypeError, ValueError):
            continue

        if last_price <= price_threshold:
            continue

        # Keep the most relevant split event (earliest date in window)
        # Finnhub split event often has 'date' (YYYY-MM-DD)
        split_events_sorted = sorted(
            split_events, key=lambda ev: (ev.get("date") or "9999-12-31")
        )
        ev0 = split_events_sorted[0]

        results.append(
            {
                "symbol": sym,
                "company": prof.get("name"),
                "exchange": exchange,
                "last_price": last_price,
                "split_date": ev0.get("date"),
                "fromFactor": ev0.get("fromFactor"),
                "toFactor": ev0.get("toFactor"),
            }
        )

    return results


if __name__ == "__main__":
    rows = main(days_ahead=10, price_threshold=1000.0)
    # Print as a simple table-ish output
    if not rows:
        print("No matches found.")
    else:
        rows = sorted(rows, key=lambda r: (r["split_date"] or "", -r["last_price"]))
        for r in rows:
            ratio = f'{r["toFactor"]}:{r["fromFactor"]}'
            print(
                f'{r["symbol"]:>6} | {r["exchange"]:<10} | ${r["last_price"]:>9.2f} | '
                f'split {r["split_date"]} ({ratio}) | {r.get("company","")}'
            )
