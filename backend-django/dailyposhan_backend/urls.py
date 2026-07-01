from django.contrib import admin
from django.urls import include, path

from dailyposhan_backend.health import health_check

urlpatterns = [
    path("api/health/", health_check, name="health-check"),
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.authentication.urls")),
    path("api/products/", include("apps.products.urls")),
    path("api/orders/", include("apps.orders.urls")),
    path("api/payments/", include("apps.payments.urls")),
    path("api/admin/", include("apps.adminpanel.urls")),
]
