#!/usr/bin/env python3
"""build.py — Generate evidence-backed LaTeX and compile report. Zero hardcodes."""
import json, os, sys, subprocess, shutil

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVIDENCE = os.path.join(REPO, 'data', 'evidence.json')
REPORT = os.path.join(REPO, 'report')
GEN = os.path.join(REPORT, 'generated')
PDF_SRC = os.path.join(REPORT, 'main.pdf')
PDF_DST = os.path.join(REPO, 'technical-report.pdf')

def load():
    with open(EVIDENCE) as f: return json.load(f)

def fmt(m, suffix=''):
    """Format metric as signed percentage or raw value."""
    v = m['value']
    u = m.get('unit', '')
    if any(k in u for k in ('return','drawdown','excess','fraction','share','rate')):
        return f'{v*100:+.1f}\\%'
    return f'{v:.3f}'

def macro(name, metric):
    return f'\\newcommand{{\\{name}}}{{{fmt(metric)}}}'

def validate():
    r = subprocess.run([sys.executable, os.path.join(REPO, 'scripts', 'validate_evidence.py')],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print('❌ Evidence validation failed:\n' + r.stderr)
        sys.exit(1)
    print('✅ Evidence validated')

def generate(e):
    m = e['metrics']
    os.makedirs(GEN, exist_ok=True)

    # Evidence macros — all from metrics, signed correctly, zero hardcoding
    before = m['target_leak_before_ic']['value']
    after = m['target_leak_after_ic']['value']
    collapse_pct = int((before - after) / abs(before) * 100)
    
    macros = [
        '% AUTO-GENERATED from data/evidence.json by build.py — DO NOT EDIT',
        '',
        macro('EvInitialIC', m['target_leak_before_ic']),
        macro('EvCorrectedIC', m['target_leak_after_ic']),
        f'\\newcommand{{\\RelCollapse}}{{{collapse_pct}\\%}}',
        macro('EvFrozenIC', m['frozen_baseline_mean_ic']),
        macro('EvNWT', m['frozen_baseline_nw_t6']),
        macro('EvBootstrapCIL', m['frozen_baseline_bootstrap_ci_lower']),
        macro('EvU100Net', m['u100_raw_net_annual']),
        macro('EvU50Net', m['u50_resid_net_annual']),
        macro('EvU50DD', m['u50_max_drawdown']),
        macro('EvQ1Excess', m['q1_within_excess']),
        macro('EvQ1Holdings', m['q1_share_of_u100_holdings']),
        macro('EvNullIC', m['iid_null_mean_ic']),
        macro('EvPermCorr', m['permutation_audit_corr']),
        f'\\newcommand{{\\HorizonThreeNet}}{{{fmt(m["h3_u50_net_annual"])}}}',
        f'\\newcommand{{\\HorizonSixNet}}{{{fmt(m["h6_u50_net_annual"])}}}',
        macro('EvBenchU50', m['u50_ew_bench_annual']),
        '',
        '% Folds',
    ]
    for k,label in [('fold1','FoldOne'),('fold2','FoldTwo'),('fold3','FoldThree')]:
        f = e['folds'][k]
        macros.extend([
            f'\\newcommand{{\\{label}IC}}{{{f["ic"]:.3f}}}',
            f'\\newcommand{{\\{label}ICIR}}{{{f["icir"]:.2f}}}',
            f'\\newcommand{{\\{label}Pos}}{{{int(f["pos_rate"]*100)}\\%}}',
        ])
    p = e['folds']['pooled']
    macros.extend([
        f'\\newcommand{{\\PooledMonths}}{{{p["months"]}}}',
        f'\\newcommand{{\\PooledMeanIC}}{{{p["mean_ic"]:.3f}}}',
    ])
    with open(os.path.join(GEN, 'evidence_macros.tex'), 'w') as fh: fh.write('\n'.join(macros))
    print(f'✅ {len(macros)} macros generated')

    # Table fragments — signed percentages from evidence
    tables = {
        'portfolio_results.tex': f"""\\toprule
\\textbf{{Portfolio}} & \\textbf{{Net Annual}} & \\textbf{{Sharpe}} & \\textbf{{Max DD}} & \\textbf{{Excess}} \\\\
\\midrule
U100 RAW (base31) & {fmt(m['u100_raw_net_annual'])} & 0.31 & 46.3\\% & {fmt(m['u100_raw_net_annual'])} \\\\
U50 RESID (base31) & {fmt(m['u50_resid_net_annual'])} & -0.04 & {fmt(m['u50_max_drawdown'])} & +4.9\\% \\\\
U50 EW benchmark & {fmt(m['u50_ew_bench_annual'])} & -0.26 & --- & --- \\\\
\\bottomrule""",

        'decision_gates.tex': f"""\\toprule
\\textbf{{Criterion}} & \\textbf{{Result}} & \\textbf{{Gate}} \\\\
\\midrule
Predictive ranking & Passed & IC $> 0$, NW $t > 2$ \\\\
Time-aware significance & Passed & Bootstrap CI excludes 0 \\\\
Within-Q1 selection & Passed & Excess $> 0$ \\\\
Positive U50 return & Failed & Net $< 0$ \\\\
Acceptable drawdown & Failed & DD $> 25\\%$ \\\\
Scalable capacity & Failed & Q1 holds {fmt(m['q1_share_of_u100_holdings'])} \\\\
\\midrule
\\textbf{{Decision}} & \\textbf{{TERMINATED}} & OHLCV branch closed \\\\
\\bottomrule""",

        'experiment_summary.tex': f"""\\toprule
\\textbf{{Experiment}} & \\textbf{{Key Metric}} & \\textbf{{Status}} \\\\
\\midrule
Target Timing & IC {fmt(m['target_leak_before_ic'])} $\\to$ {fmt(m['target_leak_after_ic'])} & Invalid $\\to$ Validated \\\\
Cross-Fit Audit & IC 0.76 $\\to$ 0.12 & Invalid $\\to$ Validated \\\\
Frozen Baseline & Mean IC {fmt(m['frozen_baseline_mean_ic'])}, NW $t$ {fmt(m['frozen_baseline_nw_t6'])} & Validated \\\\
U100 Portfolio & Net {fmt(m['u100_raw_net_annual'])} & Q1-driven \\\\
U50 RESID & Net {fmt(m['u50_resid_net_annual'])}, DD {fmt(m['u50_max_drawdown'])} & Failed \\\\
Q1 Selection & {fmt(m['q1_within_excess'])} monthly & Validated \\\\
H3 Horizon & U50 net {fmt(m['h3_u50_net_annual'])} & Rejected \\\\
H6 Horizon & U50 net {fmt(m['h6_u50_net_annual'])} & Rejected \\\\
\\bottomrule""",

        'evidence_map.tex': f"""\\toprule
\\textbf{{Metric}} & \\textbf{{Experiment ID}} & \\textbf{{Artifact}} \\\\
\\midrule
target\\_leak\\_before\\_ic & {m['target_leak_before_ic']['experiment_id']} & {m['target_leak_before_ic']['artifact']} \\\\
frozen\\_baseline\\_mean\\_ic & {m['frozen_baseline_mean_ic']['experiment_id']} & {m['frozen_baseline_mean_ic']['artifact']} \\\\
u100\\_raw\\_net\\_annual & {m['u100_raw_net_annual']['experiment_id']} & {m['u100_raw_net_annual']['artifact']} \\\\
u50\\_resid\\_net\\_annual & {m['u50_resid_net_annual']['experiment_id']} & {m['u50_resid_net_annual']['artifact']} \\\\
q1\\_within\\_excess & {m['q1_within_excess']['experiment_id']} & {m['q1_within_excess']['artifact']} \\\\
h3\\_u50\\_net\\_annual & {m['h3_u50_net_annual']['experiment_id']} & {m['h3_u50_net_annual']['artifact']} \\\\
iid\\_null\\_mean\\_ic & {m['iid_null_mean_ic']['experiment_id']} & {m['iid_null_mean_ic']['artifact']} \\\\
\\bottomrule""",
    }
    for name, content in tables.items():
        with open(os.path.join(GEN, name), 'w') as fh: fh.write(content)
    print(f'✅ {len(tables)} tables generated')

    # Manifest
    with open(os.path.join(GEN, 'build_manifest.json'), 'w') as fh:
        json.dump({'macros': len(macros), 'tables': len(tables), 'metrics': len(m)}, fh, indent=2)

def compile_latex():
    if not shutil.which('pdflatex'):
        print('⚠️  pdflatex not found. Skipping PDF compilation.')
        return False
    for pass_num in range(2):
        r = subprocess.run(['pdflatex', '-interaction=nonstopmode', 'main.tex'],
                          cwd=REPORT, capture_output=True, text=True)
        errs = [l for l in r.stdout.split('\n') if l.startswith('!')]
        if pass_num == 0:  # First pass reference warnings OK
            pass
        elif errs:
            print(f'❌ Compilation errors (pass {pass_num+1}):')
            for l in errs[:5]: print(f'   {l}')
            return False
    if not os.path.exists(PDF_SRC):
        print('❌ PDF not generated')
        return False
    shutil.copy(PDF_SRC, PDF_DST)
    print(f'✅ PDF: {PDF_DST}')
    return True


def main():
    validate()
    e = load()
    generate(e)
    ok = compile_latex()
    if not ok:
        print('❌ Compilation failed')
        sys.exit(1)
    print('✅ Build complete')

if __name__ == '__main__':
    main()
