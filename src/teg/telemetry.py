"""OTel initialization: traces / metrics / logs are all sent via OTLP HTTP.

Same setup as taruza's telemetry.py, so teg shows up in the same LGTM stack.
Read from environment variables (standard SDK behavior):
  OTEL_SERVICE_NAME              -> resource's service.name
  OTEL_RESOURCE_ATTRIBUTES       -> other resource attributes
  OTEL_EXPORTER_OTLP_ENDPOINT    -> e.g. http://lgtm:4318 (the exporter appends paths like /v1/traces itself)
"""

from fastapi import FastAPI
from opentelemetry import metrics, trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def setup() -> None:
    # Resource.create() automatically merges OTEL_SERVICE_NAME / OTEL_RESOURCE_ATTRIBUTES.
    resource = Resource.create()

    # --- traces ---
    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    trace.set_tracer_provider(tracer_provider)

    # --- metrics ---
    reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(), export_interval_millis=10_000
    )
    metrics.set_meter_provider(
        MeterProvider(resource=resource, metric_readers=[reader])
    )

    # --- logs ---
    logger_provider = LoggerProvider(resource=resource)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter()))
    set_logger_provider(logger_provider)

    # LoggingInstrumentor does two things:
    #   1. Attaches an OTel handler to the root logger (standard logging records ->
    #      OTel logs, with trace_id / span_id)
    #   2. inject_trace_context=True: adds otelTraceID / otelSpanID to every record,
    #      which log.ini's format prints ("0" outside a span). Records logged before
    #      this runs don't have them; JsonFormatter writes null for those instead
    #      of failing.
    # No set_logging_format: it only adds a logging.basicConfig() call, which is a
    # no-op once --log-config has set up root, so output keeps log.ini's format.
    # log_code_attributes=True: the handler drops funcName / lineno / pathname,
    # so send them as code.function.name / code.line.number / code.file.path.
    LoggingInstrumentor().instrument(
        inject_trace_context=True, log_code_attributes=True
    )


def instrument_app(app: FastAPI) -> None:
    # Inbound HTTP: one server span per request, linked to the caller's trace
    # (e.g. taruza) via the traceparent header.
    # healthz / metrics are polled, so they'd only add noise.
    FastAPIInstrumentor.instrument_app(
        app, excluded_urls="healthz,metrics", exclude_spans=["send", "receive"]
    )
