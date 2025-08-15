# src/app/models.py
from __future__ import annotations
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, HttpUrl, Field, field_validator


class Finding(BaseModel):
    url: HttpUrl
    discovered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source: str = "local_csv"
    risk_score: Optional[float] = None

    @field_validator("source")
    @classmethod
    def _trim_source(cls, v: str) -> str:
        return v.strip() or "unknown"


class Evidence(BaseModel):
    url: HttpUrl
    final_url: Optional[HttpUrl] = None
    redirects: List[str] = []
    screenshot_path: Optional[str] = None
    html_hash: Optional[str] = None
    html_size: Optional[int] = None


class NetworkMeta(BaseModel):
    dns_records: Dict[str, Any] = {}  # e.g., {"A": ["1.2.3.4"], "AAAA": []}
    ip: Optional[str] = None
    asn: Optional[str] = None
    tls_issuer: Optional[str] = None


class Parties(BaseModel):
    registrar: Optional[str] = None
    registrar_abuse: Optional[str] = None
    hoster: Optional[str] = None
    hoster_abuse: Optional[str] = None
    brand_contact: Optional[str] = None


class Report(BaseModel):
    url: HttpUrl
    recipients: List[str] = []
    message_id: Optional[str] = None
    sent_at: Optional[datetime] = None
    attachments: List[str] = []
    status: str = "draft"


class Outcome(BaseModel):
    url: HttpUrl
    status: str = "pending"  # pending | reported | taken_down | false_positive | unknown
    last_seen_http_status: Optional[int] = None
    observed_takedown_at: Optional[datetime] = None
    sla_days: Optional[float] = None
