from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, Optional
OptionType = Literal["CALL", "PUT"]
AnalysisState = Literal["CONFIRMED", "WAITING_FOR_EVIDENCE", "REJECTED", "DATA_UNAVAILABLE"]
@dataclass(frozen=True)
class UnderlyingSignal:
    symbol: str
    direction: Literal["BULLISH", "BEARISH", "NEUTRAL", "UNKNOWN"]
    kfoo_state: AnalysisState
    hard_gates_passed: int = 0
    hard_gates_required: int = 5
    mtf_state: Optional[str] = None
    evidence_source: str = "KFOO"
    @property
    def gates_complete(self) -> bool:
        return self.hard_gates_passed >= self.hard_gates_required
@dataclass(frozen=True)
class OptionContract:
    symbol: str
    underlying: str
    option_type: OptionType
    strike: float
    expiration: str
    dte: float
    bid: float
    ask: float
    volume: float
    open_interest: float
    implied_volatility: Optional[float]
    delta: Optional[float] = None
    gamma: Optional[float] = None
    theta: Optional[float] = None
    vega: Optional[float] = None
    premium: Optional[float] = None
    contract_multiplier: float = 1.0
    @property
    def mid(self) -> float:
        return (self.bid + self.ask) / 2.0
    @property
    def spread(self) -> float:
        return max(0.0, self.ask - self.bid)
    @property
    def spread_pct(self) -> Optional[float]:
        mid = self.mid
        return None if mid <= 0 else self.spread / mid
@dataclass(frozen=True)
class OptionsPolicy:
    min_dte: float = 7.0
    max_dte: float = 90.0
    min_delta_abs: float = 0.30
    max_delta_abs: float = 0.70
    max_spread_pct: float = 0.10
    min_open_interest: float = 1.0
    min_volume: float = 0.0
    min_rr: float = 1.0
@dataclass(frozen=True)
class OptionsAnalysis:
    state: AnalysisState
    contract: str
    underlying: str
    direction: str
    reasons: tuple[str, ...]
    target_underlying: Optional[float]
    entry_premium: Optional[float]
    target_pnl_per_contract: Optional[float]
    target_rr: Optional[float]
    max_loss_per_contract: Optional[float]
    source: str = "OPTIONS_MONITOR"
