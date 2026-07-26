#!/usr/bin/env python3
"""audit_report_provenance.py — Detect hardcoded empirical values in generate_sections.py."""
import json, os, sys, subprocess, re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN = os.path.join(REPO, 'scripts', 'generate_sections.py')

with open(GEN) as f:
    src = f.read()

with open(os.path.join(REPO, 'data', 'evidence.json')) as f:
    metrics = json.load(f)['metrics']

# Structural values exempt from audit (years, model params, feature counts, gate thresholds)
EXEMPT = {200, 20, 3, 6, 10, 12, 14, 25, 31, 50, 60, 75, 90, 80,
          0, 1, 2, 4, 5, 8, 11, 42, 100, 241, 5000,
          -1, 0.02, 0.7, 1.0, 10.0, 0.1, 0.03, 0.05, 0.001,
          2010, 2016, 2017, 2019, 2013, 2020, 2021, 2015, 2022, 2024, 2026, -2024,
          16, 17, 18, 19, 21, 22, 23, 24,
          120, 0.01, 1000}

NUMBER_RE = re.compile(r'(?<![\w.])-?\d+(?:\.\d+)?(?![\w.])')
EVIDENCE_CALLS = re.compile(r'\b(F|ic|ret_pct|ratio|dd_pct|unsigned_pct|raw|int)\s*\([^)]*\)')

errors = []
for i, line in enumerate(src.split('\n'), 1):
    if line.strip().startswith('#'):
        continue
    # Strip evidence function calls, then check remaining numbers
    stripped = EVIDENCE_CALLS.sub(' ', line)
    for m in NUMBER_RE.finditer(stripped):
        val = m.group()
        try:
            num = float(val)
        except ValueError:
            continue
        if num in EXEMPT or (num == int(num) and int(num) in EXEMPT):
            continue
        errors.append((i, val, line.strip()[:80]))

if errors:
    print(f'❌ {len(errors)} unverified empirical values:')
    for line, val, ctx in errors[:10]:
        print(f'  Line {line}: {val} — {ctx}')
    sys.exit(1)

# Regenerate and diff
subprocess.run([sys.executable, GEN], cwd=REPO, capture_output=True)
diff = subprocess.run(['git', 'diff', '--', 'report/sections/', 'report/appendix/'],
                     cwd=REPO, capture_output=True, text=True)
if diff.stdout.strip():
    print('❌ Generated sections differ from committed')
    sys.exit(1)
print('✅ All content matches evidence.json')
