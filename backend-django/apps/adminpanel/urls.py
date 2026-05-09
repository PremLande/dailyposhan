from django.urls import path
from .views import admin_orders, update_order_status

urlpatterns = [
    path("orders", admin_orders),
    path("orders/<str:order_id>/status", update_order_status),
]
