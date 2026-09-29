from __future__ import annotations
from dataclasses import dataclass

from .analyzer import analyze_contract
from .chain import load_chain, Provider
from .models import OptionContract, OptionsAnalysis, OptionsPolicy, UnderlyingSignal

@dataclass(frozen=True)
class OptionsScan:
    provider: Provider
    underlying: str
    state: str
    analyses: tuple[OptionsAnalysis, ...]
    data_reason: str = ""

def scan_options(
    provider: Provider,
    signal: UnderlyingSignal,
    *,
    target_underlying: float | None,
    policy: OptionsPolicy = OptionsPolicy(),
    currency: str | None = None,
    expiration: int | None = None,
) -> OptionsScan:
    snapshot = load_chain(provider, signal.symbol, currency=currency or signal.symbol, expiration=expiration)
    if snapshot.state != "OK":
        return OptionsScan(provider, signal.symbol, snapshot.state, (), snapshot.reason)
    analyses = tuple(
        analyze_contract(signal, contract, target_underlying=target_underlying, policy=policy)
        for contract in snapshot.contracts
    )
    return OptionsScan(provider, signal.symbol, "OK", analyses)

def confirmed(analyses: tuple[OptionsAnalysis, ...]) -> tuple[OptionsAnalysis, ...]:
    return tuple(item for item in analyses if item.state == "CONFIRMED")
