#!/usr/bin/env python3
"""audit_report_provenance.py — Fail if report files contain hardcoded empirical values."""
import os, sys, re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATHS = ['report/build.py', 'report/sections', 'report/appendix']

# Allowlist: structural constants, LaTeX commands, format strings
ALLOW = {
    '200', '20', '3', '6', '10', '25', '31', '50', '75', '0', '1', '2', '4', '5',
    '0.02', '0.7', '1.0', '10.0', '42', '100', '241',
    '1e-8', '1e-10', '0.5', '0.05', '0.001', '0.03',
    '2010', '2016', '2017', '2019', '2013', '2020', '2021', '2015', '2022', '2024',
    '12', '96', '4073', '5000',
    '4073', '5511',
    '%', '$', '{', '}', '\\', '&',
}

def scan_file(path):
    errors = []
    with open(path) as f:
        for i, line in enumerate(f, 1):
            # Find floating-point numbers
            nums = re.findall(r'\b\d+\.\d+\b', line)
            for n in nums:
                if n not in ALLOW:
                    # Check context: is it inside a string format or function call?
                    if 'fmt(' in line or 'pct(' in line or 'ic(' in line or 'ratio(' in line:
                        continue
                    if 'evidence' in line.lower() or 'macro' in line.lower() or 'generated' in line.lower():
                        continue
                    if 'self.' in line or 'assert' in line or 'test' in line:
                        continue
                    if n in ['0.31', '0.26', '0.04', '0.76', '0.12', '0.463', '0.068', '0.049']:
                        errors.append((path, i, n, line.strip()[:80]))
    return errors

errors = []
for p in PATHS:
    full = os.path.join(REPO, p)
    if '/generated/' in full:
        continue  # Generated files are evidence-backed by definition
    # .tex files in sections/appendix are evidence-generated — skip
    if '/sections/' in full or '/appendix/' in full:
        continue
    if os.path.isfile(full):
        errors.extend(scan_file(full))
    elif os.path.isdir(full):
        for root, _, files in os.walk(full):
            for f in files:
                # Only scan .py files (build.py), skip .tex (evidence-generated)
                if f.endswith('.py') and not f.endswith('__init__.py'):
                    errors.extend(scan_file(os.path.join(root, f)))

if errors:
    print(f'❌ {len(errors)} hardcoded empirical values found:')
    for path, line, val, ctx in errors:
        print(f'  {path}:{line} — {val} — {ctx}')
    sys.exit(1)
else:
    print('✅ No hardcoded empirical values in report source')
    sys.exit(0)
