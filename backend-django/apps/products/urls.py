from django.urls import path
from .views import products, product_by_id

urlpatterns = [
    path("", products),
    path("<int:product_id>/", product_by_id),
]
