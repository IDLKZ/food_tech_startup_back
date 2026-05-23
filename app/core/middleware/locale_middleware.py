# app/shared/middleware/locale_middleware.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

SUPPORTED_LANGS = ("ru", "kk", "en")
DEFAULT_LANG = "ru"


class LocaleMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.lang = self._resolve_lang(request)
        response = await call_next(request)
        return response

    def _resolve_lang(self, request: Request) -> str:
        # 1. query param
        lang = request.query_params.get("lang")
        if lang in SUPPORTED_LANGS:
            return lang

        # 2. Accept-Language header
        accept_lang = request.headers.get("Accept-Language", "")
        for part in accept_lang.split(","):
            code = part.strip().split(";")[0][:2].lower()
            if code in SUPPORTED_LANGS:
                return code

        return DEFAULT_LANG