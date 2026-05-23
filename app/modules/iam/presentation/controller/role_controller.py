# app/modules/iam/presentation/controllers/role_controller.py
from fastapi import APIRouter, Depends, status

from app.core.response.common_response import ApiCommonResponse
from app.modules.iam.application.use_case.commands.create_role_use_case import CreateRoleUseCase, CreateRoleCommand
from app.modules.iam.presentation.schemas.role_schema import CreateRoleSchema
from app.modules.iam.presentation.dependencies.role_dependencies import (
    get_create_role_use_case,
)


class RoleController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.post(
            "/create",
            status_code=status.HTTP_201_CREATED,
            summary="Создать роль",
        )(self.create)

    async def create(
        self,
        body: CreateRoleSchema,
        use_case: CreateRoleUseCase = Depends(get_create_role_use_case),
    ) -> ApiCommonResponse[dict]:
        result = await use_case.execute(
            CreateRoleCommand(
                title_ru=body.title_ru,
                title_kk=body.title_kk,
                title_en=body.title_en,
                description_ru=body.description_ru,
                description_kk=body.description_kk,
                description_en=body.description_en,
                value=body.value,
            )
        )
        return ApiCommonResponse.ok(
            data={"role_id": str(result.role_id)},
            message="Роль успешно создана",
        )