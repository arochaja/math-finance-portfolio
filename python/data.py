"""Price series and parameters used by the Volatility Exercises in the portfolio."""

# Exercise 1 --- 15 consecutive weekly closes.
WEEKLY_CLOSES = [
    30.2, 32.0, 31.1, 30.1, 30.2, 30.3, 30.6, 33.0,
    32.9, 33.0, 33.5, 33.5, 33.7, 33.5, 33.2,
]

# Exercise 3 --- DASH daily closes, May 6 to June 6.
DASH_DAILY_CLOSES = [
    110.93, 112.00, 110.55, 110.25, 111.00, 110.47, 111.87, 113.35,
    111.15, 112.19, 113.02, 114.71, 117.81, 116.28, 115.19, 116.22,
    116.35, 115.37, 116.72, 113.00, 113.53, 114.48, 114.44, 116.48,
]

# Exercise 2 --- call quoted at $2.50, to be inverted for implied volatility.
IMPLIED_VOL_CASE = dict(market_price=2.50, S0=15.0, K=13.0, r=0.05, T=0.25)

# Exercise 4 --- call price as a function of volatility, very short maturity.
SENSITIVITY_CASE = dict(S0=100.0, K=50.0, r=0.06, T=0.01)
