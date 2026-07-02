def score_orders(orders):
    totals_by_customer = {}
    for order in orders:
        totals_by_customer.setdefault(order["customer_id"], 0)
        totals_by_customer[order["customer_id"]] += order["amount"]
    return [totals_by_customer[order["customer_id"]] for order in orders]
