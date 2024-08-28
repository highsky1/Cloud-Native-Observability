import requests

from opentelemetry.instrumentation.requests import RequestsInstrumentor

def rename_span(span, request):
    span.update_name(f"Web Request {request.method}")

def add_response_attributes(span, request, response):
    span.set_attribute("http.response.headers", str(response.headers))

#configure_tracer()
RequestsInstrumentor().uninstrument()
RequestsInstrumentor().instrument(
    request_hook=rename_span,
    response_hook=add_response_attributes,
)

resp = requests.get("https://www.cloudnativeobservability.com")
print(resp.status_code)