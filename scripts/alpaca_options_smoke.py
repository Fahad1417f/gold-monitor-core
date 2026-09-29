from __future__ import annotations

import os
import sys

from adapters.options.alpaca import fetch_alpaca_options


def main() -> int:
    symbol = (sys.argv[1] if len(sys.argv) > 1 else "NVDA").upper()
    feed = os.getenv("ALPACA_OPTIONS_FEED", "indicative")
    contracts = fetch_alpaca_options(symbol)
    print(f"ALPACA_OPTIONS_SMOKE=PASS symbol={symbol} feed={feed} contracts={len(contracts)}")
    for item in contracts[:5]:
        print(
            f"{item.symbol} {item.option_type} strike={item.strike} "
            f"dte={item.dte:.2f} bid={item.bid} ask={item.ask} "
            f"oi={item.open_interest} iv={item.implied_volatility}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
