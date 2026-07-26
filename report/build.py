#!/usr/bin/env python3
"""build.py — Single entry point: generate → validate → audit → compile → PDF."""
import os, sys, subprocess, shutil

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(REPO, 'scripts')
REPORT = os.path.join(REPO, 'report')
PDF_SRC = os.path.join(REPORT, 'main.pdf')
PDF_DST = os.path.join(REPO, 'technical-report.pdf')

def run(cmd, label):
    print(f'[{label}]', end=' ', flush=True)
    r = subprocess.run([sys.executable] + cmd, cwd=REPO, capture_output=True, text=True)
    if r.returncode != 0:
        print(f'❌\n{r.stderr[:800]}')
        sys.exit(1)
    print('✅')

def compile_latex():
    if not shutil.which('pdflatex'):
        print('[LaTeX] ⚠️  pdflatex not found')
        return False
    for i in range(2):
        r = subprocess.run(['pdflatex', '-interaction=nonstopmode', 'main.tex'],
                          cwd=REPORT, capture_output=True, text=True)
        errs = [l for l in r.stdout.split('\n') if l.startswith('!')]
        if i == 1 and errs:
            print(f'[LaTeX] ❌ {len(errs)} errors')
            for l in errs[:3]: print(f'   {l}')
            return False
    if os.path.exists(PDF_SRC):
        shutil.copy(PDF_SRC, PDF_DST)
        print(f'[LaTeX] ✅ {PDF_DST}')
        # Check for table-command leakage
        if shutil.which('pdftotext'):
            txt = subprocess.run(['pdftotext', PDF_DST, '-'], capture_output=True, text=True).stdout
            leaks = [l for l in txt.split('\n') if 'midrule' in l.lower() or 'bottomrule' in l.lower()]
            if leaks:
                print(f'[Leak] ❌ {len(leaks)} table commands in PDF text')
                return False
        return True
    print('[LaTeX] ❌ PDF not generated')
    return False

def main():
    run([os.path.join(SCRIPTS, 'validate_evidence.py')], 'Validate')
    run([os.path.join(SCRIPTS, 'generate_sections.py')], 'Generate')
    run([os.path.join(SCRIPTS, 'audit_report_provenance.py')], 'Audit')
    if not compile_latex():
        sys.exit(1)
    print('✅ Build complete')

if __name__ == '__main__':
    main()
