import unittest
from unittest.mock import patch

from adapters.options import alpaca, yahoo
from core.options.chain import load_chain


class OptionsAdapterTests(unittest.TestCase):
    def test_yahoo_mapping(self):
        payload = {"optionChain":{"result":[{
            "expirationDates":[1793395200],
            "options":[{"calls":[{
                "contractSymbol":"TEST261030C00100000","strike":100,"expiration":1793395200,
                "bid":4.8,"ask":5.2,"lastPrice":5.0,"volume":100,"openInterest":500,
                "impliedVolatility":0.30
            }],"puts":[]}]
        }]}}
        with patch.object(yahoo, "_get", side_effect=[payload, payload]):
            expirations, contracts = yahoo.fetch_yahoo_options("TEST")
        self.assertEqual(expirations, [1793395200])
        self.assertEqual(len(contracts), 1)
        self.assertIsNone(contracts[0].delta)
        self.assertEqual(contracts[0].contract_multiplier, 100.0)

    def test_alpaca_mapping(self):
        contracts_payload = [{
            "symbol": "AAPL261016C00200000",
            "expiration_date": "2026-10-16",
            "type": "call",
            "strike_price": "200",
            "size": "100",
            "open_interest": "321"
        }]
        snapshots_payload = {
            "snapshots": {
                "AAPL261016C00200000": {
                    "latestTrade": {"p": 6.25},
                    "latestQuote": {"bp": 6.20, "ap": 6.30},
                    "greeks": {
                        "delta": 0.55, "gamma": 0.03, "theta": -0.08,
                        "vega": 0.12, "impliedVolatility": 0.31
                    }
                }
            }
        }
        with patch.object(alpaca, "_contract_rows", return_value=contracts_payload):
            with patch.object(alpaca, "_chain_snapshot", return_value=snapshots_payload):
                result = alpaca.fetch_alpaca_options("AAPL", "2026-10-16")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].option_type, "CALL")
        self.assertEqual(result[0].strike, 200.0)
        self.assertEqual(result[0].open_interest, 321.0)
        self.assertEqual(result[0].delta, 0.55)
        self.assertEqual(result[0].contract_multiplier, 100.0)

    def test_loader_fails_closed(self):
        with patch("adapters.options.yahoo.fetch_yahoo_options", side_effect=RuntimeError("offline")):
            result = load_chain("YAHOO", "NVDA")
        self.assertEqual(result.state, "DATA_UNAVAILABLE")
        self.assertEqual(result.contracts, ())

    def test_alpaca_loader_fails_closed(self):
        with patch("adapters.options.alpaca.fetch_alpaca_options", side_effect=RuntimeError("missing credentials")):
            result = load_chain("ALPACA", "NVDA")
        self.assertEqual(result.state, "DATA_UNAVAILABLE")
        self.assertEqual(result.contracts, ())


if __name__ == "__main__":
    unittest.main()
