import time, logging
from opentelemetry.sdk._logs.export import ConsoleLogExporter, BatchLogRecordProcessor
from opentelemetry.sdk._logs import LoggerProvider, LogRecord, LoggingHandler
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk.resources import Resource
from opentelemetry._logs import (
    set_logger_provider,
    get_logger_provider,
)
from opentelemetry._logs.severity import SeverityNumber

def configure_logger_provider():
    provider = LoggerProvider(resource=Resource.create())
    set_logger_provider(provider)
    exporter = ConsoleLogExporter()
    provider.add_log_record_processor(BatchLogRecordProcessor(exporter))

if __name__ == "__main__":
    configure_logger_provider()
    logger = logging.getLogger(__file__)
    logger.setLevel(logging.DEBUG)
    handler = LoggingHandler()
    logger.addHandler(handler)
    logger.info("second log line")
    #logger.warning("second log line", extra={"key1": "val1"})
    #logger = get_logger_provider().get_logger(
    #    "shopper",
    #    "0.1.2",
    #)
    #logger.emit(
    #    LogRecord(
    #        timestamp=time.time_ns(),
    #        body="first log line",
    #        severity_number=SeverityNumber.INFO,
    #    )
    #)
