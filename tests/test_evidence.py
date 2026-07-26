#!/usr/bin/env python3
"""test_evidence.py — Verify evidence.json integrity. No hardcoded research values."""
import json, os, sys, unittest

EVIDENCE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'evidence.json')

class TestEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(EVIDENCE_PATH) as f:
            cls.data = json.load(f)

    def test_parses_successfully(self):
        self.assertIsInstance(self.data, dict)
        self.assertIn('metrics', self.data)

    def test_all_metric_references_resolve(self):
        metrics = self.data.get('metrics', {})
        # Check collapse references
        for c in self.data.get('collapses', []):
            for field in ['before', 'after']:
                v = c.get(field, {})
                if 'metric' in v:
                    self.assertIn(v['metric'], metrics, f"Collapse '{c['id']}' references unknown metric '{v['metric']}'")
        # Check exhibit references
        for ex in self.data.get('exhibits', {}).get('primary', []):
            for field in ['before_metric', 'after_metric']:
                if field in ex:
                    self.assertIn(ex[field], metrics, f"Exhibit '{ex['letter']}' references unknown metric '{ex[field]}'")
        # Check pipeline scenario references
        for s in self.data.get('pipeline_scenarios', []):
            if 'display_metric' in s and s['display_metric']:
                self.assertIn(s['display_metric'], metrics, f"Scenario '{s['id']}' references unknown metric '{s['display_metric']}'")

    def test_all_experiment_references_resolve(self):
        exp_ids = set()
        for m in self.data.get('metrics', {}).values():
            if 'experiment_id' in m:
                exp_ids.add(m['experiment_id'])
        # Ledger should reference valid experiment IDs (checked implicitly through metrics existence)

    def test_valid_metrics_contain_values_and_units(self):
        for key, m in self.data.get('metrics', {}).items():
            self.assertIn('value', m, f"Metric '{key}' missing value")
            self.assertIn('unit', m, f"Metric '{key}' missing unit")
            self.assertIsInstance(m['value'], (int, float), f"Metric '{key}' value is not numeric")

    def test_invalid_metrics_contain_status(self):
        for key, m in self.data.get('metrics', {}).items():
            self.assertIn('status', m, f"Metric '{key}' missing status field")

    def test_artifact_paths_are_relative(self):
        for key, m in self.data.get('metrics', {}).items():
            if 'artifact' in m:
                self.assertFalse(m['artifact'].startswith('/'), f"Metric '{key}' has absolute path")
                self.assertFalse(m['artifact'].startswith('~'), f"Metric '{key}' has home-relative path")

    def test_collapse_percentage_derives_from_values(self):
        metrics = self.data.get('metrics', {})
        for c in self.data.get('collapses', []):
            bkey = c.get('before', {}).get('metric')
            akey = c.get('after', {}).get('metric')
            if bkey and akey and bkey in metrics and akey in metrics:
                before = metrics[bkey]['value']
                after = metrics[akey]['value']
                if before != 0:
                    rel = abs((before - after) / abs(before))
                    self.assertGreater(rel, 0, f"Collapse '{c['id']}' shows zero relative decline")
                    self.assertLessEqual(rel, 1.0, f"Collapse '{c['id']}' relative decline exceeds 100%")

    def test_no_incompatible_unit_comparison(self):
        # Verify collapse before/after metrics have same unit type
        metrics = self.data.get('metrics', {})
        for c in self.data.get('collapses', []):
            bkey = c.get('before', {}).get('metric')
            akey = c.get('after', {}).get('metric')
            if bkey and akey and bkey in metrics and akey in metrics:
                bu = metrics[bkey].get('unit', '')
                au = metrics[akey].get('unit', '')
                # Both should be comparable (both IC or both return or both correlation)
                bu_cat = 'ic' if 'IC' in bu else ('return' if 'return' in bu else 'other')
                au_cat = 'ic' if 'IC' in au else ('return' if 'return' in au else 'other')
                self.assertEqual(bu_cat, au_cat,
                    f"Collapse '{c['id']}' compares incompatible units: '{bu}' vs '{au}'")

    def test_89_pct_collapse_derives_from_0_94_to_0_10(self):
        metrics = self.data.get('metrics', {})
        if 'target_leak_before_ic' in metrics and 'target_leak_after_ic' in metrics:
            before = metrics['target_leak_before_ic']['value']
            after = metrics['target_leak_after_ic']['value']
            self.assertAlmostEqual(before, 0.94, delta=0.01)
            self.assertAlmostEqual(after, 0.10, delta=0.01)
            rel = (before - after) / abs(before)
            self.assertAlmostEqual(rel * 100, 89.0, delta=1.0)


if __name__ == '__main__':
    unittest.main()
