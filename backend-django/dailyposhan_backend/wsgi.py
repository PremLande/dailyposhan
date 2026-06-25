import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyposhan_backend.settings")

# Initialize OpenTelemetry
from dailyposhan_backend.otel_init import init_telemetry
init_telemetry()

application = get_wsgi_application()
