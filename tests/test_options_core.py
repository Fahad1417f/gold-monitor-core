import unittest
from core.options.analyzer import analyze_contract
from core.options.greeks import black_scholes_greeks
from core.options.models import OptionContract, UnderlyingSignal
from core.options.payoff import target_rr
def contract(**overrides):
    data = dict(symbol="TEST-100-C", underlying="TEST", option_type="CALL", strike=100.0, expiration="2026-10-30", dte=31.0, bid=4.8, ask=5.2, volume=100.0, open_interest=500.0, implied_volatility=0.30, delta=0.55, premium=5.0)
    data.update(overrides)
    return OptionContract(**data)
class OptionsCoreTests(unittest.TestCase):
    def test_black_scholes(self):
        g = black_scholes_greeks(100, 100, 30/365, 0.05, 0.30, "CALL")
        self.assertGreater(g.price, 0); self.assertGreater(g.delta, 0); self.assertGreater(g.gamma, 0); self.assertGreater(g.vega, 0)
    def test_target_rr(self):
        reward, loss, rr = target_rr(contract(), 115)
        self.assertEqual(loss, 5.0); self.assertEqual(reward, 10.0); self.assertEqual(rr, 2.0)
    def test_confirmed(self):
        result = analyze_contract(UnderlyingSignal("TEST", "BULLISH", "CONFIRMED", 5), contract(), target_underlying=115)
        self.assertEqual(result.state, "CONFIRMED"); self.assertEqual(result.target_rr, 2.0)
    def test_waits_for_kfoo(self):
        result = analyze_contract(UnderlyingSignal("TEST", "BULLISH", "WAITING_FOR_EVIDENCE", 5), contract(), target_underlying=115)
        self.assertEqual(result.state, "WAITING_FOR_EVIDENCE")
    def test_rejects_wrong_type(self):
        result = analyze_contract(UnderlyingSignal("TEST", "BULLISH", "CONFIRMED", 5), contract(option_type="PUT"), target_underlying=115)
        self.assertEqual(result.state, "REJECTED"); self.assertIn("OPTION_TYPE_MISMATCH", result.reasons)
    def test_rejects_wide_spread(self):
        result = analyze_contract(UnderlyingSignal("TEST", "BULLISH", "CONFIRMED", 5), contract(bid=3, ask=7), target_underlying=115)
        self.assertEqual(result.state, "REJECTED"); self.assertIn("WIDE_BID_ASK", result.reasons)
    def test_rejects_zero_premium(self):
        result = analyze_contract(UnderlyingSignal("TEST", "BULLISH", "CONFIRMED", 5), contract(premium=0), target_underlying=115)
        self.assertEqual(result.state, "REJECTED"); self.assertIn("PREMIUM_UNAVAILABLE", result.reasons)
if __name__ == "__main__": unittest.main()
