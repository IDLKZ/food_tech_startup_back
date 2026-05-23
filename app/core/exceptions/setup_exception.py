from fastapi import FastAPI

from app.core.exceptions.app_exception import AppException
from app.core.exceptions.http_exception import app_exception_handler


def setup_exception(app: FastAPI) -> None:
    app.add_exception_handler(AppException, app_exception_handler)