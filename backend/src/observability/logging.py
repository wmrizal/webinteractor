from __future__ import annotations

import json
import logging
import os
from typing import Any

LOG_FORMAT = "%(message)s"
_DEFAULT_LEVEL = "INFO"


class StructuredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if hasattr(record, "event"):
            payload["event"] = record.event
        if hasattr(record, "context"):
            payload["context"] = record.context

        return json.dumps(payload, default=str)


def configure_logging() -> None:
    root_logger = logging.getLogger()
    if root_logger.handlers:
        return

    handler = logging.StreamHandler()
    handler.setFormatter(StructuredFormatter(LOG_FORMAT))
    root_logger.addHandler(handler)
    root_logger.setLevel(os.getenv("LOG_LEVEL", _DEFAULT_LEVEL).upper())


def get_logger(name: str) -> logging.Logger:
    configure_logging()
    return logging.getLogger(name)
