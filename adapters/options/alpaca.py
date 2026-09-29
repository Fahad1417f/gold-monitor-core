from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any

from core.options.models import OptionContract

DATA_BASE_URL = "https://data.alpaca.markets/v1beta1/options/snapshots"
BROKER_BASE_URL = "https://paper-api.alpaca.markets/v2/options/contracts"


def _headers() -> dict[str, str]:
    key = os.getenv("ALPACA_API_KEY_ID")
    secret = os.getenv("ALPACA_API_SECRET_KEY")
    if not key or not secret:
        raise RuntimeError("ALPACA_API_KEY_ID and ALPACA_API_SECRET_KEY are required.")
    return {
        "Accept": "application/json",
        "APCA-API-KEY-ID": key,
        "APCA-API-SECRET-KEY": secret,
        "User-Agent": "gold-monitor-core/options",
    }


def _get(url: str) -> dict[str, Any]:
    request = urllib.request.Request(url, headers=_headers())
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def _contract_rows(symbol: str, expiration: str | None) -> list[dict[str, Any]]:
    params = {
        "underlying_symbols": symbol.upper(),
        "status": "active",
        "limit": "10000",
    }
    if expiration:
        params["expiration_date"] = expiration
    url = BROKER_BASE_URL + "?" + urllib.parse.urlencode(params)
    payload = _get(url)
    return list(payload.get("option_contracts") or [])


def _chain_snapshot(symbol: str, expiration: str | None) -> dict[str, Any]:
    params: dict[str, str] = {
        "feed": os.getenv("ALPACA_OPTIONS_FEED", "indicative"),
        "limit": "1000",
    }
    if expiration:
        params["expiration_date"] = expiration
    url = DATA_BASE_URL.replace(
        "/snapshots/",
        "/snapshots/",
    ) + "/" + urllib.parse.quote(symbol.upper()) + "?" + urllib.parse.urlencode(params)
    return _get(url)


def _parse_occ(symbol: str) -> tuple[str, str, str, float]:
    # OCC option symbology: ROOT + YYMMDD + C/P + 8-digit strike*1000.
    if len(symbol) < 16:
        raise ValueError(f"Invalid OCC option symbol: {symbol}")
    tail = symbol[-15:]
    root = symbol[:-15]
    date_code, option_type, strike_code = tail[:6], tail[6], tail[7:]
    if option_type not in {"C", "P"}:
        raise ValueError(f"Invalid option type in symbol: {symbol}")
    expiration = datetime.strptime(date_code, "%y%m%d").date().isoformat()
    strike = int(strike_code) / 1000.0
    return root, expiration, option_type, strike


def fetch_alpaca_options(
    symbol: str,
    expiration: str | None = None,
) -> list[OptionContract]:
    symbol = symbol.upper()
    rows = _contract_rows(symbol, expiration)
    metadata = {str(row.get("symbol")): row for row in rows if row.get("symbol")}

    payload = _chain_snapshot(symbol, expiration)
    snapshots = payload.get("snapshots") or {}
    contracts: list[OptionContract] = []

    for contract_symbol, snapshot in snapshots.items():
        try:
            occ_root, occ_expiration, option_code, occ_strike = _parse_occ(contract_symbol)
        except (TypeError, ValueError):
            continue

        row = metadata.get(contract_symbol, {})
        expiration_value = str(row.get("expiration_date") or occ_expiration)
        strike = float(row.get("strike_price") or occ_strike)
        option_type = "CALL" if str(row.get("type") or option_code).lower() in {"call", "c"} else "PUT"
        multiplier = float(row.get("size") or 100)

        quote = snapshot.get("latestQuote") or {}
        trade = snapshot.get("latestTrade") or {}
        greeks = snapshot.get("greeks") or {}

        bid = float(quote.get("bp") or quote.get("bid_price") or 0)
        ask = float(quote.get("ap") or quote.get("ask_price") or 0)
        premium_value = trade.get("p") or trade.get("price")
        premium = float(premium_value) if premium_value is not None else None

        expiry_dt = datetime.fromisoformat(expiration_value).replace(tzinfo=timezone.utc)
        dte = max(0.0, (expiry_dt - datetime.now(timezone.utc)).total_seconds() / 86400)

        iv = greeks.get("impliedVolatility")
        if iv is None:
            iv = greeks.get("implied_volatility")

        contracts.append(
            OptionContract(
                symbol=str(contract_symbol),
                underlying=symbol,
                option_type=option_type,
                strike=strike,
                expiration=expiration_value,
                dte=dte,
                bid=bid,
                ask=ask,
                volume=float(snapshot.get("volume") or 0),
                open_interest=float(row.get("open_interest") or 0),
                implied_volatility=(float(iv) if iv is not None else None),
                delta=(float(greeks["delta"]) if greeks.get("delta") is not None else None),
                gamma=(float(greeks["gamma"]) if greeks.get("gamma") is not None else None),
                theta=(float(greeks["theta"]) if greeks.get("theta") is not None else None),
                vega=(float(greeks["vega"]) if greeks.get("vega") is not None else None),
                premium=premium,
                contract_multiplier=multiplier,
            )
        )

    return contracts
