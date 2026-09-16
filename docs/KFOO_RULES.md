# KFOO Rule Contract

## Long-side core conditions

All required conditions below must be true before a long-side KFOO confirmation can be produced:

1. A candle closes above the continuity average.
2. The liquidity table shows inbound liquidity.
3. Inbound liquidity is greater than outbound liquidity.
4. The price channel is ascending.
5. The KFOO signal explicitly shows `Whales Buying`.

## Short-side core conditions

The short-side contract is the inverse of the long-side contract.

## Multi-timeframe context

The monitor evaluates the broader context beginning at 4H, then 1H, with 15M used for setup/quick-trade context and 3M used for general entry timing.

## Additional evidence

KFOO divergence, KFOO arrows, cloud-related arrows, accumulation/distribution points, and head-and-shoulders structures may support analysis but do not silently replace the required core conditions.

## Missing evidence

Missing or unreadable required evidence produces `WAITING_FOR_EVIDENCE` or `DATA_UNAVAILABLE`. It must never be converted into a bullish or bearish state by assumption.
