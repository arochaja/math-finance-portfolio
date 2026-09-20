"""Black--Scholes pricing and volatility estimation.

A small, dependency-free implementation of the formulas derived in the
portfolio (``src/main.tex``): the Black--Scholes call and put prices from the
binomial limit, historical volatility from a series of closing prices, and
implied volatility recovered by numerical inversion.

Every function here is the direct computational counterpart of a derivation in
the PDF, so the numbers in :mod:`reproduce` match the ones written there.
"""

from __future__ import annotations

import math
from statistics import stdev
from typing import Sequence

TRADING_DAYS_PER_YEAR = 252
TRADING_WEEKS_PER_YEAR = 52


def norm_cdf(x: float) -> float:
    """Standard normal CDF, N(x), via the error function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def d1_d2(S0: float, K: float, r: float, sigma: float, T: float) -> tuple[float, float]:
    """The Black--Scholes d1 and d2.

    d1 = [ln(S0/K) + (r + sigma^2/2)T] / (sigma sqrt(T)),  d2 = d1 - sigma sqrt(T).
    """
    if sigma <= 0 or T <= 0:
        raise ValueError("sigma and T must be positive")
    d1 = (math.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    return d1, d1 - sigma * math.sqrt(T)


def call_price(S0: float, K: float, r: float, sigma: float, T: float) -> float:
    """Black--Scholes price of a European call: c = S0 N(d1) - K e^{-rT} N(d2)."""
    d1, d2 = d1_d2(S0, K, r, sigma, T)
    return S0 * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)


def put_price(S0: float, K: float, r: float, sigma: float, T: float) -> float:
    """Black--Scholes price of a European put: p = K e^{-rT} N(-d2) - S0 N(-d1)."""
    d1, d2 = d1_d2(S0, K, r, sigma, T)
    return K * math.exp(-r * T) * norm_cdf(-d2) - S0 * norm_cdf(-d1)


def put_from_parity(call: float, S0: float, K: float, r: float, T: float) -> float:
    """Put price implied by put--call parity: p = c + K e^{-rT} - S0."""
    return call + K * math.exp(-r * T) - S0


def log_returns(prices: Sequence[float]) -> list[float]:
    """Continuously compounded returns u_i = ln(S_i / S_{i-1})."""
    if len(prices) < 2:
        raise ValueError("need at least two prices")
    return [math.log(b / a) for a, b in zip(prices, prices[1:])]


def historical_volatility(prices: Sequence[float], periods_per_year: int) -> float:
    """Annualized volatility from closing prices.

    The sample standard deviation of the log returns (with the n-1 correction)
    scaled by sqrt(periods_per_year).
    """
    u = log_returns(prices)
    return stdev(u) * math.sqrt(periods_per_year)


def implied_volatility(
    market_price: float,
    S0: float,
    K: float,
    r: float,
    T: float,
    *,
    lo: float = 1e-6,
    hi: float = 5.0,
    tol: float = 1e-12,
    max_iter: int = 200,
) -> float:
    """Invert Black--Scholes for sigma by bisection.

    The call price is strictly increasing in sigma, so bisection on
    ``call_price(sigma) - market_price`` converges to the unique root.
    """
    f_lo = call_price(S0, K, r, lo, T) - market_price
    f_hi = call_price(S0, K, r, hi, T) - market_price
    if f_lo * f_hi > 0:
        raise ValueError(f"no implied volatility in [{lo}, {hi}] for price {market_price}")

    for _ in range(max_iter):
        mid = 0.5 * (lo + hi)
        f_mid = call_price(S0, K, r, mid, T) - market_price
        if abs(f_mid) < tol or (hi - lo) < tol:
            return mid
        if f_lo * f_mid < 0:
            hi = mid
        else:
            lo, f_lo = mid, f_mid
    return 0.5 * (lo + hi)


__all__ = [
    "norm_cdf",
    "d1_d2",
    "call_price",
    "put_price",
    "put_from_parity",
    "log_returns",
    "historical_volatility",
    "implied_volatility",
    "TRADING_DAYS_PER_YEAR",
    "TRADING_WEEKS_PER_YEAR",
]
