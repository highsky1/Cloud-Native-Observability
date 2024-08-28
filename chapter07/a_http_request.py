import requests
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.instrumentation.requests import RequestsInstrumentor

def configure_tracer():
    exporter = ConsoleSpanExporter()
    span_processor = BatchSpanProcessor(exporter)
    provider = TracerProvider()
    provider.add_span_processor(span_processor)
    trace.set_tracer_provider(provider)

def rename_span(span, request):
    span.update_name(f"Web Request {request.method}")

def add_response_attributes(span, request, response):
    span.set_attribute("http.response.headers", str(response.headers))

configure_tracer()
RequestsInstrumentor().instrument(
    request_hook=rename_span,
    response_hook=add_response_attributes,
)

url = "https://www.cloudnativeobservability.com"
resp = requests.get(url)
print(resp.status_code)