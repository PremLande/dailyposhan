from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["POST"])
def create_payment(request):
    method = request.data.get("method", "cod")
    payment_id = "PAY123456"
    status = "Pending COD" if method == "cod" else "Paid"
    return Response({"payment_id": payment_id, "status": status})


@api_view(["POST"])
def verify_payment(request):
    payment_id = request.data.get("payment_id", "")
    return Response({"payment_id": payment_id, "verified": True})
