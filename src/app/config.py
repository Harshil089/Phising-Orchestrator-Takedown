# src/app/config.py
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
import os
import json

try:
    import yaml  # type: ignore
except Exception:  # lightweight fallback if PyYAML not installed yet
    yaml = None  # pragma: no cover


@dataclass(frozen=True)
class BrowserSettings:
    headless: bool = True
    javascript_enabled: bool = False
    user_agent: str = "Mozilla/5.0 (compatible; PhishTakedownOrchestrator/0.1; +local)"
    nav_timeout_ms: int = 10000
    max_redirects: int = 5


@dataclass(frozen=True)
class Paths:
    root: Path
    artifacts_dir: Path
    outbox_dir: Path
    runs_dir: Path

    @staticmethod
    def from_root(root: Path) -> "Paths":
        artifacts = root / "artifacts"
        outbox = root / ".outbox"
        runs = root / ".runs"
        artifacts.mkdir(parents=True, exist_ok=True)
        outbox.mkdir(parents=True, exist_ok=True)
        runs.mkdir(parents=True, exist_ok=True)
        return Paths(root=root, artifacts_dir=artifacts, outbox_dir=outbox, runs_dir=runs)


@dataclass(frozen=True)
class Reporting:
    enable_reporting: bool = False  # global kill switch
    smtp_server: Optional[str] = None
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    rate_limit_per_min: int = 15


@dataclass(frozen=True)
class Sheets:
    google_sheet_id: Optional[str] = None
    google_credentials_path: Optional[str] = None


@dataclass(frozen=True)
class Heuristics:
    suspicious_tlds: List[str] = None  # type: ignore
    brand_keywords: List[str] = None  # type: ignore
    url_length_warn: int = 100

    def __init__(
        self,
        suspicious_tlds: Optional[List[str]] = None,
        brand_keywords: Optional[List[str]] = None,
        url_length_warn: int = 100,
    ):
        object.__setattr__(self, "suspicious_tlds", suspicious_tlds or ["top", "xyz", "gq", "tk", "ml", "cf"])
        object.__setattr__(self, "brand_keywords", brand_keywords or ["login", "verify", "account", "bank"])
        object.__setattr__(self, "url_length_warn", url_length_warn)


@dataclass(frozen=True)
class Config:
    env: str
    browser: BrowserSettings
    paths: Paths
    reporting: Reporting
    sheets: Sheets
    heuristics: Heuristics

    def to_json(self) -> str:
        def _default(o):
            if isinstance(o, Path):
                return str(o)
            if hasattr(o, "__dict__"):
                return o.__dict__
            return str(o)
        return json.dumps(self, default=_default, indent=2)


_cached_config: Optional[Config] = None


def _load_yaml(path: Path) -> dict:
    if not path.exists() or yaml is None:
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def get_config(config_yaml: Optional[str] = None) -> Config:
    global _cached_config
    if _cached_config is not None and config_yaml is None:
        return _cached_config

    root = Path(os.getcwd())

    # Load YAML if provided or default examples/sample_config.yaml
    yaml_path = Path(config_yaml) if config_yaml else (root / "examples" / "sample_config.yaml")
    data = _load_yaml(yaml_path)

    # ENV
    env = os.getenv("APP_ENV", data.get("env", "dev"))

    # Browser
    browser = BrowserSettings(
        headless=bool(str(data.get("browser", {}).get("headless", "true")).lower() == "true"),
        javascript_enabled=bool(str(data.get("browser", {}).get("javascript_enabled", "false")).lower() == "true"),
        user_agent=data.get("browser", {}).get("user_agent", BrowserSettings.user_agent),
        nav_timeout_ms=int(data.get("browser", {}).get("nav_timeout_ms", BrowserSettings.nav_timeout_ms)),
        max_redirects=int(data.get("browser", {}).get("max_redirects", BrowserSettings.max_redirects)),
    )

    # Paths
    paths = Paths.from_root(root)

    # Reporting (env overrides)
    reporting = Reporting(
        enable_reporting=(os.getenv("ENABLE_REPORTING", str(data.get("reporting", {}).get("enable_reporting", "false"))).lower() == "true"),
        smtp_server=os.getenv("SMTP_SERVER", data.get("reporting", {}).get("smtp_server")),
        smtp_username=os.getenv("SMTP_USERNAME", data.get("reporting", {}).get("smtp_username")),
        smtp_password=os.getenv("SMTP_PASSWORD", data.get("reporting", {}).get("smtp_password")),
        rate_limit_per_min=int(os.getenv("RATE_LIMIT_PER_MIN", data.get("reporting", {}).get("rate_limit_per_min", 15))),
    )

    # Sheets
    sheets = Sheets(
        google_sheet_id=os.getenv("GOOGLE_SHEET_ID", data.get("sheets", {}).get("google_sheet_id")),
        google_credentials_path=os.getenv("GOOGLE_CREDENTIALS_PATH", data.get("sheets", {}).get("google_credentials_path")),
    )

    # Heuristics
    heur = data.get("heuristics", {})
    heuristics = Heuristics(
        suspicious_tlds=heur.get("suspicious_tlds"),
        brand_keywords=heur.get("brand_keywords"),
        url_length_warn=int(heur.get("url_length_warn", 100)),
    )

    cfg = Config(
        env=env,
        browser=browser,
        paths=paths,
        reporting=reporting,
        sheets=sheets,
        heuristics=heuristics,
    )

    if config_yaml is None:
        _cached_config = cfg
    return cfg
