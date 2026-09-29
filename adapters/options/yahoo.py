from __future__ import annotations
import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any
from core.options.models import OptionContract

BASE_URL = "https://query1.finance.yahoo.com/v7/finance/options"

def _get(symbol: str, expiration: int | None = None) -> dict[str, Any]:
    url = BASE_URL + "/" + urllib.parse.quote(symbol.upper())
    if expiration is not None:
        url += "?date=" + str(int(expiration))
    request = urllib.request.Request(url, headers={"User-Agent": "gold-monitor-core/options"})
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.load(response)

def fetch_yahoo_options(symbol: str, expiration: int | None = None) -> tuple[list[int], list[OptionContract]]:
    payload = _get(symbol, expiration)
    result = payload["optionChain"]["result"][0]
    expirations = [int(x) for x in result.get("expirationDates", [])]
    if expiration is None and expirations:
        payload = _get(symbol, expirations[0])
        result = payload["optionChain"]["result"][0]
    contracts = []
    for side in result.get("options", []):
        for rows, option_type in ((side.get("calls", []), "CALL"), (side.get("puts", []), "PUT")):
            for item in rows:
                expiry_ts = int(item.get("expiration") or 0)
                if not expiry_ts:
                    continue
                expiry = datetime.fromtimestamp(expiry_ts, tz=timezone.utc)
                dte = (expiry - datetime.now(timezone.utc)).total_seconds() / 86400
                contracts.append(OptionContract(
                    symbol=str(item.get("contractSymbol") or ""),
                    underlying=symbol.upper(), option_type=option_type,
                    strike=float(item["strike"]), expiration=expiry.date().isoformat(), dte=dte,
                    bid=float(item.get("bid") or 0), ask=float(item.get("ask") or 0),
                    volume=float(item.get("volume") or 0), open_interest=float(item.get("openInterest") or 0),
                    implied_volatility=(float(item["impliedVolatility"]) if item.get("impliedVolatility") is not None else None),
                    premium=(float(item["lastPrice"]) if item.get("lastPrice") is not None else None),
                    contract_multiplier=100.0,
                ))
    return expirations, contracts
