# Options data sources

## Deribit
The monitor can fetch public crypto option-chain data from Deribit. The documented public methods expose active instruments and ticker fields including bid/ask, volume, open interest, implied volatility and Greeks. No account credentials are used.

## Yahoo
The monitor includes a development/research adapter for US-listed equity options. It maps bid/ask, volume, open interest, IV and premium. Yahoo does not reliably provide all Greeks through this interface, so missing Greeks remain missing.

## Source policy
- Market/vendor Greeks take precedence.
- Model Greeks never overwrite source Greeks.
- Missing required data fails closed.
- No order placement is included.
- For production, use a licensed provider with appropriate exchange entitlements. Yahoo is treated as a research adapter, not a guaranteed licensed production feed.
