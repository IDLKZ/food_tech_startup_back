from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions.app_exception import AppException
from app.core.locales.local_provider import translate
from app.core.response.common_response import ApiCommonResponse


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    lang = getattr(request.state, "lang", "ru")
    settings = request.app.state.container.settings()
    message = translate(exc.message_key, lang, *exc.args_values)

    response = ApiCommonResponse.fail(
        message=message,
        inner_code=exc.inner_code,
        code=exc.status_code,
        error_trace=str(exc) if settings.debug else None,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump(),
    )