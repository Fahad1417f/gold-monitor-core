# Architecture

## Objective

Build a maintainable Gold Monitor Core that separates market-data analysis from KFOO-specific visual evidence.

## Source boundary

### KFOO evidence

KFOO-specific fields are authoritative only when explicitly observed through an approved KFOO source/adapter. Examples include:

- Continuity-average relation
- Liquidity inflow/outflow state
- Inflow greater than outflow
- Price-channel direction
- Whales Buying / Whales Selling
- KFOO-specific divergence/arrow/table evidence

### Proxy evidence

Market-data indicators such as EMA, SMI, ATR, RSI, DMI, swing structure, and candle-derived metrics are useful research evidence. They must never be relabelled as KFOO evidence.

## Decision flow

```text
market data + KFOO observations
            |
            v
       normalization
            |
            v
       evidence ledger
            |
            v
      hard-rule gates
            |
            v
    4H / 1H / 15M context
            |
            v
         3M timing
            |
            v
      CONFIRMED / WAIT
            |
            v
      audit + outcome
```

## Initial safety boundary

The core is read-only. Broker execution, order placement, and credential management are intentionally excluded from the initial repository.

## Legacy migration rule

Code from legacy GOLD-BOT/V54/V56 and the existing signal monitor is migrated selectively only after its behavior, dependencies, and test coverage are reviewed. The new repository is not a blind copy.
