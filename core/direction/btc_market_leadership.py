"""Crypto-only BTC market leadership context.

This is context evidence for crypto options. It is intentionally separate
from the GOLD-only DXY dollar-wave rule and never creates a trade signal.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, Optional

Leadership = Literal["BULLISH", "BEARISH", "NEUTRAL", "DATA_UNAVAILABLE"]

@dataclass(frozen=True)
class BTCMarketLeadership:
    state: Leadership
    btc_symbol: str
    target_symbol: str
    timeframe: Optional[str]
    reason: str
    source: str = "MARKET_CONTEXT"

def btc_market_leadership(*, btc_direction: str | None, target_direction: str | None, target_market: str, timeframe: str | None = None) -> BTCMarketLeadership:
    market = str(target_market).strip().upper()
    if market not in {"CRYPTO", "CRYPTO_OPTIONS"}:
        return BTCMarketLeadership("DATA_UNAVAILABLE", "BTCUSDT", market, timeframe, "BTC leadership context is restricted to crypto.")
    btc = str(btc_direction or "").strip().upper()
    target = str(target_direction or "").strip().upper()
    if btc not in {"BULLISH", "BEARISH", "NEUTRAL"} or target not in {"BULLISH", "BEARISH", "NEUTRAL"}:
        return BTCMarketLeadership("DATA_UNAVAILABLE", "BTCUSDT", market, timeframe, "BTC or target direction is missing/invalid.")
    if target == "NEUTRAL" or btc == "NEUTRAL":
        return BTCMarketLeadership("NEUTRAL", "BTCUSDT", market, timeframe, "BTC/target direction is neutral.")
    if btc == target:
        return BTCMarketLeadership(btc, "BTCUSDT", market, timeframe, "BTC direction agrees with target crypto direction.")
    return BTCMarketLeadership("NEUTRAL", "BTCUSDT", market, timeframe, "BTC direction disagrees with target crypto direction.")
