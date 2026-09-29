from __future__ import annotations
from dataclasses import dataclass
from math import exp, erf, log, pi, sqrt
from typing import Literal
OptionType = Literal["CALL", "PUT"]
@dataclass(frozen=True)
class Greeks:
    price: float
    delta: float
    gamma: float
    theta: float
    vega: float
def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))
def _norm_pdf(x: float) -> float:
    return exp(-0.5 * x * x) / sqrt(2.0 * pi)
def black_scholes_greeks(spot: float, strike: float, time_years: float, rate: float, volatility: float, option_type: OptionType) -> Greeks:
    """European Black-Scholes estimate; vendor/exchange Greeks remain authoritative when supplied."""
    if min(spot, strike) <= 0 or time_years <= 0 or volatility <= 0:
        raise ValueError("spot, strike, time_years and volatility must be positive")
    sigma_sqrt_t = volatility * sqrt(time_years)
    d1 = (log(spot / strike) + (rate + 0.5 * volatility**2) * time_years) / sigma_sqrt_t
    d2 = d1 - sigma_sqrt_t
    pdf = _norm_pdf(d1)
    disc = exp(-rate * time_years)
    if option_type == "CALL":
        price = spot * _norm_cdf(d1) - strike * disc * _norm_cdf(d2)
        delta = _norm_cdf(d1)
        theta = (-(spot * pdf * volatility) / (2 * sqrt(time_years)) - rate * strike * disc * _norm_cdf(d2)) / 365.0
    elif option_type == "PUT":
        price = strike * disc * _norm_cdf(-d2) - spot * _norm_cdf(-d1)
        delta = _norm_cdf(d1) - 1.0
        theta = (-(spot * pdf * volatility) / (2 * sqrt(time_years)) + rate * strike * disc * _norm_cdf(-d2)) / 365.0
    else:
        raise ValueError("option_type must be CALL or PUT")
    gamma = pdf / (spot * sigma_sqrt_t)
    vega = spot * pdf * sqrt(time_years) / 100.0
    return Greeks(price, delta, gamma, theta, vega)
