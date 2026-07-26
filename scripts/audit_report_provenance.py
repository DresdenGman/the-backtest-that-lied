#!/usr/bin/env python3
"""audit_report_provenance.py — Verify sections match evidence.json. Regenerate and diff."""
import json, os, sys, subprocess

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVIDENCE = os.path.join(REPO, 'data', 'evidence.json')
SECTIONS = os.path.join(REPO, 'report', 'sections')

with open(EVIDENCE) as f:
    evidence = json.load(f)

# Regenerate all sections and diff
result = subprocess.run([sys.executable, os.path.join(REPO, 'scripts', 'generate_sections.py')],
                       capture_output=True, text=True)
if result.returncode != 0:
    print('❌ Section generation failed:\n' + result.stderr)
    sys.exit(1)

# Check git diff — should be empty
diff = subprocess.run(['git', 'diff', '--', 'report/sections/', 'report/appendix/'],
                     cwd=REPO, capture_output=True, text=True)
if diff.stdout.strip():
    print('❌ Sections differ from evidence-generated output:')
    print(diff.stdout[:2000])
    sys.exit(1)

# Also audit build.py for hardcoded empirical values
build_py = os.path.join(REPO, 'report', 'build.py')
with open(build_py) as f:
    bp = f.read()
# Blacklist values that must not appear in build.py
forbidden = ['0.31', '46.3', '-0.04', '+4.9', '-0.26', '0.76', '0.12',
             '0.940', '0.100', '0.108', '6.8', '61.3', '21.7', '15.2', '48.1']
found = [v for v in forbidden if v in bp]
if found:
    print(f'❌ build.py contains hardcoded values: {found}')
    sys.exit(1)

print('✅ All report content matches evidence.json')
sys.exit(0)
