from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Payment, Address


@api_view(["POST"])
def create_payment(request):
    """Create a payment record"""
    try:
        order_id = request.data.get("order_id", "")
        method = request.data.get("method", "cod")
        amount = request.data.get("amount", 0)

        if not order_id:
            return Response(
                {"error": "Order ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        payment = Payment.objects.create(
            order_id=order_id,
            method=method,
            amount=amount,
            status="Pending" if method == "cod" else "Processing"
        )

        return Response({
            "payment_id": payment.id,
            "order_id": payment.order_id,
            "method": payment.method,
            "status": payment.status,
            "amount": payment.amount,
            "message": "Payment created successfully"
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
def verify_payment(request):
    """Verify/Update payment status"""
    try:
        payment_id = request.data.get("payment_id", "")
        transaction_id = request.data.get("transaction_id", "")
        new_status = request.data.get("status", "")

        payment = Payment.objects.filter(id=payment_id).first()
        if not payment:
            return Response(
                {"error": "Payment not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if transaction_id:
            payment.transaction_id = transaction_id
        if new_status:
            payment.status = new_status

        payment.save()

        return Response({
            "payment_id": payment.id,
            "order_id": payment.order_id,
            "status": payment.status,
            "verified": True,
            "message": "Payment verified successfully"
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def get_payment(request, payment_id):
    """Get payment details"""
    try:
        payment = Payment.objects.filter(id=payment_id).first()
        if not payment:
            return Response(
                {"error": "Payment not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({
            "id": payment.id,
            "order_id": payment.order_id,
            "method": payment.method,
            "status": payment.status,
            "amount": payment.amount,
            "transaction_id": payment.transaction_id,
            "created_at": payment.created_at,
            "updated_at": payment.updated_at
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
def save_address(request):
    """Save customer address"""
    try:
        address = Address.objects.create(
            customer_name=request.data.get("customer_name", ""),
            phone=request.data.get("phone", ""),
            full_address=request.data.get("full_address", ""),
            pincode=request.data.get("pincode", ""),
            is_default=request.data.get("is_default", False)
        )

        return Response({
            "id": address.id,
            "customer_name": address.customer_name,
            "pincode": address.pincode,
            "message": "Address saved successfully"
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def get_addresses(request, customer_name=None):
    """Get addresses for customer"""
    try:
        if customer_name:
            addresses = Address.objects.filter(customer_name=customer_name).values(
                'id', 'customer_name', 'phone', 'full_address', 'pincode', 'is_default'
            )
        else:
            addresses = Address.objects.all().values(
                'id', 'customer_name', 'phone', 'full_address', 'pincode', 'is_default'
            )

        return Response(list(addresses), status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["PUT"])
def update_address(request, address_id):
    """Update address"""
    try:
        address = Address.objects.filter(id=address_id).first()
        if not address:
            return Response(
                {"error": "Address not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if "phone" in request.data:
            address.phone = request.data["phone"]
        if "full_address" in request.data:
            address.full_address = request.data["full_address"]
        if "pincode" in request.data:
            address.pincode = request.data["pincode"]
        if "is_default" in request.data:
            address.is_default = request.data["is_default"]

        address.save()

        return Response({
            "id": address.id,
            "message": "Address updated successfully"
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["DELETE"])
def delete_address(request, address_id):
    """Delete address"""
    try:
        address = Address.objects.filter(id=address_id).first()
        if not address:
            return Response(
                {"error": "Address not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        address.delete()

        return Response(
            {"message": "Address deleted successfully"},
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
