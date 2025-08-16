# src/discovery/feeds.py
import csv
from pathlib import Path
from typing import List
from src.app.models import Finding
from datetime import datetime
from datetime import datetime, UTC


import json

def write_findings_jsonl(findings: List[Finding], out_path: str):
    with open(out_path, "w", encoding="utf-8") as f:
        for finding in findings:
            # Convert Pydantic model to dict and handle serialization
            finding_dict = finding.model_dump()
            # Convert HttpUrl objects to strings for JSON serialization
            finding_dict['url'] = str(finding_dict['url'])
            # Convert datetime objects to ISO format strings for JSON serialization
            if 'discovered_at' in finding_dict and finding_dict['discovered_at']:
                finding_dict['discovered_at'] = finding_dict['discovered_at'].isoformat()
            f.write(json.dumps(finding_dict) + "\n")



def load_findings_from_csv(csv_path: str) -> List[Finding]:
    findings = []
    seen = set()
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            raw_url = (row.get("url") or "").strip()
            source = (row.get("source") or "").strip() or "unknown"
            if not raw_url:
                # Skip empty URL rows
                continue

            url = _ensure_scheme(raw_url)  # NEW: add https:// if missing
            domain = _normalize_domain(url)
            try:
                finding = Finding(
                    url=url,
                    discovered_at=datetime.now(UTC),
                    source=source,
                )
                findings.append(finding)
                seen.add(key)
            except Exception as e:
                print(f"Skipping invalid URL ({url}): {e}")
    return findings

def _normalize_domain(url: str) -> str:
    # Simple domain extraction (improve as needed)
    url = url.replace("http://", "").replace("https://", "")
    domain = url.split("/")[0]
    return domain.lower()

def _ensure_scheme(url: str, default_scheme: str = "https") -> str:
    """If URL has no scheme, prepend default_scheme://."""
    u = url.strip()
    if not u:
        return u
    # Has scheme?
    if u.startswith(("http://", "https://")):
        return u
    return f"{default_scheme}://{u}"
