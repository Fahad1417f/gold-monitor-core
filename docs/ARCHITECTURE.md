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

### Proxy and observed-rule evidence

Market-data indicators such as EMA, SMI, ATR, RSI, DMI, swing structure, and candle-derived metrics are useful research evidence. They must never be relabelled as KFOO evidence.

The DOLLAR_WAVE_GOLD_IMPACT layer is an observed-rule evidence component derived from the user's supplied KFOO table examples. It is kept separate from the five hard KFOO entry gates and cannot independently create a trade signal.

## Dollar-wave evidence

The DXY table has two different numeric concepts:

1. DXY current/index value, such as 100.283.
2. Last-candle change value, classified into the observed bands:
   - 0.001-0.005 -> WEAK
   - 0.006-0.009 -> MEDIUM
   - 0.01-0.09 -> STRONG
   - 0.1-0.9 -> VERY_STRONG

Direction mapping:

- Dollar wave UP -> observed gold effect NEGATIVE.
- Dollar wave DOWN -> observed gold effect POSITIVE.

The implementation fails closed for missing/invalid direction and for change values outside the documented range. It does not infer a causal relationship or assign a probability.

## Decision flow

```
market data + KFOO observations + observed dollar-wave evidence
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
          R:R gate
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
