# Experiment Ledger

Chronological record of evidence-backed milestones. Every row references an experiment ID in `evidence.json`.

| Phase | Experiment ID | Description | Status |
|-------|---------------|-------------|--------|
| V1 — Naive Pipeline | EXP_TARGET_SHIFT_01 | Target timing audit: discovered contemporaneous leakage (IC 0.94→0.10) | ❌ Invalid |
| V2 — Leak Detection | EXP_CROSSFIT_01 | Own-stock factor contamination audit (IC 0.76→0.12) | ❌ Invalid |
| V3 — Frozen Baseline | EXP_BASELINE_V43 | Clean pipeline with PIT universe, cross-fitting, rank normalization | ✅ Validated |
| V3 — Null Infrastructure | EXP_NULL_IID_01 | iid Gaussian null test; constant-label audit; permutation audit | ✅ Validated |
| DP-1 — Portfolio Diagnostics | EXP_DP1_PORTFOLIO | Cost-survival diagnostic: U100 +6.8% net, U50 negative | ⚠️ Observed |
| DP-1A — Liquidity Attribution | EXP_DP1A_QUINTILE | Quintile decomposition: 48% of holdings in Q1, within-Q1 selection +2.71% | ⚠️ Observed |
| Step 5 — Target Ablation | EXP_STEP5_ABLATION | RAW vs RESID: residualization improves U50 by 1.2% but cannot reach profitability | ❌ Rejected |
| MH-1R — Multi-Horizon | EXP_MH1R_HORIZON | 3-month and 6-month targets: all horizons produce negative U50 returns | ❌ Rejected |
| **FINAL** | — | **OHLCV-only development terminated. Branch closed.** | **Killed** |

## Decision Log

1. **Leak audit passed** → Clean pipeline established
2. **Statistical signal confirmed** → But concentrated in Q1
3. **Portfolio costs applied** → Liquid universes unprofitable
4. **Multi-horizon tested** → No improvement
5. **TERMINATE** → OHLCV-only cannot be a scalable core strategy
