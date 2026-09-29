# Options Monitor Architecture

The Options Monitor applies the existing KFOO/MTF evidence discipline to options without assuming that an underlying signal automatically makes an option contract suitable.

Flow: KFOO / market context -> UNDERLYING SIGNAL -> OPTIONS CHAIN SNAPSHOT -> CONTRACT POLICY -> OPTIONS OPPORTUNITY

Preserved expertise:
- KFOO five hard gates remain upstream.
- 4H -> 1H -> 15M -> 3M context remains upstream.
- KFOO Whale, RSI, divergence, accumulation/distribution and H&S remain evidence.
- Gold keeps the DXY dollar-wave evidence layer.
- Crypto uses BTC market leadership context, never the DXY rule.
- Evidence is never silently substituted with a proxy.
- Missing required inputs produce WAITING_FOR_EVIDENCE or DATA_UNAVAILABLE.
- R:R is target-based for options; it does not fabricate a stop or use theoretical unlimited maximum profit as reward.

Contract data: underlying, venue, expiration, DTE, strike, call/put, bid, ask, spread, volume, open interest, IV, Delta, Gamma, Theta, Vega, premium, multiplier, optional target underlying.

Greek provenance: vendor/exchange Greeks remain authoritative. Black-Scholes values are MODEL estimates and must not overwrite vendor Greeks.

Safety: read-only. No order placement, broker credentials, or execution logic is part of the Options Monitor.
