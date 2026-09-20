"""Tests: internal consistency of the pricing code, plus the portfolio's numbers."""

import math

import pytest

import finmath as fm
from data import DASH_DAILY_CLOSES, IMPLIED_VOL_CASE, SENSITIVITY_CASE, WEEKLY_CLOSES


# --- Black--Scholes ---------------------------------------------------------

def test_norm_cdf_known_values():
    assert fm.norm_cdf(0.0) == pytest.approx(0.5)
    assert fm.norm_cdf(1.96) == pytest.approx(0.975, abs=1e-4)
    assert fm.norm_cdf(-3.0) + fm.norm_cdf(3.0) == pytest.approx(1.0)


def test_put_call_parity():
    """c - p = S0 - K e^{-rT}, the parity relation proved in Exercises 41-47."""
    S0, K, r, sigma, T = 42.0, 40.0, 0.10, 0.20, 0.5
    c = fm.call_price(S0, K, r, sigma, T)
    p = fm.put_price(S0, K, r, sigma, T)
    assert c - p == pytest.approx(S0 - K * math.exp(-r * T))
    assert fm.put_from_parity(c, S0, K, r, T) == pytest.approx(p)


def test_hull_textbook_case():
    """S0=42, K=40, r=10%, sigma=20%, T=0.5 gives c = 4.76, p = 0.81."""
    S0, K, r, sigma, T = 42.0, 40.0, 0.10, 0.20, 0.5
    assert fm.call_price(S0, K, r, sigma, T) == pytest.approx(4.76, abs=5e-3)
    assert fm.put_price(S0, K, r, sigma, T) == pytest.approx(0.81, abs=5e-3)


def test_call_price_increases_with_volatility():
    prices = [fm.call_price(100.0, 100.0, 0.05, s, 1.0) for s in (0.1, 0.2, 0.4, 0.8)]
    assert prices == sorted(prices)


def test_call_price_respects_no_arbitrage_bounds():
    """max(S0 - K e^{-rT}, 0) <= c <= S0, the bounds of Exercises 41-44."""
    S0, K, r, sigma, T = 100.0, 95.0, 0.04, 0.3, 1.5
    c = fm.call_price(S0, K, r, sigma, T)
    assert max(S0 - K * math.exp(-r * T), 0.0) <= c <= S0


def test_zero_volatility_or_maturity_is_rejected():
    with pytest.raises(ValueError):
        fm.call_price(100.0, 100.0, 0.05, 0.0, 1.0)
    with pytest.raises(ValueError):
        fm.call_price(100.0, 100.0, 0.05, 0.2, 0.0)


# --- Volatility -------------------------------------------------------------

def test_log_returns():
    assert fm.log_returns([100.0, 110.0]) == pytest.approx([math.log(1.1)])
    with pytest.raises(ValueError):
        fm.log_returns([100.0])


def test_constant_prices_have_zero_volatility():
    assert fm.historical_volatility([50.0] * 10, 252) == pytest.approx(0.0)


def test_implied_volatility_round_trips():
    S0, K, r, sigma, T = 100.0, 105.0, 0.03, 0.27, 0.75
    price = fm.call_price(S0, K, r, sigma, T)
    assert fm.implied_volatility(price, S0, K, r, T) == pytest.approx(sigma, abs=1e-8)


def test_implied_volatility_rejects_unattainable_price():
    with pytest.raises(ValueError):
        fm.implied_volatility(0.0, 100.0, 50.0, 0.05, 1.0)


# --- The portfolio's stated results -----------------------------------------

def test_exercise_1_weekly_historical_volatility():
    """PDF: sigma ~ 0.20794."""
    sigma = fm.historical_volatility(WEEKLY_CLOSES, fm.TRADING_WEEKS_PER_YEAR)
    assert sigma == pytest.approx(0.20794001923088867, abs=1e-12)


def test_exercise_2_implied_volatility():
    """PDF: sigma ~ 0.39644 backed out of a $2.50 call."""
    sigma = fm.implied_volatility(**IMPLIED_VOL_CASE)
    assert sigma == pytest.approx(0.3964355285962891, abs=1e-9)
    assert fm.call_price(sigma=sigma, **{k: v for k, v in IMPLIED_VOL_CASE.items()
                                         if k != "market_price"}) == pytest.approx(2.50)


def test_exercise_3_daily_series_annualizes_with_252():
    """The PDF scaled this daily series by sqrt(52); sqrt(252) is the right factor."""
    weekly_scaling = fm.historical_volatility(DASH_DAILY_CLOSES, fm.TRADING_WEEKS_PER_YEAR)
    daily_scaling = fm.historical_volatility(DASH_DAILY_CLOSES, fm.TRADING_DAYS_PER_YEAR)
    assert weekly_scaling == pytest.approx(0.09750432790261566, abs=1e-12)  # PDF's value
    assert daily_scaling == pytest.approx(0.2146458, abs=1e-6)
    assert daily_scaling / weekly_scaling == pytest.approx(math.sqrt(252 / 52))


def test_exercise_4_call_is_insensitive_to_volatility_at_short_maturity():
    """Deep in the money with T = 0.01, the call sits at S0 - K e^{-rT} until sigma is large."""
    intrinsic = SENSITIVITY_CASE["S0"] - SENSITIVITY_CASE["K"] * math.exp(
        -SENSITIVITY_CASE["r"] * SENSITIVITY_CASE["T"]
    )
    for sigma in (0.05, 0.25, 0.5, 1.0):
        assert fm.call_price(sigma=sigma, **SENSITIVITY_CASE) == pytest.approx(intrinsic, abs=1e-4)
    assert fm.call_price(sigma=5.0, **SENSITIVITY_CASE) == pytest.approx(51.333093, abs=1e-6)
