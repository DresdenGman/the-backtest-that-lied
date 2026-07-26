#!/usr/bin/env python3
"""validate_evidence.py — Ensure every displayed metric has provenance."""
import json, sys, os

EVIDENCE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'evidence.json')

def load_evidence():
    with open(EVIDENCE_PATH) as f:
        return json.load(f)

def validate():
    e = load_evidence()
    errors = []
    exp_ids = set()

    # 1. All metrics must have experiment_id and artifact
    for key, m in e.get('metrics', {}).items():
        if 'experiment_id' not in m:
            errors.append(f"Metric '{key}' missing experiment_id")
        else:
            eid = m['experiment_id']
            # Allow duplicates: before/after of same experiment
            if eid not in exp_ids:
                exp_ids.add(eid)
        if 'artifact' not in m:
            errors.append(f"Metric '{key}' missing artifact path")
        if 'status' not in m:
            errors.append(f"Metric '{key}' missing status field")

    # 2. Verify key percentages
    tl_before = e['metrics']['target_leak_before_ic']['value']
    tl_after = e['metrics']['target_leak_after_ic']['value']
    abs_decline = tl_before - tl_after
    rel_decline = (tl_before - tl_after) / tl_before
    if not abs(abs_decline - 0.84) < 0.01:
        errors.append(f"Absolute decline {abs_decline:.2f} ≠ 0.84")
    if not abs(rel_decline - 0.8936) < 0.01:
        errors.append(f"Relative decline {rel_decline:.4f} ≠ 0.8936")

    # 3. Collapses must reference valid metrics
    for c in e.get('collapses', []):
        for field in ['before', 'after']:
            v = c.get(field, {})
            if 'metric' in v:
                if v['metric'] not in e['metrics']:
                    errors.append(f"Collapse '{c['id']}' references unknown metric '{v['metric']}'")

    # 4. Exhibits must reference valid metrics
    for ex in e.get('exhibits', {}).get('primary', []):
        for field in ['before_metric', 'after_metric']:
            if field in ex and ex[field] not in e['metrics']:
                errors.append(f"Exhibit '{ex['letter']}' references unknown metric '{ex[field]}'")

    # 5. Timeline must have exactly one killed stage
    killed = [t for t in e.get('timeline', []) if t.get('status') == 'killed']
    if len(killed) != 1:
        errors.append(f"Expected 1 killed timeline stage, found {len(killed)}")

    # 6. Integrity checks must be all boolean answers
    for ic in e.get('integrity_checks', []):
        if not isinstance(ic.get('answer'), bool):
            errors.append(f"Integrity check '{ic['question'][:40]}...' has non-boolean answer")

    if errors:
        print(f"❌ {len(errors)} validation errors:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print(f"✅ All validations passed ({len(e['metrics'])} metrics, {len(e['collapses'])} collapses, {len(e['exhibits']['primary'])} primary exhibits)")
        sys.exit(0)

if __name__ == '__main__':
    validate()
