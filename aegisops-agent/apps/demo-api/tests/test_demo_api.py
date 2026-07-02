from __future__ import annotations

import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from app.config import get_settings
from app.main import health
from app.service import calculate_discount, get_order, predict_order_risk


def test_health_returns_ok() -> None:
    assert health() == {"status": "ok"}


def test_discount_logic_is_deterministic() -> None:
    assert calculate_discount(order_total=250.0, customer_tier="gold") == 25.0
    assert calculate_discount(order_total=80.0, customer_tier="standard") == 0.0


def test_order_lookup_returns_demo_order() -> None:
    order = get_order("demo-100")

    assert order["order_id"] == "demo-100"
    assert order["status"] == "paid"


def test_predict_order_risk_uses_amount_and_country() -> None:
    assert predict_order_risk({"amount": 1500, "country": "AU"}) == {
        "risk": "review",
        "score": 0.64,
    }


def test_settings_default_to_demo_mode() -> None:
    settings = get_settings()

    assert settings.app_mode == "demo"
    assert settings.service_name == "aegisops-demo-api"
