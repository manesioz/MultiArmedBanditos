import logging
from typing import Dict, Any

# Logging configuration
LOG_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": True
        }
    }
}

# API settings
API_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "reload": True
}

# Default strategy settings
EPSILON_GREEDY_DEFAULT_EPSILON = 0.1