def calculate_discount(order_total: float, customer_tier: str) -> float:
    if customer_tier == "gold" and order_total >= 100:
        return round(order_total * 0.10, 2)
    return 0.0
