#!/usr/bin/env python3
"""Recompute the Volatility Exercises from the portfolio and check them.

Run from anywhere:

    python3 python/reproduce.py

Each row prints the value computed here next to the value written in the PDF.
Two rows disagree; the notes at the bottom explain why.
"""

from __future__ import annotations

import finmath as fm
from data import DASH_DAILY_CLOSES, IMPLIED_VOL_CASE, SENSITIVITY_CASE, WEEKLY_CLOSES

# Value printed in MATH_476_Portfolio.pdf, Volatility Exercises.
PORTFOLIO_VALUES = {
    "Ex 1  historical vol, 15 weekly closes": 0.20794001923088867,
    "Ex 2  implied vol from a $2.50 call": 0.3964355285962891,
    "Ex 3  historical vol, DASH daily closes": 0.09750432790261566,
    "Ex 4c call price at sigma = 5": 64.00670002074642,
}


def computed() -> dict[str, float]:
    return {
        "Ex 1  historical vol, 15 weekly closes": fm.historical_volatility(
            WEEKLY_CLOSES, fm.TRADING_WEEKS_PER_YEAR
        ),
        "Ex 2  implied vol from a $2.50 call": fm.implied_volatility(**IMPLIED_VOL_CASE),
        "Ex 3  historical vol, DASH daily closes": fm.historical_volatility(
            DASH_DAILY_CLOSES, fm.TRADING_DAYS_PER_YEAR
        ),
        "Ex 4c call price at sigma = 5": fm.call_price(sigma=5.0, **SENSITIVITY_CASE),
    }


NOTES = """
Notes on the two rows that differ
---------------------------------
Ex 3  The DASH series is daily, so annualizing multiplies the sample standard
      deviation by sqrt(252). The PDF used sqrt(52), the weekly factor carried
      over from Exercise 1, which understates sigma by sqrt(252/52) ~ 2.20.
      Weekly scaling reproduces the PDF's 0.0975 exactly:
          historical_volatility(DASH_DAILY_CLOSES, 52) = 0.09750
Ex 4c With S0 = 100, K = 50, r = 0.06, T = 0.01 and sigma = 5, the Black--Scholes
      call is 51.333. The PDF's 64.007 is the price at the same sigma but
      T ~ 0.0596, so the maturity used in the notebook was not the stated T = 0.01.
      The qualitative conclusion is unchanged: the call is near-worthless in
      volatility until sigma grows large, then rises steeply.
"""


def main() -> None:
    values = computed()
    width = max(len(label) for label in values)
    print(f"{'quantity':<{width}}  {'computed':>12}  {'in PDF':>12}   match")
    print("-" * (width + 42))
    for label, value in values.items():
        stated = PORTFOLIO_VALUES[label]
        agrees = abs(value - stated) <= 1e-9 * max(1.0, abs(stated))
        print(f"{label:<{width}}  {value:>12.6f}  {stated:>12.6f}   {'yes' if agrees else 'NO'}")

    S0, K, r, T = (SENSITIVITY_CASE[k] for k in ("S0", "K", "r", "T"))
    print(f"\nEx 4a/b  call price vs. volatility (S0={S0:.0f}, K={K:.0f}, r={r}, T={T}):")
    for sigma in (0.05, 0.25, 0.5, 1.0, 2.0, 5.0):
        print(f"    sigma = {sigma:<5} c = {fm.call_price(S0, K, r, sigma, T):.4f}")
    print(
        "  Flat across sigma in [0.05, 1]: with T = 0.01 the call is deep in the money\n"
        "  and worth essentially S0 - K e^{-rT}. Only much larger sigma moves it."
    )
    print(NOTES)


if __name__ == "__main__":
    main()
