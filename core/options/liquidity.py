from __future__ import annotations
from .models import OptionContract
def validate_liquidity(contract: OptionContract, max_spread_pct: float, min_oi: float, min_volume: float) -> tuple[bool, tuple[str, ...]]:
    reasons: list[str] = []
    if contract.bid <= 0 or contract.ask <= 0 or contract.ask < contract.bid: reasons.append("INVALID_QUOTE")
    if contract.spread_pct is None or contract.spread_pct > max_spread_pct: reasons.append("WIDE_BID_ASK")
    if contract.open_interest < min_oi: reasons.append("LOW_OPEN_INTEREST")
    if contract.volume < min_volume: reasons.append("LOW_VOLUME")
    return (not reasons, tuple(reasons))
