import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from discovery.feeds import load_findings_from_csv

def test_load_findings():
    csv_path = "examples/seed_urls.csv"
    findings = load_findings_from_csv(csv_path)
    assert len(findings) > 0
    assert all(f.url for f in findings)
