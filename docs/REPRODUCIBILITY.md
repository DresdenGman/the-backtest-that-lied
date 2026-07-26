# Reproducibility

## Level 1: Evidence Verification ✅ Fully Reproducible

```bash
git clone https://github.com/a24300/the-backtest-that-lied.git
cd the-backtest-that-lied
python scripts/validate_evidence.py
python -m unittest discover -s tests
```

All evidence claims in `evidence.json` are structurally validated and reference-integrity-checked.

## Level 2: Website Rendering ✅ Fully Reproducible

```bash
python scripts/serve.py
# Open http://127.0.0.1:8000
```

Zero build step. Zero dependencies. Pure HTML/CSS/JS loading from evidence.json via fetch().

## Level 3: Model Training ⚠️ Documented, Not Fully Reproducible

The original model training requires:
- RQAlpha market-data bundle (~3.3GB, not redistributable)
- Python 3.11 environment with LightGBM, pandas, numpy, scikit-learn
- 200+ LightGBM fits across 3 folds × 20 seeds × multiple experimental phases

The evidence.json file is the authoritative publication layer — it contains all validated results with experiment IDs, artifact paths, and protocol documentation. It does not replace raw experiment artifacts but provides a complete, validatable record of what was tested and what was concluded.

## What Is Explicitly Not Claimed

- End-to-end reproducibility from raw market data
- A profitable trading strategy
- A deployable investment system
- General A-share market predictions
