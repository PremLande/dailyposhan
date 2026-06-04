from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from apps.orders.models import Order, OrderItem


@api_view(["GET"])
def admin_orders(request):
    """Get all orders for admin dashboard"""
    try:
        orders = Order.objects.all().order_by('-created_at')
        orders_data = []

        for order in orders:
            items_count = OrderItem.objects.filter(order=order).count()
            orders_data.append({
                "id": order.id,
                "customer_name": order.customer_name,
                "phone": order.phone,
                "total": order.total,
                "status": order.status,
                "payment_status": order.payment_status,
                "created_at": order.created_at,
                "items_count": items_count
            })

        return Response(orders_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["PUT"])
def update_order_status(request, order_id):
    """Update order status by admin"""
    try:
        order = Order.objects.filter(id=order_id).first()
        if not order:
            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        new_status = request.data.get("status")
        if new_status:
            order.status = new_status
            order.save()

        return Response({
            "id": order.id,
            "status": order.status,
            "message": "Order status updated successfully"
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def admin_dashboard_stats(request):
    """Get dashboard statistics for admin"""
    try:
        total_orders = Order.objects.count()
        pending_orders = Order.objects.filter(status='Pending').count()
        delivered_orders = Order.objects.filter(status='Delivered').count()
        total_revenue = Order.objects.filter(payment_status='Paid').aggregate(
            total=models.Sum('total')
        )['total'] or 0

        return Response({
            "total_orders": total_orders,
            "pending_orders": pending_orders,
            "delivered_orders": delivered_orders,
            "total_revenue": total_revenue
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
