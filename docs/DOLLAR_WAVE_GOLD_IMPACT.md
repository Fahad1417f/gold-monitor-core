# Dollar Wave -> Gold Impact

## Status

Implemented as an observed-rule evidence layer from the KFOO table examples supplied on 2026-09-23.

This is intentionally not a replacement for the five hard KFOO entry conditions.

## Exact mapping

The table distinguishes the current DXY value from the last-candle change value.

| Last-candle change | Strength | Observed interpretation |
|---|---|---|
| 0.001-0.005 | WEAK | Light effect |
| 0.006-0.009 | MEDIUM | Moderate effect |
| 0.01-0.09 | STRONG | Possible beginning of a top/bottom |
| 0.1-0.9 | VERY_STRONG | Fast/strong movement (pump/dump) |

The boundaries are inclusive.

## Direction mapping

- Dollar wave UP -> observed gold effect NEGATIVE
- Dollar wave DOWN -> observed gold effect POSITIVE

The same numeric change therefore has opposite gold effects depending on wave direction.

## Evidence contract

The implementation stores these fields separately:

- dxy_value: current DXY/index value, e.g. 100.283
- change_value: last-candle change, e.g. 0.006
- wave_direction: UP or DOWN
- strength: WEAK, MEDIUM, STRONG, VERY_STRONG
- gold_effect: POSITIVE or NEGATIVE
- timeframe: source timeframe when known
- state: OBSERVED_RULE or DATA_UNAVAILABLE

Values outside 0.001-0.9, missing values, or invalid directions fail closed.

## Safety boundary

This layer is an observed relationship encoded from the supplied KFOO examples. It does not claim that DXY causally moves gold in every market condition, and it must not independently generate a trade.

The final signal still requires the core KFOO evidence, multi-timeframe context, and valid R:R according to the repository contracts.
