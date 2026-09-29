import unittest
from unittest.mock import patch
from adapters.options import yahoo
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

    def test_loader_fails_closed(self):
        with patch("adapters.options.yahoo.fetch_yahoo_options", side_effect=RuntimeError("offline")):
            result = load_chain("YAHOO", "NVDA")
        self.assertEqual(result.state, "DATA_UNAVAILABLE")
        self.assertEqual(result.contracts, ())

if __name__ == "__main__":
    unittest.main()
