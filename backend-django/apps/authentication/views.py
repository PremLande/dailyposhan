from rest_framework.decorators import api_view
from rest_framework.response import Response

USERS = [
    {"id": 1, "name": "Admin", "email": "admin@dailyposhan.in", "password": "admin123", "role": "admin"}
]


@api_view(["POST"])
def register(request):
    email = request.data.get("email", "").strip().lower()
    if any(u["email"] == email for u in USERS):
        return Response({"error": "Email already registered"}, status=400)
    user = {
        "id": len(USERS) + 1,
        "name": request.data.get("name", "Customer"),
        "email": email,
        "password": request.data.get("password", ""),
        "role": "customer",
    }
    USERS.append(user)
    return Response({"id": user["id"], "name": user["name"], "email": user["email"], "role": user["role"]})


@api_view(["POST"])
def login(request):
    email = request.data.get("email", "").strip().lower()
    password = request.data.get("password", "")
    user = next((u for u in USERS if u["email"] == email and u["password"] == password), None)
    if not user:
        return Response({"error": "Invalid credentials"}, status=401)
    return Response({"id": user["id"], "name": user["name"], "email": user["email"], "role": user["role"]})
