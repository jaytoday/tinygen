import logging
import logging.config

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router

app = FastAPI()


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
)

app.include_router(api_router, prefix="/api/v1")

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO", 
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["console"],
            "level": "INFO", 
            "propagate": False,
        },
    },
}
logging.config.dictConfig(logging_config)
