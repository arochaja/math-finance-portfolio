# Portfolio of Financial Derivatives & Options

[![CI](https://github.com/arochaja/math-finance-portfolio/actions/workflows/ci.yml/badge.svg)](https://github.com/arochaja/math-finance-portfolio/actions/workflows/ci.yml)
[![LaTeX](https://img.shields.io/badge/built%20with-LaTeX-008080)](src/main.tex)
[![License: CC BY 4.0](https://img.shields.io/badge/license-CC%20BY%204.0-lightgrey)](LICENSE)

A worked portfolio of **115+ exercises** in mathematical finance — from forward-contract
payoffs through risk-neutral binomial pricing, a from-scratch derivation of the
Black–Scholes formula, volatility estimation, and linear programming.

Written in LaTeX with every solution shown in full: derivations, arbitrage arguments,
TikZ/pgfplots payoff diagrams, and numerical results.

📄 **[Read the full portfolio (74 pages, PDF)](MATH_476_Portfolio.pdf)**

---

## What's inside

| Topic | Exercises | Highlights |
|---|---|---|
| **Forwards & futures** | 1–20 | Long/short payoff diagrams, FX hedging with bid–ask spreads, margin and settlement |
| **Options fundamentals** | 21–40 | Call/put payoffs vs. profits, leverage comparisons, writing options, time value of money under discrete and continuous compounding |
| **No-arbitrage bounds** | 41–55 | Upper and lower bounds on option prices, put–call parity, early exercise of American puts, convexity in strike |
| **Trading strategies** | 48–56, 81 | Bull and bear spreads, butterflies, straddles, strangles — profit tables and expiry diagrams |
| **Binomial tree pricing** | 56–80 | Delta-hedged riskless portfolios, risk-neutral probability $p = \frac{e^{rT}-d}{u-d}$, one- and two-step trees, backward induction |
| **Black–Scholes from the binomial limit** | BSM 1–4 | Deriving $c = e^{-rT}(S_0U_1 - KU_2)$ and taking $n \to \infty$ to recover $c = S_0N(d_1) - Ke^{-rT}N(d_2)$ |
| **Volatility** | Vol 1–4 | Historical volatility from weekly and daily closes, implied volatility by numerical inversion, sensitivity of call price to $\sigma$ |
| **Linear programming** | 98–115 | Feasible-region graphing, conversion to standard form, the simplex method, and applied optimization problems |

### A few results worth skimming

- **Risk-neutral pricing from first principles** (Ex. 63–70) — construct the
  $\Delta$-hedged portfolio, show it is riskless regardless of the stock's move, and
  derive $f = e^{-rT}[pf_u + (1-p)f_d]$ before extending it to the two-step case.
- **Black–Scholes as a limit** (BSM Problems 1–4) — show the binomial summation's terms
  are nonzero exactly when $j > \frac{n}{2} - \frac{\ln(S_0/K)}{2\sigma\sqrt{T/n}}$, then
  prove $p(1-p) \to \tfrac14$ and apply the central limit theorem.
- **Volatility estimation** (Vol 1–3) — annualized $\sigma \approx 0.208$ from 15 weekly
  closes; implied $\sigma \approx 0.396$ backed out of a \$2.50 call; $\sigma \approx 0.098$
  from a month of DASH daily closes.

<p align="center">
  <img src="src/figures/tree-ex.png" width="45%" alt="Two-step binomial tree">
  <img src="src/figures/vol-vs-call-price.png" width="45%" alt="Call option price vs. volatility">
</p>

---

## The Python companion

The volatility exercises were originally computed in a Colab notebook. `python/`
reimplements that work as a small, dependency-free library so the results in the
PDF can be checked by anyone who clones the repo.

```bash
cd python
python3 reproduce.py          # recompute the Volatility Exercises
pip install pytest && pytest  # 14 tests
```

| File | What it holds |
|---|---|
| `finmath.py` | Black-Scholes call and put prices, `d1`/`d2`, put-call parity, log returns, historical volatility, implied volatility by bisection |
| `data.py` | The price series and parameters used by the Volatility Exercises |
| `reproduce.py` | Recomputes each stated result and prints it beside the value in the PDF |
| `test_finmath.py` | Parity, no-arbitrage bounds, monotonicity in sigma, implied-vol round-trip, and the portfolio's own figures |

`reproduce.py` output:

```
quantity                                     computed        in PDF   match
---------------------------------------------------------------------------
Ex 1  historical vol, 15 weekly closes       0.207940      0.207940   yes
Ex 2  implied vol from a $2.50 call          0.396436      0.396436   yes
Ex 3  historical vol, DASH daily closes      0.214646      0.097504   NO
Ex 4c call price at sigma = 5               51.333093     64.006700   NO
```

The two mismatches are errata in the written solutions, and the script explains
both: Exercise 3 annualizes a *daily* series, so the scaling factor is
$\sqrt{252}$ rather than the $\sqrt{52}$ carried over from Exercise 1; and the
Exercise 4(c) price corresponds to $T \approx 0.0596$, not the stated
$T = 0.01$, for which the correct price is \$51.33. Neither changes the
conclusion of the exercise.

---

## Repository layout

```
.
├── MATH_476_Portfolio.pdf   # compiled portfolio — start here
├── src/
│   ├── main.tex             # the portfolio source (~4,600 lines)
│   ├── course-notes.tex     # course notes / problem statements (reference)
│   └── figures/             # diagrams, plots, and computed output
├── python/                  # Black-Scholes and volatility code, with tests
└── LICENSE
```

## Building the PDF

Requires a TeX distribution with `pgfplots` and `tikz` (TeX Live, MacTeX, or MiKTeX).

```bash
cd src
pdflatex main.tex && pdflatex main.tex   # run twice to resolve references
```

The second pass is needed for cross-references and hyperlinks. `main.tex` sets
`\graphicspath{{figures/}{./}}`, so it must be compiled from inside `src/`.

> `course-notes.tex` is the instructor's source for the problem statements, kept for
> reference. It will not compile as-is — several of its figures were not distributed
> with the original materials.

---

## About

Coursework for **MATH 476 — Mathematical Finance**, Cal Poly San Luis Obispo.
Written by **Andres Rocha**.

Solutions are released under [CC BY 4.0](LICENSE). Problem statements belong to the
course instructor and are reproduced here only to make the solutions readable.
