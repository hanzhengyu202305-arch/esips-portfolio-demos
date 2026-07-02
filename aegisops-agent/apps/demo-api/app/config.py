from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_mode: str = "demo"
    service_name: str = "aegisops-demo-api"
    latency_budget_ms: int = 250


def get_settings() -> Settings:
    return Settings(app_mode=os.getenv("APP_MODE", "demo"))
