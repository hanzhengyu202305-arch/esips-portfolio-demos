from __future__ import annotations


ORDERS = {
    "demo-100": {
        "order_id": "demo-100",
        "amount": 1500,
        "country": "AU",
        "status": "paid",
        "customer_tier": "gold",
    }
}


def calculate_discount(order_total: float, customer_tier: str) -> float:
    if customer_tier == "gold" and order_total >= 100:
        return round(order_total * 0.10, 2)
    return 0.0


def get_order(order_id: str) -> dict:
    return ORDERS.get(
        order_id,
        {
            "order_id": order_id,
            "amount": 0,
            "country": "AU",
            "status": "not_found",
            "customer_tier": "standard",
        },
    )


def predict_order_risk(payload: dict) -> dict:
    amount = float(payload.get("amount", 0))
    country = str(payload.get("country", ""))
    score = 0.24
    if amount >= 1000:
        score += 0.30
    if country != "AU":
        score += 0.20
    else:
        score += 0.10
    score = round(min(score, 0.99), 2)
    return {"risk": "review" if score >= 0.6 else "low", "score": score}


def score_orders(orders: list[dict]) -> list[float]:
    totals_by_customer: dict[str, float] = {}
    for order in orders:
        customer_id = str(order.get("customer_id", "unknown"))
        totals_by_customer.setdefault(customer_id, 0.0)
        totals_by_customer[customer_id] += float(order.get("amount", 0))
    return [totals_by_customer[str(order.get("customer_id", "unknown"))] for order in orders]
