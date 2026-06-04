from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User


@api_view(["POST"])
def register(request):
    """Register a new user"""
    try:
        email = request.data.get("email", "").strip().lower()
        name = request.data.get("name", "Customer").strip()
        password = request.data.get("password", "")

        if not email or not password:
            return Response(
                {"error": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if user already exists
        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already registered"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create new user
        user = User.objects.create(
            name=name,
            email=email,
            role="customer"
        )
        user.set_password(password)
        user.save()

        return Response({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
def login(request):
    """Authenticate user"""
    try:
        email = request.data.get("email", "").strip().lower()
        password = request.data.get("password", "")

        if not email or not password:
            return Response(
                {"error": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Find user by email
        user = User.objects.filter(email=email).first()

        if not user or not user.check_password(password):
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def get_all_users(request):
    """Get all users (admin only)"""
    try:
        users = User.objects.all().values('id', 'name', 'email', 'role', 'created_at')
        return Response(list(users), status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def get_user(request, user_id):
    """Get user by ID"""
    try:
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
