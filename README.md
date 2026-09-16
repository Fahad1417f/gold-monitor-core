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

## KFOO evidence contract

A signal may only be labelled `KFOO` when its required KFOO evidence is explicitly available and verified. Otherwise the system uses states such as `WAITING_FOR_EVIDENCE`, `DATA_UNAVAILABLE`, or `PROXY` and never silently substitutes a proxy for KFOO.

## Trading safety

No live trading or order placement is enabled by this repository's initial design.
