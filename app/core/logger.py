import logging
import json
from datetime import datetime

from app.core.config import settings


class JsonFormatter(logging.Formatter):
    """
    Custom logging formatter to output logs in JSON format.
    for using later in any log processing systems
    """

    def format(self, record: logging.LogRecord) -> str:
        log_message = {
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "file": record.filename,
            "line": record.lineno,
        }

        if record.exc_info:
            log_message["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_message)


class Logger:
    def __init__(self, log_level=settings.LOG_LEVEL, log_format=settings.LOG_FORMAT):
        self.log_level = log_level
        self.log_format = log_format
        self.logger = self.configure_logging()
        self.logger.info('Logger initialized')

    def get_logger(self) -> logging.Logger:
        return self.logger

    def configure_logging(self) -> logging.Logger:
        """
        Configures the logging system with the specified log level.

        Returns:
            A logger instance configured with JSON formatting.
        """
        log_level: int = getattr(logging, self.log_level.upper(), logging.INFO)
        logger_ = logging.getLogger(__name__)
        logger_.setLevel(log_level)

        if logger_.hasHandlers():
            logger_.handlers.clear()

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(JsonFormatter())
        logger_.addHandler(stream_handler)

        file_handler = logging.FileHandler(settings.LOG_FILE_PATH)
        file_handler.setFormatter(JsonFormatter())
        logger_.addHandler(file_handler)

        return logger_


LOG_LEVEL = settings.LOG_LEVEL
LOG_FORMAT = settings.LOG_FORMAT
module_logger = Logger(log_level=LOG_LEVEL).get_logger()


if __name__ == "__main__":
    logger = Logger().get_logger()
    logger.error("This is an error message")
    logger.warning("This is a warning message")
    logger.info("This is an info message")
    logger.debug("This is a debug message")
    logger.critical("This is a critical message")
