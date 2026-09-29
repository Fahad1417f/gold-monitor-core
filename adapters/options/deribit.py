from __future__ import annotations
import json
import urllib.request
from datetime import datetime, timezone
from typing import Any
from core.options.models import OptionContract

BASE_URL = "https://www.deribit.com/api/v2"

def _rpc(method: str, params: dict[str, Any]) -> dict[str, Any]:
    payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    request = urllib.request.Request(BASE_URL + "/" + method, data=payload, method="GET", headers={"Content-Type": "application/json", "User-Agent": "gold-monitor-core/options"})
    with urllib.request.urlopen(request, timeout=15) as response:
        data = json.load(response)
    if data.get("error"):
        raise RuntimeError(f"Deribit API error: {data['error']}")
    return data["result"]

def fetch_deribit_options(currency: str = "BTC") -> list[OptionContract]:
    instruments = _rpc("public/get_instruments", {"currency": currency.upper(), "kind": "option", "expired": False})
    now = datetime.now(timezone.utc)
    contracts = []
    for instrument in instruments:
        name = instrument["instrument_name"]
        ticker = _rpc("public/ticker", {"instrument_name": name})
        expiry = datetime.fromtimestamp(instrument["expiration_timestamp"] / 1000, tz=timezone.utc)
        dte = (expiry - now).total_seconds() / 86400
        if dte <= 0:
            continue
        bid, ask = ticker.get("best_bid_price"), ticker.get("best_ask_price")
        greeks = ticker.get("greeks") or {}
        if bid is None or ask is None:
            continue
        contracts.append(OptionContract(
            symbol=name, underlying=currency.upper(),
            option_type=str(instrument["option_type"]).upper(),
            strike=float(instrument["strike"]), expiration=expiry.date().isoformat(),
            dte=dte, bid=float(bid), ask=float(ask),
            volume=float((ticker.get("stats") or {}).get("volume") or 0),
            open_interest=float(ticker.get("open_interest") or 0),
            implied_volatility=(float(ticker["mark_iv"]) / 100.0 if ticker.get("mark_iv") is not None else None),
            delta=(float(greeks["delta"]) if greeks.get("delta") is not None else None),
            gamma=(float(greeks["gamma"]) if greeks.get("gamma") is not None else None),
            theta=(float(greeks["theta"]) if greeks.get("theta") is not None else None),
            vega=(float(greeks["vega"]) if greeks.get("vega") is not None else None),
            premium=float(ticker["mark_price"]) if ticker.get("mark_price") is not None else None,
            contract_multiplier=float(instrument.get("contract_size") or 1),
        ))
    return contracts
