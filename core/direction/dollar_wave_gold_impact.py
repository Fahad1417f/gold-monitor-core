"""Observed DXY-wave impact mapping for gold.

This module encodes the user's observed KFOO table convention shown in
reference screenshots. It is an evidence layer, not a substitute for
KFOO's hard-entry rules and not a claim of causal market behavior.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation
from typing import Any, Literal, Optional

WaveDirection = Literal["UP", "DOWN"]
Strength = Literal["WEAK", "MEDIUM", "STRONG", "VERY_STRONG"]
GoldEffect = Literal["POSITIVE", "NEGATIVE"]
State = Literal["OBSERVED_RULE", "DATA_UNAVAILABLE"]


@dataclass(frozen=True)
class DollarWaveImpact:
    state: State
    wave_direction: Optional[WaveDirection]
    change_value: Optional[Decimal]
    strength: Optional[Strength]
    gold_effect: Optional[GoldEffect]
    dxy_value: Optional[Decimal]
    timeframe: Optional[str]
    interpretation: Optional[str]
    source: str = "USER_OBSERVED_KFOO_TABLE"
    rule_version: str = "2026-09-23"

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        if self.change_value is not None:
            data["change_value"] = str(self.change_value)
        if self.dxy_value is not None:
            data["dxy_value"] = str(self.dxy_value)
        return data


def _decimal(value: Any) -> Optional[Decimal]:
    if value is None:
        return None
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return None
    if not result.is_finite():
        return None
    return result


def classify_dollar_change(value: Any) -> Optional[Strength]:
    """Map the absolute last-candle dollar change to the observed bands.

    Boundaries are inclusive:
      0.001-0.005 -> WEAK
      0.006-0.009 -> MEDIUM
      0.01-0.09   -> STRONG
      0.1-0.9     -> VERY_STRONG

    Values outside the documented range are intentionally unavailable.
    """
    change = _decimal(value)
    if change is None or change < Decimal("0.001") or change > Decimal("0.9"):
        return None

    if change <= Decimal("0.005"):
        return "WEAK"
    if change <= Decimal("0.009"):
        return "MEDIUM"
    if change <= Decimal("0.09"):
        return "STRONG"
    return "VERY_STRONG"


def dollar_wave_gold_impact(
    wave_direction: Any,
    change_value: Any,
    *,
    dxy_value: Any = None,
    timeframe: Optional[str] = None,
) -> DollarWaveImpact:
    """Return the observed gold-impact interpretation of a DXY wave.

    UP dollar wave -> NEGATIVE gold effect.
    DOWN dollar wave -> POSITIVE gold effect.

    The returned interpretation is deliberately descriptive and is not a
    trading decision. Missing/invalid evidence fails closed.
    """
    direction = str(wave_direction).strip().upper() if wave_direction is not None else ""
    if direction not in {"UP", "DOWN"}:
        return DollarWaveImpact(
            state="DATA_UNAVAILABLE",
            wave_direction=None,
            change_value=None,
            strength=None,
            gold_effect=None,
            dxy_value=_decimal(dxy_value),
            timeframe=timeframe,
            interpretation="Dollar-wave direction is missing or invalid.",
        )

    change = _decimal(change_value)
    strength = classify_dollar_change(change)
    if change is None or strength is None:
        return DollarWaveImpact(
            state="DATA_UNAVAILABLE",
            wave_direction=direction,
            change_value=change,
            strength=None,
            gold_effect=None,
            dxy_value=_decimal(dxy_value),
            timeframe=timeframe,
            interpretation="Last-candle dollar change is missing or outside the documented 0.001-0.9 range.",
        )

    effect: GoldEffect = "NEGATIVE" if direction == "UP" else "POSITIVE"

    if strength == "WEAK":
        interpretation = "Light observed effect on gold."
    elif strength == "MEDIUM":
        interpretation = "Moderate observed effect on gold."
    elif strength == "STRONG":
        interpretation = (
            "Strong observed movement; an UP dollar wave may indicate the "
            "beginning of a gold top, while a DOWN wave may indicate the "
            "beginning of a gold bottom."
        )
    else:
        interpretation = (
            "Very strong observed movement; the reference rule describes a "
            "fast/strong move (pump or dump) on gold."
        )

    return DollarWaveImpact(
        state="OBSERVED_RULE",
        wave_direction=direction,
        change_value=change,
        strength=strength,
        gold_effect=effect,
        dxy_value=_decimal(dxy_value),
        timeframe=timeframe,
        interpretation=interpretation,
    )
