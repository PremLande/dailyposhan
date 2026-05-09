from rest_framework.decorators import api_view
from rest_framework.response import Response

PRODUCTS = [
    {"id": 1, "name": "Muscle Fuel Jar", "price": 249, "calories": 420, "protein": "34g"},
    {"id": 2, "name": "Glow & Flow Jar", "price": 229, "calories": 310, "protein": "14g"},
    {"id": 3, "name": "Chatori Jar", "price": 199, "calories": 260, "protein": "12g"},
]


@api_view(["GET"])
def products(request):
    return Response(PRODUCTS)


@api_view(["GET"])
def product_by_id(request, product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        return Response({"error": "Product not found"}, status=404)
    return Response(product)
