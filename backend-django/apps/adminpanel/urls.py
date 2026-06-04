from django.urls import path
from .views import admin_orders, update_order_status, admin_dashboard_stats

urlpatterns = [
    path("orders/", admin_orders, name="admin_orders"),
    path("orders/<str:order_id>/status/", update_order_status, name="update_order_status"),
    path("dashboard/stats/", admin_dashboard_stats, name="admin_dashboard_stats"),
]
