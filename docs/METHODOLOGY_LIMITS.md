# Methodology & Limitations

## Approach

The research followed a pre-registered protocol: define the hypothesis, validate on frozen walk-forward folds, and accept or reject based on pre-declared gates. No model was optimized after seeing test results. No evaluation gate was changed to make results appear successful.

## Known Limitations

1. **Data scope**: Only daily OHLCV (open, high, low, close, volume) was tested. No fundamental, macroeconomic, industry, analyst, or alternative data was incorporated.

2. **Market coverage**: A-shares only. Results do not generalize to other markets.

3. **Liquidity constraint**: Signal is concentrated in the lowest-liquidity quintile (median ADV ¥19M). The strategy has no demonstrated scalable capacity.

4. **Training horizon**: Training ends 2021; the 2022-2024 period was consumed as validation. A genuinely unseen forward test begins only from July 2026.

5. **Model family**: Only LightGBM (gradient-boosted trees) was tested. No neural networks, transformers, or ensemble-of-ensembles approaches were attempted.

6. **Factor family**: Only 20 technical price-volume factors were used (momentum, volatility, volume, reversal, skewness). No factor discovery, genetic programming, or alternative factor families were explored.

7. **Universe filter**: U50/U30 were the primary liquid-universe targets. Different liquidity thresholds might yield different results but were not optimized.

8. **Cost assumptions**: 31bp round-trip costs were used as the base scenario. Real-world costs vary by broker, trade size, and market conditions.

9. **Capacity assessment**: No formal market-impact model or capacity analysis was performed beyond ADV20 quintile attribution.

10. **Survivorship**: The point-in-time universe included delisted stocks but did not explicitly model delisting returns.

## What This Project Demonstrates

Despite these limitations, the project demonstrates a complete research methodology:
- Hypothesis formulation
- Leakage detection and correction
- Adversarial validation infrastructure
- Cost-aware portfolio evaluation
- Liquidity attribution
- Pre-registered stopping rules
- Honest rejection of a favored hypothesis
