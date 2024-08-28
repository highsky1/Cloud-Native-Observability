#!/usr/bin/env python3
from logging.config import dictConfig
import requests
from flask import Flask
from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry._logs import set_logger_provider

logger_provider = LoggerProvider()
set_logger_provider(logger_provider)

dictConfig(
    {
        "version": 1,
        "handlers": {
            "otlp": {
                "class": "opentelemetry.sdk._logs.LoggingHandler",
            }
        },
        "root": {"level": "DEBUG", "handlers": ["otlp"]},
    }
)
app = Flask(__name__)
app.wsgi_app = OpenTelemetryMiddleware(app.wsgi_app)


@app.route("/")
def welcome():
    return "Welcome to the grocery store!"


@app.route("/products")
def products():
    url = "http://localhost:5001/inventory"
    resp = requests.get(url)
    return resp.text


if __name__ == "__main__":
    app.run(port=5000)
