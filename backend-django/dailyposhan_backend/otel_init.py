import os
from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor


def init_telemetry():
    otel_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4317")
    service_name = os.getenv("OTEL_SERVICE_NAME", "dailyposhan-backend")
    service_version = os.getenv("OTEL_SERVICE_VERSION", "1.0.0")

    resource = Resource.create(
        {
            SERVICE_NAME: service_name,
            SERVICE_VERSION: service_version,
            "deployment.environment": os.getenv("OTEL_DEPLOYMENT_ENVIRONMENT", "development"),
        }
    )

    otlp_trace_exporter = OTLPSpanExporter(endpoint=otel_endpoint)
    trace_provider = TracerProvider(resource=resource)
    trace_provider.add_span_processor(BatchSpanProcessor(otlp_trace_exporter))
    trace.set_tracer_provider(trace_provider)

    otlp_metric_exporter = OTLPMetricExporter(endpoint=otel_endpoint)
    metric_reader = PeriodicExportingMetricReader(otlp_metric_exporter)
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)

    DjangoInstrumentor().instrument()
    RequestsInstrumentor().instrument()
