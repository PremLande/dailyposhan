from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response

ORDERS = []


@api_view(["POST"])
def create_order(request):
    payload = request.data
    order_id = f"DP{10000 + len(ORDERS)}"
    order = {
        "id": order_id,
        "customer_name": payload.get("customer_name"),
        "phone": payload.get("phone"),
        "address": payload.get("address"),
        "items": payload.get("items", []),
        "total": payload.get("total", 0),
        "payment_method": payload.get("payment_method", "cod"),
        "payment_status": payload.get("payment_status", "Pending COD"),
        "status": "Pending",
        "created_at": datetime.utcnow().isoformat(),
    }
    ORDERS.append(order)
    return Response(order, status=201)


@api_view(["GET"])
def order_by_id(request, order_id):
    order = next((o for o in ORDERS if o["id"] == order_id), None)
    if not order:
        return Response({"error": "Order not found"}, status=404)
    return Response(order)
