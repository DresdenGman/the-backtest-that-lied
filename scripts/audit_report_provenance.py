#!/usr/bin/env python3
"""audit_report_provenance.py — Verify generate_sections.py is the canonical source."""
import json, os, sys, subprocess, re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN = os.path.join(REPO, 'scripts', 'generate_sections.py')

# 1. Audit generate_sections.py for hardcoded empirical values
with open(GEN) as f:
    src = f.read()

with open(os.path.join(REPO, 'data', 'evidence.json')) as f:
    m = json.load(f)['metrics']

# Any number in the source that looks like a research result must come via F(), ic(), ret_pct(), etc.
# Structural values (years, feature counts, model params) are exempt.
EXEMPT_LINES = {'200', '20', '3', '6', '10', '12', '14', '25', '31', '50', '60', '75', '90',
                '0', '1', '2', '4', '5', '96',
                '0.02', '0.7', '1.0', '10.0', '0.1', '0.03', '0.05',
                '42', '100', '241', '5000',
                '2010', '2016', '2017', '2019', '2013', '2020', '2021', '2015', '2022', '2024',
                '4.2', '3.2', '1.0',
                '0.01', '0.001', '1000'}

errors = []
# Find suspicious patterns: number.number in lines that are NOT function calls
for i, line in enumerate(src.split('\n'), 1):
    nums = re.findall(r'\b\d+\.\d+\b', line)
    for n in nums:
        if n in EXEMPT_LINES:
            continue
        # Is this line calling an evidence function?
        if any(f in line for f in ['F(', 'ic(', 'ret_pct(', 'ratio(', 'dd_pct(', 'unsigned_pct(', 'raw(']):
            continue
        # Is it a comment or docstring?
        stripped = line.strip()
        if stripped.startswith('#') or stripped.startswith('"""') or stripped.startswith("'''"):
            continue
        errors.append((i, n, line.strip()[:80]))

if errors:
    print(f'❌ generate_sections.py has {len(errors)} unverified values:')
    for line, val, ctx in errors[:10]:
        print(f'  Line {line}: {val} — {ctx}')
    sys.exit(1)

# 2. Regenerate and diff
subprocess.run([sys.executable, GEN], cwd=REPO, capture_output=True)
diff = subprocess.run(['git', 'diff', '--', 'report/sections/', 'report/appendix/'],
                     cwd=REPO, capture_output=True, text=True)
if diff.stdout.strip():
    print('❌ Sections differ from generated output')
    sys.exit(1)
print('✅ All content matches evidence.json')
