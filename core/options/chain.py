from __future__ import annotations
from dataclasses import dataclass
from typing import Literal
from .models import OptionContract

Provider = Literal["YAHOO", "DERIBIT"]

@dataclass(frozen=True)
class OptionChainSnapshot:
    provider: Provider
    underlying: str
    contracts: tuple[OptionContract, ...]
    state: Literal["OK", "DATA_UNAVAILABLE"]
    reason: str = ""

def load_chain(provider: Provider, underlying: str, **kwargs) -> OptionChainSnapshot:
    try:
        if provider == "YAHOO":
            from adapters.options.yahoo import fetch_yahoo_options
            _, contracts = fetch_yahoo_options(underlying, kwargs.get("expiration"))
        elif provider == "DERIBIT":
            from adapters.options.deribit import fetch_deribit_options
            contracts = fetch_deribit_options(kwargs.get("currency", underlying))
        else:
            return OptionChainSnapshot(provider, underlying, (), "DATA_UNAVAILABLE", "Unsupported options provider.")
        if not contracts:
            return OptionChainSnapshot(provider, underlying, (), "DATA_UNAVAILABLE", "Provider returned no option contracts.")
        return OptionChainSnapshot(provider, underlying, tuple(contracts), "OK")
    except Exception as exc:
        return OptionChainSnapshot(provider, underlying, (), "DATA_UNAVAILABLE", f"{type(exc).__name__}: {exc}")
