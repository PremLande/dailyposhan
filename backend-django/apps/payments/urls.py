from django.urls import path
from .views import create_payment, verify_payment

urlpatterns = [
    path("create", create_payment),
    path("verify", verify_payment),
]
