# Gold Monitor Core

Read-only, fail-closed monitoring architecture for XAUUSD with a KFOO evidence layer, multi-timeframe context, research/outcome tracking, and Telegram alerting.

## Scope

This repository is a clean rebuild. It does not copy the legacy V54/V56 architecture wholesale and it does not enable trade execution.

### Core principles

- Read-only by default
- Fail-closed when required evidence is unavailable
- KFOO evidence must remain distinguishable from proxy/market-data analysis
- Multi-timeframe context: 4H → 1H → 15M → 3M timing
- Deterministic hard rules before any confidence score
- Full signal/outcome audit trail
- Broker/execution adapters are out of scope for the initial core

## Planned modules

```text
core/
  kfoo_rules/
  evidence/
  direction/
    dollar_wave_gold_impact.py
  multi_timeframe/
  structure/
  scoring/
vision/
  tradingview/
  kfoo_table/
  whale_detection/
data/
  market/
  candles/
  outcomes/
research/
alerts/
  telegram/
tests/
docs/
```

## Dollar-wave evidence

The repository now contains an observed-rule component for the DXY table convention supplied on 2026-09-23:

- 0.001-0.005 → WEAK
- 0.006-0.009 → MEDIUM
- 0.01-0.09 → STRONG
- 0.1-0.9 → VERY_STRONG
- Dollar wave UP → observed NEGATIVE gold effect
- Dollar wave DOWN → observed POSITIVE gold effect

The current DXY/index price and the last-candle change value are stored separately. Invalid or undocumented values fail closed. This layer is evidence/context only and cannot independently create a trade signal.

See docs/DOLLAR_WAVE_GOLD_IMPACT.md.

## KFOO evidence contract

A signal may only be labelled KFOO when its required KFOO evidence is explicitly available and verified. Otherwise the system uses states such as WAITING_FOR_EVIDENCE, DATA_UNAVAILABLE, or PROXY and never silently substitutes a proxy for KFOO.

## Trading safety

No live trading or order placement is enabled by this repository's initial design.
