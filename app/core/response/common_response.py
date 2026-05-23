from typing import TypeVar, Optional, Generic

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponseError(BaseModel):
    inner_code: Optional[int] = None
    message: Optional[str] = None
    detail: Optional[str] = None
    validation_errors: Optional[dict[str, str]] = None
    error_trace: Optional[str] = None

class ApiCommonResponse(BaseModel, Generic[T]):
    message: Optional[str] = None
    data: T
    code: Optional[int] = None
    error: Optional[ApiResponseError] = None

    @classmethod
    def ok(
        cls,
        data: T,
        message: Optional[str] = None,
        code: int = 200,
    ) -> "ApiCommonResponse[T]":
        return cls(message=message, data=data, code=code, error=None)

    @classmethod
    def fail(
        cls,
        message: Optional[str] = None,
        inner_code: Optional[int] = None,
        detail: Optional[str] = None,
        validation_errors: Optional[dict[str, str]] = None,
        error_trace: Optional[str] = None,
        code: int = 400,
    ) -> "ApiCommonResponse[EmptyData]":
        return cls(
            message=message,
            data=EmptyData(),
            code=code,
            error=ApiResponseError(
                inner_code=inner_code,
                message=message,
                detail=detail,
                validation_errors=validation_errors,
                error_trace=error_trace,
            ),
        )


class EmptyData(BaseModel):
    empty: bool = True