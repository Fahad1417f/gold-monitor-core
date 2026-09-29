# Options data sources

## Deribit
The monitor can fetch public crypto option-chain data from Deribit. The documented public methods expose active instruments and ticker fields including bid/ask, volume, open interest, implied volatility and Greeks. No account credentials are used.

## Alpaca — US options (primary)
The monitor can fetch US-listed option-chain snapshots from Alpaca. The documented chain endpoint returns the latest trade, latest quote and Greeks for contracts, with `opra` as the official OPRA feed and `indicative` as a free indicative feed. Contract metadata is used for expiration, strike, multiplier and open interest. API credentials are required and are read only from environment variables.

Environment:
- `ALPACA_API_KEY_ID`
- `ALPACA_API_SECRET_KEY`
- `ALPACA_OPTIONS_FEED=opra` for an OPRA entitlement, or `indicative` for the free indicative feed.
- `ALPACA_BROKER_BASE_URL` may be set to the production broker API when appropriate; paper is the safe default for contract metadata.

The adapter never places orders. Execution remains OFF.

## Yahoo
The monitor retains a development/research adapter for US-listed equity options as a fallback. It maps bid/ask, volume, open interest, IV and premium. Yahoo does not reliably provide all Greeks through this interface, so missing Greeks remain missing.

## Source policy
- Market/vendor Greeks take precedence.
- Model Greeks never overwrite source Greeks.
- Missing required data fails closed.
- No order placement is included.
- For production, use a licensed provider with appropriate exchange entitlements. Yahoo is treated as a research adapter, not a guaranteed licensed production feed.
