#!/usr/bin/env python3
import requests
from common import configure_tracer
from opentelemetry import context, trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
#from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
from local_machine_resource_detector import LocalMachineResourceDetector
from opentelemetry.semconv.trace import HttpFlavorValues, SpanAttributes
from opentelemetry.propagate import inject

def configure_tracer(name, version):
    exporter = ConsoleSpanExporter()
    span_processor = SimpleSpanProcessor(exporter)
    local_resource = LocalMachineResourceDetector().detect()
    resource = local_resource.merge(
        Resource.create(
            {
                "service.name": name,
                "service.version": version,
            }
        )
    )
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(span_processor)
    trace.set_tracer_provider(provider)
    return trace.get_tracer(name, version)

tracer = configure_tracer("shopper", "0.1.2")

@tracer.start_as_current_span("browse")
def browse():
    print("visiting the grocery store")
    #add_item_to_cart("orange")
    with tracer.start_as_current_span(
        "web request", kind=trace.SpanKind.CLIENT
    ) as span:
        url = "http://localhost:5000/products"
        #span = trace.get_current_span()
        span.set_attributes(
            {
                SpanAttributes.HTTP_METHOD: "GET",
                SpanAttributes.HTTP_FLAVOR: str(HttpFlavorValues.HTTP_1_1),
                SpanAttributes.HTTP_URL: url,
                SpanAttributes.NET_PEER_IP: "127.0.0.1",
            }
        )
        headers = {}
        inject(headers)
        resp = requests.get(url)
        span.set_attribute(SpanAttributes.HTTP_STATUS_CODE,resp.status_code)
    #span.set_attributes(
    #    {
    #        "http.method": "GET",
    #        "http.flavor": "1.1",
    #        "http.url": "http://localhost:5000",
    #        "net.peer.ip": "127.0.0.1",
    #    }
    #)
    #span.set_attribute("http.method", "GET")
    #span.set_attribute("http.flavor", "1.1")
    #span.set_attribute("http.url", "http://localhost:5000")
    #span.set_attribute("net.peer.ip", "127.0.0.1")

@tracer.start_as_current_span("add item to cart")
def add_item_to_cart(item, quantity):
    span = trace.get_current_span()
    span.set_attribute(
        {
            "item": item,
            "quantity": quantity,
        }
    )
    print("add {} to cart".format(item))

@tracer.start_as_current_span("visit store")
def visit_store():
    browse()

if __name__ == "__main__":
    visit_store()
    tracer = configure_tracer("shopper", "0.1.2")
    #tracer = configure_tracer()
    #with tracer.start_as_current_span("visit store"):
    #    with tracer.start_as_current_span("browse"):
    #        browse()
    #        with tracer.start_as_current_span("add item to cart"):
    #            add_item_to_cart("orange")
    #span = tracer.start_span("visit store")
    #ctx = trace.set_span_in_context(span)
    #token = context.attach(ctx)
    #span2 = tracer.start_span("browse")
    #browse()
    #span2.end()
    #context.detach(token)
    #span.end()