from fastapi import FastAPI

from app.modules.iam.presentation.controller.role_controller import RoleController


def register_routers(app: FastAPI) -> None:
    # IAM
    role_controller = RoleController()
    app.include_router(
        role_controller.router,
        prefix="/api/v1/roles",
        tags=["IAM - Roles"],
    )