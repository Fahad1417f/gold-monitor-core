from __future__ import annotations
from .liquidity import validate_liquidity
from .models import OptionContract, OptionsAnalysis, OptionsPolicy, UnderlyingSignal
from .payoff import target_rr
def analyze_contract(signal: UnderlyingSignal, contract: OptionContract, *, target_underlying: float | None, policy: OptionsPolicy = OptionsPolicy()) -> OptionsAnalysis:
    if signal.kfoo_state in {"DATA_UNAVAILABLE", "WAITING_FOR_EVIDENCE"}:
        return OptionsAnalysis("WAITING_FOR_EVIDENCE", contract.symbol, contract.underlying, signal.direction, ("UNDERLYING_KFOO_EVIDENCE_INCOMPLETE",), target_underlying, None, None, None, None)
    if signal.direction == "NEUTRAL":
        return OptionsAnalysis("REJECTED", contract.symbol, contract.underlying, signal.direction, ("UNDERLYING_DIRECTION_NEUTRAL",), target_underlying, None, None, None, None)
    reasons: list[str] = []
    expected = "CALL" if signal.direction == "BULLISH" else "PUT"
    if contract.option_type != expected: reasons.append("OPTION_TYPE_MISMATCH")
    if not (policy.min_dte <= contract.dte <= policy.max_dte): reasons.append("DTE_OUT_OF_POLICY")
    if contract.delta is None: reasons.append("DELTA_UNAVAILABLE")
    elif not (policy.min_delta_abs <= abs(contract.delta) <= policy.max_delta_abs): reasons.append("DELTA_OUT_OF_POLICY")
    liquid, liquidity_reasons = validate_liquidity(contract, policy.max_spread_pct, policy.min_open_interest, policy.min_volume)
    if not liquid: reasons.extend(liquidity_reasons)
    premium = contract.premium if contract.premium is not None else contract.mid
    if premium <= 0: reasons.append("PREMIUM_UNAVAILABLE")
    reward = max_loss = rr = None
    if target_underlying is not None and premium > 0:
        reward, max_loss, rr = target_rr(contract, target_underlying)
        if rr is None: reasons.append("TARGET_REWARD_NON_POSITIVE")
        elif rr < policy.min_rr: reasons.append("TARGET_RR_BELOW_POLICY")
    if reasons:
        return OptionsAnalysis("REJECTED", contract.symbol, contract.underlying, signal.direction, tuple(reasons), target_underlying, premium, reward, rr, max_loss)
    return OptionsAnalysis("CONFIRMED", contract.symbol, contract.underlying, signal.direction, ("UNDERLYING_GATES_AND_CONTRACT_POLICY_PASS",), target_underlying, premium, reward, rr, max_loss)
