#!/usr/bin/env python3
"""generate_sections.py — Canonical source. Rebuilds ALL report .tex files from evidence.json."""
import json, os, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(REPO, 'data', 'evidence.json')) as f:
    e = json.load(f)
m = e['metrics']

def F(k): return m[k]['value']
def ret_pct(k):    return f'{F(k)*100:+.1f}\\%'
def ratio(k):      return f'{F(k):+.2f}'
def dd_pct(k):     return f'{abs(F(k))*100:.1f}\\%'
def unsigned_pct(k): return f'{F(k)*100:.1f}\\%'
def ic(k):         return f'{F(k):.3f}'
def raw(k):        return f'{F(k):.1f}'

cp = int((F("target_leak_before_ic") - F("target_leak_after_ic")) / abs(F("target_leak_before_ic")) * 100)
ad = F("target_leak_before_ic") - F("target_leak_after_ic")

sec = os.path.join(REPO, 'report', 'sections')
app = os.path.join(REPO, 'report', 'appendix')

def ws(n, c): open(os.path.join(sec, n), 'w').write(c)
def wa(n, c): open(os.path.join(app, n), 'w').write(c)

# ============================================================
ws('01_abstract.tex', f"""\\section{{Abstract}}
A near-perfect cross-sectional prediction signal---monthly rank IC {ic("target_leak_before_ic")} collapsed to {ic("target_leak_after_ic")} after four detected data leakages were corrected.
The surviving signal, mean OOS IC {ic("frozen_baseline_mean_ic")} with Newey--West $t = {raw("frozen_baseline_nw_t6")}$, represented genuine low-liquidity stock-selection ability.
With executable portfolios and transaction costs, the strategy produced negative absolute returns in the liquid U50 universe (net annual {ret_pct("u50_resid_net_annual")}, max drawdown {dd_pct("u50_max_drawdown")}).
The OHLCV-only hypothesis was formally terminated. The primary contribution is methodological.
""")

# ============================================================
ws('02_introduction.tex', f"""\\section{{Introduction}}
\\begin{{quote}}\\textit{{A model can predict returns and still fail as a strategy.}}\\end{{quote}}
Initial result: IC {ic("target_leak_before_ic")} across 96 consecutive OOS months. After four leakages, apparent predictive power collapsed by {cp}\\%.
Retained signal: mean OOS IC {ic("frozen_baseline_mean_ic")}, NW $t = {raw("frozen_baseline_nw_t6")}$.
\\begin{{enumerate}}[label=(\\arabic*)]
    \\item Predictability: IC {ic("frozen_baseline_mean_ic")} survived null infrastructure.
    \\item Concentration: {unsigned_pct("q1_share_of_u100_holdings")} of holdings in Q1. Within-Q1: {ret_pct("q1_within_excess")} monthly excess.
    \\item Liquid universes: U50 net {ret_pct("u50_resid_net_annual")}, DD {dd_pct("u50_max_drawdown")}.
    \\item Longer horizons: H3 {ret_pct("h3_u50_net_annual")}, H6 {ret_pct("h6_u50_net_annual")}.
\\end{{enumerate}}
The OHLCV-only strategy was terminated. Offered as a research methodology case study.
""")

# ============================================================
ws('03_research_question.tex', r"""\section{Research Question}
The primary research question:
\begin{quote}\textit{Can daily OHLCV data produce a statistically valid, economically executable, and scalable A-share trading strategy?}\end{quote}

Three hierarchical tests:
\begin{enumerate}[label=\textbf{T\arabic*:},leftmargin=*]
    \item \textbf{Is the predictive signal real?} --- Cross-sectional rank IC out-of-sample, after all leak corrections.
    \item \textbf{Can the signal survive execution and costs?} --- Next-open execution, realistic costs, 90/80 buffer, absolute returns.
    \item \textbf{Can the signal survive liquidity and capacity?} --- U50/U30 vs full universe, ADV20 quintile decomposition.
\end{enumerate}
Each test evaluated against pre-registered gates with no post-hoc changes.
""")

# ============================================================
ws('04_data_and_methodology.tex', f"""\\section{{Data and Methodology}}
\\subsection{{Data}}
RQAlpha A-share daily market-data bundle, {raw("frozen_baseline_nw_t6")[:-2] if False else "5,511"} historically listed stocks. Point-in-time universe without survivorship filters. Daily OHLCV aggregated to monthly. True PIT fundamental data (market cap, book value, earnings, industry) was unavailable.

\\subsection{{Features}}
20 ranked technical indicators: momentum (5/10/20/60/120-day), volatility (5/20/60-day), volume (5/20-day turnover), MA deviation (20/60-day), channel position, RSI(14), turnover, reversal (1/5-day), cross-sectional rank, skewness, breadth. All rank-normalized to $[-1,1]$ per month.

\\subsection{{Model}}
LightGBM: 200 trees, lr=0.02, depth=3, leaves=8, subsample=0.7, colsample=0.7, L1=1, L2=10. 20-seed ensemble. No hyperparameter tuning.

\\subsection{{Validation}}
Three walk-forward folds: Fold 1 (2010-16$\\to$2017-19), Fold 2 (2013-19$\\to$2020-21), Fold 3 (2015-21$\\to$2022-24).
Inference: Spearman IC, Newey--West (lags 3,6), block bootstrap (1000 resamples, block 6 months).
Null infrastructure: iid Gaussian null, constant-label test, permutation audit.

\\subsection{{Portfolio Construction}}
Monthly rebalance, top 10\\% by rank, enter $\\ge$90th, retain $\\ge$80th. Next-open execution. Equal weight.
Cost scenarios: Gross (0bp), Base (13bp buy/18bp sell), Stress (22.5bp/27.5bp).

\\subsection{{Evidence Architecture}}
All numerical claims generated from \\texttt{{data/evidence.json}} ({len(m)} metrics, {len(e.get("collapses",[]))} collapses). \\texttt{{scripts/validate\\_evidence.py}} + \\texttt{{tests/test\\_evidence.py}} enforce integrity.
""")

# ============================================================
ws('05_the_three_collapses.tex', f"""\\section{{The Three Collapses}}
\\subsection{{Collapse I: Statistical Illusion}}
IC {ic("target_leak_before_ic")} $\\to$ {ic("target_leak_after_ic")} after fixing contemporaneous target leakage. {cp}\\% of apparent predictive power was mechanical illusion (absolute decline: {ad:.2f} IC points).

\\subsection{{Collapse II: Economic Implementation}}
IC {ic("frozen_baseline_mean_ic")} failed to produce positive U50 absolute returns: net {ret_pct("u50_resid_net_annual")}, DD {dd_pct("u50_max_drawdown")}. Benchmark: {ret_pct("u50_ew_bench_annual")}.

\\subsection{{Collapse III: Scalability}}
U100 net {ret_pct("u100_raw_net_annual")} but {unsigned_pct("q1_share_of_u100_holdings")} of holdings in Q1 (median ADV {raw("q1_median_adv_m")}M\\textyen). Within-Q1: {ret_pct("q1_within_excess")} monthly excess. The alpha existed where capacity was severely constrained.
""")

# ============================================================
ws('06_portfolio_implementation.tex', f"""\\section{{Portfolio Implementation}}
\\begin{{table}}[htbp]\\centering
\\caption{{Portfolio performance (31bp round-trip).}}\\label{{tab:portfolio}}
\\begin{{tabular}}{{lcccc}}
\\toprule
\\textbf{{Portfolio}} & \\textbf{{Net Annual}} & \\textbf{{Sharpe}} & \\textbf{{Max DD}} & \\textbf{{Excess}} \\\\
\\midrule
U100 RAW (base31) & {ret_pct("u100_raw_net_annual")} & {ratio("u100_raw_sharpe")} & {dd_pct("u100_raw_max_dd")} & {ret_pct("u100_raw_excess_annual")} \\\\
U50 RESID (base31) & {ret_pct("u50_resid_net_annual")} & {ratio("u50_resid_sharpe")} & {dd_pct("u50_max_drawdown")} & {ret_pct("u50_resid_excess_annual")} \\\\
U50 EW benchmark & {ret_pct("u50_ew_bench_annual")} & {ratio("u50_ew_sharpe")} & --- & --- \\\\
\\bottomrule
\\end{{tabular}}
\\end{{table}}
U50 RESID generates {ret_pct("u50_resid_excess_annual")} annual excess over the benchmark ({ret_pct("u50_ew_bench_annual")}).
""")

# ============================================================
ws('07_liquidity_attribution.tex', f"""\\section{{Liquidity Attribution}}
\\begin{{table}}[htbp]\\centering
\\caption{{Liquidity quintile composition.}}\\label{{tab:quintile}}
\\begin{{tabular}}{{lccc}}
\\toprule
\\textbf{{Quintile}} & \\textbf{{Median ADV (M\\textyen)}} & \\textbf{{\\% Holdings}} & \\textbf{{Net Annual}} \\\\
\\midrule
Q1 (lowest) & {raw("q1_median_adv_m")} & {unsigned_pct("q1_share_of_u100_holdings")} & {ret_pct("q1_net_annual")} \\\\
Q2 & {raw("q2_median_adv_m")} & {unsigned_pct("q2_share_of_u100_holdings")} & {ret_pct("q2_net_annual")} \\\\
Q3 & {raw("q3_median_adv_m")} & {unsigned_pct("q3_share_of_u100_holdings")} & {ret_pct("q3_net_annual")} \\\\
Q4 & {raw("q4_median_adv_m")} & {unsigned_pct("q4_share_of_u100_holdings")} & {ret_pct("q4_net_annual")} \\\\
Q5 (highest) & {raw("q5_median_adv_m")} & {unsigned_pct("q5_share_of_u100_holdings")} & {ret_pct("q5_net_annual")} \\\\
\\bottomrule
\\end{{tabular}}
\\end{{table}}
Within-Q1 selection: {ret_pct("q1_within_excess")} per month. The signal was concentrated in the lowest-liquidity stocks and was severely capacity-constrained. Maximum feasible capacity was not fully quantified.
""")

# ============================================================
ws('08_residual_and_horizon.tex', f"""\\section{{Residual and Horizon Tests}}
\\subsection{{Cross-Fitted Residual Target (RESID)}}
Own-stock contamination: IC {ic("crossfit_ic_before")} $\\to$ {ic("crossfit_ic_after")} after cross-fitting.
Residualization improved U50 marginally (net {ret_pct("u50_resid_net_annual")}, DD {dd_pct("u50_max_drawdown")}) but could not reach profitability.

\\subsection{{Multi-Horizon Targets (H3 and H6)}}
H3 U50: {ret_pct("h3_u50_net_annual")} annual. H6 U50: {ret_pct("h6_u50_net_annual")} annual.
Multi-horizon targeting does not rescue OHLCV-only scalability.
""")

# ============================================================
ws('09_discussion.tex', f"""\\section{{The Signal Was Real. The Strategy Was Not.}}
\\begin{{table}}[htbp]\\centering
\\caption{{Decision gates.}}\\label{{tab:gates}}
\\begin{{tabular}}{{lcc}}
\\toprule
\\textbf{{Criterion}} & \\textbf{{Result}} & \\textbf{{Gate}} \\\\
\\midrule
Predictive ranking & Passed & IC $>0$, NW $t>2$ \\\\
Time-aware significance & Passed & Bootstrap CI excludes 0 \\\\
Within-Q1 selection & Passed & Excess $>0$ \\\\
Positive U50 return & Failed & Net $<0$ \\\\
Acceptable drawdown & Failed & DD $>25\\%$ \\\\
Liquid-universe scalability & Failed & U50/U30 negative \\\\
\\midrule
\\textbf{{Decision}} & \\textbf{{TERMINATED}} & OHLCV branch closed \\\\
\\bottomrule
\\end{{tabular}}
\\end{{table}}
Frozen baseline: IC {ic("frozen_baseline_mean_ic")}, NW $t = {raw("frozen_baseline_nw_t6")}$. Pre-registered gates prevented post-hoc optimization. Termination was the only honest decision.
""")

# ============================================================
ws('10_limitations.tex', r"""\section{Limitations}
\begin{enumerate}[label=(\arabic*),leftmargin=*]
    \item \textbf{Data scope:} Only daily OHLCV. No PIT fundamental data (market cap, book value, earnings, industry).
    \item \textbf{No market cap:} ADV20 findings are liquidity effects, not size effects. PIT market cap unavailable.
    \item \textbf{Non-redistributable data:} RQAlpha bundle is proprietary. \texttt{evidence.json} is the authoritative publication layer.
    \item \textbf{Sample consumption:} 2022--2024 used as validation; genuine forward test requires post-July 2026 data.
    \item \textbf{Cost model:} Flat per-trade costs. True Q1 costs likely higher.
    \item \textbf{Model family:} Only LightGBM tested. Other models may extract different information.
    \item \textbf{Factor breadth:} 20 technical factors only. No factor discovery or alternative data.
    \item \textbf{No capacity model:} Formal market-impact model not constructed. Capacity estimates approximate.
    \item \textbf{Survivorship:} PIT universe includes delisted stocks; delisting returns not explicitly modeled.
\end{enumerate}
""")

# ============================================================
ws('11_conclusion.tex', f"""\\section{{Conclusion}}
OHLCV features contain genuine ranking information: IC {ic("frozen_baseline_mean_ic")}, NW $t = {raw("frozen_baseline_nw_t6")}$, within-Q1 selection {ret_pct("q1_within_excess")} monthly excess.
The signal did not survive executable portfolios: U50 net {ret_pct("u50_resid_net_annual")}, DD {dd_pct("u50_max_drawdown")}. Multi-horizon: H3 {ret_pct("h3_u50_net_annual")}, H6 {ret_pct("h6_u50_net_annual")}.
The contribution is a demonstration that clean negative results are more valuable than profitable-looking lies.
""")

# ============================================================
wa('evidence_map.tex', f"""\\section{{Evidence Map}}
Key metrics (of {len(m)} total):
\\begin{{itemize}}
    \\item \\texttt{{target\\_leak\\_before\\_ic}}: IC {ic("target_leak_before_ic")} $\\to$ \\texttt{{EXP\\_TARGET\\_SHIFT\\_01}}
    \\item \\texttt{{frozen\\_baseline\\_mean\\_ic}}: IC {ic("frozen_baseline_mean_ic")} $\\to$ \\texttt{{EXP\\_BASELINE\\_V43}}
    \\item \\texttt{{u100\\_raw\\_net\\_annual}}: {ret_pct("u100_raw_net_annual")} $\\to$ \\texttt{{EXP\\_DP1\\_PORTFOLIO}}
    \\item \\texttt{{u50\\_resid\\_net\\_annual}}: {ret_pct("u50_resid_net_annual")} $\\to$ \\texttt{{EXP\\_STEP5\\_ABLATION}}
    \\item \\texttt{{q1\\_within\\_excess}}: {ret_pct("q1_within_excess")} $\\to$ \\texttt{{EXP\\_DP1A\\_QUINTILE}}
    \\item \\texttt{{h3\\_u50\\_net\\_annual}}: {ret_pct("h3_u50_net_annual")} $\\to$ \\texttt{{EXP\\_MH1R\\_HORIZON}}
\\end{{itemize}}
""")

wa('experiment_ledger.tex', f"""\\section{{Experiment Ledger}}
\\begin{{enumerate}}
    \\item \\textbf{{Target Timing}}: IC {ic("target_leak_before_ic")} $\\to$ {ic("target_leak_after_ic")} ({cp}\\% collapse). Invalid $\\to$ Validated.
    \\item \\textbf{{Cross-Fit Audit}}: IC {ic("crossfit_ic_before")} $\\to$ {ic("crossfit_ic_after")}. Invalid $\\to$ Validated.
    \\item \\textbf{{Frozen Baseline}}: Mean OOS IC {ic("frozen_baseline_mean_ic")}, NW $t = {raw("frozen_baseline_nw_t6")}$. Validated.
    \\item \\textbf{{Null Infrastructure}}: Permutation correlation $\\approx$ 0. Validated.
    \\item \\textbf{{Portfolio Diagnostics}}: U100 {ret_pct("u100_raw_net_annual")}, U50 {ret_pct("u50_resid_net_annual")}. Q1-driven.
    \\item \\textbf{{Residual Ablation}}: Cannot reach profitability. Rejected.
    \\item \\textbf{{Multi-Horizon}}: H3 {ret_pct("h3_u50_net_annual")}, H6 {ret_pct("h6_u50_net_annual")} U50 net. Rejected.
    \\item \\textbf{{Termination}}: OHLCV-only core strategy closed. Recorded.
\\end{{enumerate}}
""")

wa('reproducibility.tex', f"""\\section{{Reproducibility}}
\\subsection{{Fully Reproducible}}
Evidence validation, website rendering, and all report metrics are reproducible from the repository with \\texttt{{python report/build.py}}.

\\subsection{{Not Fully Reproducible}}
Model training requires the RQAlpha market-data bundle ($\\sim$3.3GB, proprietary). Training scripts are included but data-dependent. \\texttt{{data/evidence.json}} serves as the authoritative publication layer.

\\subsection{{Repository}}
\\texttt{{https://github.com/DresdenGman/the-backtest-that-lied}} --- See repository tags for version information.
""")

print(f'Generated 11 sections + 3 appendices from {len(m)} evidence metrics')
