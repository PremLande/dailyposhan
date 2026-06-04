from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product


@api_view(["GET"])
def products(request):
    """Get all active products"""
    try:
        products_list = Product.objects.filter(is_active=True).values(
            'id', 'name', 'price', 'calories', 'protein', 'description', 
            'image_url', 'stock', 'created_at'
        )
        return Response(list(products_list), status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def product_by_id(request, product_id):
    """Get product by ID"""
    try:
        product = Product.objects.filter(id=product_id, is_active=True).first()
        if not product:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "calories": product.calories,
            "protein": product.protein,
            "description": product.description,
            "image_url": product.image_url,
            "stock": product.stock,
            "is_active": product.is_active,
            "created_at": product.created_at
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
def create_product(request):
    """Create a new product (admin only)"""
    try:
        product = Product.objects.create(
            name=request.data.get("name", ""),
            price=request.data.get("price", 0),
            calories=request.data.get("calories"),
            protein=request.data.get("protein"),
            description=request.data.get("description"),
            image_url=request.data.get("image_url"),
            stock=request.data.get("stock", 0),
            is_active=request.data.get("is_active", True)
        )
        return Response({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "message": "Product created successfully"
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["PUT"])
def update_product(request, product_id):
    """Update product"""
    try:
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Update fields if provided
        if "name" in request.data:
            product.name = request.data["name"]
        if "price" in request.data:
            product.price = request.data["price"]
        if "calories" in request.data:
            product.calories = request.data["calories"]
        if "protein" in request.data:
            product.protein = request.data["protein"]
        if "description" in request.data:
            product.description = request.data["description"]
        if "image_url" in request.data:
            product.image_url = request.data["image_url"]
        if "stock" in request.data:
            product.stock = request.data["stock"]
        if "is_active" in request.data:
            product.is_active = request.data["is_active"]

        product.save()
        return Response({
            "id": product.id,
            "message": "Product updated successfully"
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["DELETE"])
def delete_product(request, product_id):
    """Soft delete product"""
    try:
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        product.is_active = False
        product.save()
        return Response(
            {"message": "Product deleted successfully"},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
