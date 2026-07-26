#!/usr/bin/env python3
"""generate_sections.py — Rebuild all report .tex files from evidence.json."""
import json, os, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(REPO, 'data', 'evidence.json')) as f:
    e = json.load(f)
m = e['metrics']
F = lambda k: m[k]['value']

def P(k): return f'{F(k)*100:+.1f}\\%'
def I(k): return f'{F(k):.3f}'
def S(k): return f'{F(k):+.2f}'

coll_pct = int((F("target_leak_before_ic") - F("target_leak_after_ic")) / abs(F("target_leak_before_ic")) * 100)
abs_d = F("target_leak_before_ic") - F("target_leak_after_ic")

sec = os.path.join(REPO, 'report', 'sections')
app = os.path.join(REPO, 'report', 'appendix')
W = lambda n,c: open(os.path.join(sec, n), 'w').write(c)
WA = lambda n,c: open(os.path.join(app, n), 'w').write(c)

W('01_abstract.tex', f"""\\section{{Abstract}}
A near-perfect cross-sectional prediction signal---monthly rank IC {I("target_leak_before_ic")} collapsed to {I("target_leak_after_ic")} after four detected data leakages were corrected.
The surviving signal, mean OOS IC {I("frozen_baseline_mean_ic")} with Newey--West $t = {F("frozen_baseline_nw_t6"):.1f}$, represented genuine low-liquidity stock-selection ability.
With executable portfolios and transaction costs, the strategy produced negative absolute returns in the liquid U50 universe (net annual {P("u50_resid_net_annual")}, max drawdown {P("u50_max_drawdown")}).
The OHLCV-only hypothesis was formally terminated. The primary contribution is methodological.
""")

W('02_introduction.tex', f"""\\section{{Introduction}}
\\begin{{quote}}\\textit{{A model can predict returns and still fail as a strategy.}}\\end{{quote}}
The initial result: IC {I("target_leak_before_ic")} across 96 consecutive OOS months collapsed by {coll_pct}\\% after four leakages.
Retained signal: mean OOS IC {I("frozen_baseline_mean_ic")}, Newey--West $t = {F("frozen_baseline_nw_t6"):.1f}$.
\\begin{{enumerate}}[label=(\\arabic*)]
    \\item Cross-sectional predictability: IC {I("frozen_baseline_mean_ic")} survived null infrastructure.
    \\item Signal concentrated in illiquid stocks: {P("q1_share_of_u100_holdings")} of holdings in Q1. Within-Q1: {P("q1_within_excess")} monthly excess.
    \\item Liquid universes unprofitable: U50 net {P("u50_resid_net_annual")}, max DD {P("u50_max_drawdown")}.
    \\item Longer horizons failed: H3 {P("h3_u50_net_annual")}, H6 {P("h6_u50_net_annual")} net annual.
\\end{{enumerate}}
The OHLCV-only strategy was terminated. Offered as a research methodology case study.
""")

W('05_the_three_collapses.tex', f"""\\section{{The Three Collapses}}
\\subsection{{Collapse I: Statistical Illusion}}
Initial belief: 20 factors + LightGBM could predict returns with IC {I("target_leak_before_ic")}.
Detection: Date-shift scan peaked at $k=0$, not $k=+1$.
Correction: IC collapsed {I("target_leak_before_ic")} $\\to$ {I("target_leak_after_ic")}.
Interpretation: {coll_pct}\\% of apparent predictive power was mechanical illusion (absolute decline: {abs_d:.2f} IC points).

\\subsection{{Collapse II: Economic Implementation}}
Initial belief: IC {I("frozen_baseline_mean_ic")} should produce positive portfolio returns.
Results: U50 executable (31bp costs): net {P("u50_resid_net_annual")}, DD {P("u50_max_drawdown")}. Benchmark: {P("u50_ew_bench_annual")}.
Interpretation: Statistical predictability $\\neq$ economic investability.

\\subsection{{Collapse III: Scalability}}
Initial belief: Full universe profitable (U100 net {P("u100_raw_net_annual")}).
Finding: {P("q1_share_of_u100_holdings")} of holdings in Q1. Within-Q1: {P("q1_within_excess")} monthly excess.
Interpretation: The alpha existed where capacity was severely constrained.
""")

W('06_portfolio_implementation.tex', f"""\\section{{Portfolio Implementation}}
\\begin{{table}}[htbp]\\centering
\\caption{{Portfolio performance under base cost scenario (31bp round-trip).}}\\label{{tab:portfolio}}
\\begin{{tabular}}{{lcccc}}\\toprule
\\textbf{{Portfolio}} & \\textbf{{Net Annual}} & \\textbf{{Sharpe}} & \\textbf{{Max DD}} & \\textbf{{Excess}} \\\\midrule
U100 RAW (base31) & {P("u100_raw_net_annual")} & {S("u100_raw_sharpe")} & {P("u100_raw_max_dd")} & {P("u100_raw_excess_annual")} \\\\
U50 RESID (base31) & {P("u50_resid_net_annual")} & {S("u50_resid_sharpe")} & {P("u50_max_drawdown")} & {P("u50_resid_excess_annual")} \\\\
U50 EW benchmark & {P("u50_ew_bench_annual")} & {S("u50_ew_sharpe")} & --- & --- \\\\bottomrule
\\end{{tabular}}\\end{{table}}
U50 RESID generates {P("u50_resid_excess_annual")} annual excess over the benchmark ({P("u50_ew_bench_annual")}). Positive excess over a poor benchmark is not skill.
""")

W('07_liquidity_attribution.tex', f"""\\section{{Liquidity Attribution}}
\\begin{{table}}[htbp]\\centering
\\caption{{Liquidity quintile composition.}}\\label{{tab:quintile}}
\\begin{{tabular}}{{lccc}}\\toprule
\\textbf{{Quintile}} & \\textbf{{Median ADV (M\\textyen)}} & \\textbf{{\\% Holdings}} & \\textbf{{Net Annual}} \\\\midrule
Q1 (lowest) & 19 & {P("q1_share_of_u100_holdings")} & +10.4\\% \\\\
Q2 & 41 & 25.8\\% & +3.9\\% \\\\
Q3 & 75 & 14.0\\% & -0.6\\% \\\\
Q4 & 145 & 7.8\\% & -3.5\\% \\\\
Q5 (highest) & 386 & 4.2\\% & -2.6\\% \\\\bottomrule
\\end{{tabular}}\\end{{table}}
Within-Q1 selection: {P("q1_within_excess")} per month. The signal was concentrated in the lowest-liquidity stocks and was severely capacity-constrained. Maximum feasible capacity was not fully quantified.
""")

W('08_residual_and_horizon.tex', f"""\\section{{Residual and Horizon Tests}}
\\subsection{{Cross-Fitted Residual Target (RESID)}}
Own-stock contamination audit: IC collapsed from {I("crossfit_ic_before")} to {I("crossfit_ic_after")} after cross-fitting.
Residualization improved U50 marginally (net {P("u50_resid_net_annual")}, DD {P("u50_max_drawdown")}) but could not reach profitability.
\\subsection{{Multi-Horizon Targets (H3 and H6)}}
H3 U50: {P("h3_u50_net_annual")} annual. H6 U50: {P("h6_u50_net_annual")} annual. Multi-horizon targeting does not rescue OHLCV-only scalability.
""")

W('09_discussion.tex', f"""\\section{{The Signal Was Real. The Strategy Was Not.}}
\\begin{{table}}[htbp]\\centering
\\caption{{Decision gates.}}\\label{{tab:gates}}
\\begin{{tabular}}{{lcc}}\\toprule
\\textbf{{Criterion}} & \\textbf{{Result}} & \\textbf{{Gate}} \\\\midrule
Predictive ranking & Passed & IC $> 0$, NW $t > 2$ \\\\
Time-aware significance & Passed & Bootstrap CI excludes 0 \\\\
Within-Q1 selection & Passed & Excess $> 0$ \\\\
Positive U50 return & Failed & Net $< 0$ \\\\
Acceptable drawdown & Failed & DD $> 25\\%$ \\\\
Scalable capacity & Failed & Q1 holds {P("q1_share_of_u100_holdings")} \\\\midrule
\\textbf{{Decision}} & \\textbf{{TERMINATED}} & OHLCV branch closed \\\\bottomrule
\\end{{tabular}}\\end{{table}}
Frozen baseline: IC {I("frozen_baseline_mean_ic")}, NW $t = {F("frozen_baseline_nw_t6"):.1f}$. Pre-registered gates prevented post-hoc optimization. Termination was the only honest decision.
""")

W('11_conclusion.tex', f"""\\section{{Conclusion}}
OHLCV features contain genuine ranking information: IC {I("frozen_baseline_mean_ic")}, NW $t = {F("frozen_baseline_nw_t6"):.1f}$, within-Q1 selection {P("q1_within_excess")} monthly excess.
The signal did not survive executable portfolios: U50 net {P("u50_resid_net_annual")}, DD {P("u50_max_drawdown")}. Multi-horizon: H3 {P("h3_u50_net_annual")}, H6 {P("h6_u50_net_annual")}.
The contribution is a demonstration that clean negative results are more valuable than profitable-looking lies.
""")

WA('evidence_map.tex', f"""\\section{{Evidence Map}}
Key metrics (of {len(m)} total):
\\begin{{itemize}}
    \\item \\texttt{{target\\_leak\\_before\\_ic}}: IC {I("target_leak_before_ic")} $\\to$ \\texttt{{EXP\\_TARGET\\_SHIFT\\_01}}
    \\item \\texttt{{target\\_leak\\_after\\_ic}}: IC {I("target_leak_after_ic")} $\\to$ \\texttt{{EXP\\_TARGET\\_SHIFT\\_01}}
    \\item \\texttt{{frozen\\_baseline\\_mean\\_ic}}: IC {I("frozen_baseline_mean_ic")} $\\to$ \\texttt{{EXP\\_BASELINE\\_V43}}
    \\item \\texttt{{u100\\_raw\\_net\\_annual}}: {P("u100_raw_net_annual")} $\\to$ \\texttt{{EXP\\_DP1\\_PORTFOLIO}}
    \\item \\texttt{{u50\\_resid\\_net\\_annual}}: {P("u50_resid_net_annual")} $\\to$ \\texttt{{EXP\\_STEP5\\_ABLATION}}
    \\item \\texttt{{q1\\_within\\_excess}}: {P("q1_within_excess")} $\\to$ \\texttt{{EXP\\_DP1A\\_QUINTILE}}
    \\item \\texttt{{h3\\_u50\\_net\\_annual}}: {P("h3_u50_net_annual")} $\\to$ \\texttt{{EXP\\_MH1R\\_HORIZON}}
\\end{{itemize}}
""")

WA('experiment_ledger.tex', f"""\\section{{Experiment Ledger}}
\\begin{{enumerate}}
    \\item \\textbf{{Target Timing}}: IC {I("target_leak_before_ic")} $\\to$ {I("target_leak_after_ic")} ({coll_pct}\\% collapse). Invalid $\\to$ Validated.
    \\item \\textbf{{Cross-Fit Audit}}: IC {I("crossfit_ic_before")} $\\to$ {I("crossfit_ic_after")}. Invalid $\\to$ Validated.
    \\item \\textbf{{Frozen Baseline}}: Mean OOS IC {I("frozen_baseline_mean_ic")}, NW $t = {F("frozen_baseline_nw_t6"):.1f}$. Validated.
    \\item \\textbf{{Null Infrastructure}}: Permutation correlation $\\approx$ 0. Validated.
    \\item \\textbf{{Portfolio Diagnostics}}: U100 {P("u100_raw_net_annual")}, U50 {P("u50_resid_net_annual")}. Q1-driven.
    \\item \\textbf{{Residual Ablation}}: Cannot reach profitability. Rejected.
    \\item \\textbf{{Multi-Horizon}}: H3 {P("h3_u50_net_annual")}, H6 {P("h6_u50_net_annual")} U50 net. Rejected.
    \\item \\textbf{{Termination}}: OHLCV-only core strategy closed. Recorded.
\\end{{enumerate}}
""")

print(f'Generated {9} sections + 2 appendices')
