from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.orders.views import ORDERS


@api_view(["GET"])
def admin_orders(request):
    return Response(ORDERS)


@api_view(["PUT"])
def update_order_status(request, order_id):
    status = request.data.get("status")
    order = next((o for o in ORDERS if o["id"] == order_id), None)
    if not order:
        return Response({"error": "Order not found"}, status=404)
    order["status"] = status
    return Response(order)
