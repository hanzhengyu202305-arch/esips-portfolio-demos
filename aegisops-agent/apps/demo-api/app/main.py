from __future__ import annotations

from app.config import get_settings
from app.service import get_order, predict_order_risk


try:
    from fastapi import FastAPI
except Exception:  # pragma: no cover - used only when FastAPI is not installed

    class FastAPI:  # type: ignore[no-redef]
        def __init__(self, title: str):
            self.title = title
            self.routes = []

        def get(self, path: str):
            def decorator(func):
                self.routes.append(("GET", path, func))
                return func

            return decorator

        def post(self, path: str):
            def decorator(func):
                self.routes.append(("POST", path, func))
                return func

            return decorator


app = FastAPI(title="AegisOps Demo API")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/predict")
def predict(payload: dict) -> dict:
    return predict_order_risk(payload)


@app.get("/orders/{order_id}")
def order(order_id: str) -> dict:
    return get_order(order_id)


@app.get("/metrics")
def metrics() -> dict:
    settings = get_settings()
    return {
        "service_name": settings.service_name,
        "app_mode": settings.app_mode,
        "latency_budget_ms": settings.latency_budget_ms,
    }
