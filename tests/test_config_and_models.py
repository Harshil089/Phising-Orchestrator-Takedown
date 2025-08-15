# tests/test_config_and_models.py
# tests/test_config_and_models.py

# Ensure the `src/` directory is on the Python path for imports to work.
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from urllib.parse import urlparse
from src.app.config import get_config
from src.app.models import Finding, Evidence, Report

def test_config_defaults():
    cfg = get_config()  # loads examples/sample_config.yaml if present
    assert cfg.reporting.enable_reporting is False
    assert cfg.browser.headless is True
    assert cfg.paths.artifacts_dir.exists()

def test_finding_and_report_models():
    f = Finding(url="https://example.com", source="unit_test")
    assert urlparse(str(f.url)).hostname == "example.com"
    r = Report(url=f.url, recipients=["abuse@example.org"])
    assert r.status == "draft"
    e = Evidence(url=f.url)
    assert urlparse(str(e.url)).hostname == "example.com"
