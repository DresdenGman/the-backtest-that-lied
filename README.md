# The Backtest That Lied

**How I built, broke, and rejected an A-share machine-learning strategy — and what I learned by killing my own best result.**

A BRS high-school research project demonstrating that clean negative results are more valuable than profitable-looking lies.

## Central Conclusion

**The signal was real. The strategy was not.**

Daily OHLCV features contain genuine cross-sectional ranking information concentrated in the lowest-liquidity A-share quintile. However, this signal did not survive the transition to executable, cost-aware, liquidity-filtered portfolios in the U50/U30 universes. After six experimental phases and 200+ LightGBM fits, OHLCV-only development was formally terminated as a scalable core strategy.

Statistical predictability and economic investability are different things — and knowing when to stop is a research skill.

## The Three Collapses

1. **Statistical Illusion** — IC 0.94 → 0.10 after fixing contemporaneous target leakage (89% collapse)
2. **Economic Implementation** — Statistically significant rankings failed to produce positive absolute returns with real costs and execution timing
3. **Scalability** — Positive full-universe returns were driven entirely by the lowest-liquidity quintile; U50/U30 returns turned negative

## Live Demo

*Repository forthcoming*

## Repository Structure

```
the-backtest-that-lied/
├── index.html                  # Interactive evidence-driven landing page
├── README.md
├── LICENSE
├── CITATION.cff
├── .gitignore
├── data/
│   └── evidence.json           # Authoritative evidence layer
├── assets/
│   ├── css/three-collapses.css
│   └── js/
│       ├── evidence-loader.js  # Single shared data fetch
│       └── three-collapses.js  # Collapse visualization
├── scripts/
│   ├── validate_evidence.py    # Primary evidence validator
│   └── serve.py                # Local development server
├── tests/
│   └── test_evidence.py        # Unit tests for evidence integrity
├── docs/
│   ├── EVIDENCE_SCHEMA.md
│   ├── EXPERIMENT_LEDGER.md
│   ├── REPRODUCIBILITY.md
│   └── METHODOLOGY_LIMITS.md
└── .github/
    └── workflows/
        ├── validate.yml        # CI validation
        └── pages.yml           # GitHub Pages deployment
```

## Reproduce Locally

```bash
git clone https://github.com/a24300/the-backtest-that-lied.git
cd the-backtest-that-lied
python scripts/serve.py
# Open http://127.0.0.1:8000
```

No build step. No dependencies. No external network required.

## Validate Evidence

```bash
python scripts/validate_evidence.py
python -m unittest discover -s tests
```

## Research Methodology

- 3-fold walk-forward validation (2010-2024)
- 20-seed LightGBM ensemble
- Point-in-time universe (4,073 A-shares)
- Cross-sectional rank normalization
- Next-open portfolio execution
- 5 transaction-cost scenarios
- ADV20 liquidity quintile decomposition
- Newey-West inference + block bootstrap
- Pre-registered decision gates (no post-hoc optimization)

## What Is Reproducible

| Component | Status |
|-----------|--------|
| Evidence validation | ✅ Fully reproducible |
| Website rendering | ✅ Fully reproducible |
| All claims and metrics | ✅ Traceable to evidence.json |
| Original model training | ⚠️ Documented but requires RQAlpha bundle (not included) |

## What Is Not Reproducible

- Raw market data (requires RQAlpha bundle, ~3.3GB, not redistributable)
- Model training runs (require the bundle + proprietary Python environment)
- Prediction artifacts (stored locally, referenced by path in evidence.json)

## Key Limitations

- Signal concentrated in lowest-liquidity quintile (median ADV ¥19M)
- No fundamental, industry, or alternative data tested
- Training period ends 2021; forward test from July 2026 is not yet available
- Maximum drawdowns exceeded 25% threshold in liquid universes
- Transaction costs (31bp) and next-open execution reduced returns substantially

## Project Status

**Terminated.** The OHLCV-only hypothesis branch is closed as a scalable core strategy. A frozen Q1 research sleeve is maintained for forward observation only — no further historical optimization or strategy modifications.

## Citation

*Forthcoming*

## License

Code: MIT License. Research conclusions and methodology are freely available for academic use. This repository does not contain or redistribute third-party market data.
