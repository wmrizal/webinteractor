from __future__ import annotations

import json
import logging
import os
import re
from typing import Any

LOG_FORMAT = "%(message)s"
_DEFAULT_LEVEL = "INFO"

_SECRET_PATTERNS = [
    re.compile(r"(?i)(password|passwd|secret|token|apikey|api_key|authorization)\s*[=:]\s*\S+"),
    re.compile(r"(?i)Bearer\s+\S+"),
]
_REDACTION_PLACEHOLDER = "[REDACTED]"


def _redact(value: str) -> str:
    for pattern in _SECRET_PATTERNS:
        value = pattern.sub(lambda m: m.group(0).split("=")[0] + "=" + _REDACTION_PLACEHOLDER, value)
    return value


class StructuredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "level": record.levelname,
            "logger": record.name,
            "message": _redact(record.getMessage()),
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
