import unittest
from decimal import Decimal

from core.direction.dollar_wave_gold_impact import (
    classify_dollar_change,
    dollar_wave_gold_impact,
)


class DollarWaveGoldImpactTests(unittest.TestCase):
    def test_documented_boundaries(self):
        self.assertEqual(classify_dollar_change("0.001"), "WEAK")
        self.assertEqual(classify_dollar_change("0.005"), "WEAK")
        self.assertEqual(classify_dollar_change("0.006"), "MEDIUM")
        self.assertEqual(classify_dollar_change("0.009"), "MEDIUM")
        self.assertEqual(classify_dollar_change("0.01"), "STRONG")
        self.assertEqual(classify_dollar_change("0.09"), "STRONG")
        self.assertEqual(classify_dollar_change("0.1"), "VERY_STRONG")
        self.assertEqual(classify_dollar_change("0.9"), "VERY_STRONG")

    def test_up_wave_is_negative_for_gold(self):
        result = dollar_wave_gold_impact(
            "UP",
            "0.006",
            market="GOLD",
            dxy_value="100.283",
            timeframe="3m",
        )
        self.assertEqual(result.state, "OBSERVED_RULE")
        self.assertEqual(result.market, "GOLD")
        self.assertEqual(result.wave_direction, "UP")
        self.assertEqual(result.strength, "MEDIUM")
        self.assertEqual(result.gold_effect, "NEGATIVE")
        self.assertEqual(result.change_value, Decimal("0.006"))
        self.assertEqual(result.dxy_value, Decimal("100.283"))
        self.assertEqual(result.timeframe, "3m")

    def test_xauusd_alias_is_allowed(self):
        result = dollar_wave_gold_impact("DOWN", "0.01", market="XAUUSD")
        self.assertEqual(result.state, "OBSERVED_RULE")
        self.assertEqual(result.market, "XAUUSD")
        self.assertEqual(result.gold_effect, "POSITIVE")

    def test_non_gold_market_fails_closed(self):
        for market in ("BTCUSDT", "ETHUSDT", "CRYPTO", "FOREX", "SILVER"):
            result = dollar_wave_gold_impact("UP", "0.006", market=market)
            self.assertEqual(result.state, "DATA_UNAVAILABLE")
            self.assertIsNone(result.gold_effect)

    def test_down_wave_is_positive_for_gold(self):
        result = dollar_wave_gold_impact("DOWN", "0.01", market="GOLD")
        self.assertEqual(result.state, "OBSERVED_RULE")
        self.assertEqual(result.gold_effect, "POSITIVE")
        self.assertEqual(result.strength, "STRONG")

    def test_invalid_values_fail_closed(self):
        for value in (None, "0", "0.0009", "0.91", "-0.1", "not-a-number"):
            self.assertIsNone(classify_dollar_change(value))
            result = dollar_wave_gold_impact("UP", value, market="GOLD")
            self.assertEqual(result.state, "DATA_UNAVAILABLE")
            self.assertIsNone(result.gold_effect)

    def test_invalid_direction_fails_closed(self):
        result = dollar_wave_gold_impact("FLAT", "0.006", market="GOLD")
        self.assertEqual(result.state, "DATA_UNAVAILABLE")
        self.assertIsNone(result.gold_effect)

    def test_dxy_price_is_separate_from_change_value(self):
        result = dollar_wave_gold_impact(
            "UP",
            "0.006",
            market="GOLD",
            dxy_value="100.283",
            timeframe="3m",
        )
        payload = result.to_dict()
        self.assertEqual(payload["change_value"], "0.006")
        self.assertEqual(payload["dxy_value"], "100.283")


if __name__ == "__main__":
    unittest.main()
