from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.middleware.locale_middleware import LocaleMiddleware


def setup_middleware(app: FastAPI) -> None:
    app.add_middleware(LocaleMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
