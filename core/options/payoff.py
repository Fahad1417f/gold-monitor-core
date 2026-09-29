from __future__ import annotations
from .models import OptionContract
def long_option_pnl(contract: OptionContract, target_underlying: float) -> float:
    premium = contract.premium if contract.premium is not None else contract.mid
    if premium <= 0: raise ValueError("premium must be positive")
    intrinsic = max(target_underlying - contract.strike, 0.0) if contract.option_type == "CALL" else max(contract.strike - target_underlying, 0.0)
    return (intrinsic - premium) * contract.contract_multiplier
def target_rr(contract: OptionContract, target_underlying: float) -> tuple[float, float, float | None]:
    premium = contract.premium if contract.premium is not None else contract.mid
    if premium <= 0: raise ValueError("premium must be positive")
    pnl = long_option_pnl(contract, target_underlying)
    max_loss = premium * contract.contract_multiplier
    rr = None if pnl <= 0 or max_loss <= 0 else pnl / max_loss
    return pnl, max_loss, rr
