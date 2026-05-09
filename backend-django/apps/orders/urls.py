from django.urls import path
from .views import create_order, order_by_id

urlpatterns = [
    path("", create_order),
    path("<str:order_id>/", order_by_id),
]
