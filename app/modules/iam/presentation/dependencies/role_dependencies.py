from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.database import get_write_session
from app.modules.iam.application.use_case.commands.create_role_use_case import CreateRoleUseCase
from app.shared.infrastructure.uow.sql_alchemy_uow import SqlAlchemyUoW
from app.modules.iam.infrastructure.repo_impl.role_repository_impl import RoleRepository


def get_role_repository(
    session: AsyncSession = Depends(get_write_session),
) -> RoleRepository:
    return RoleRepository(session)


def get_create_role_use_case(
    session: AsyncSession = Depends(get_write_session),
) -> CreateRoleUseCase:
    repo = RoleRepository(session)
    uow = SqlAlchemyUoW(session)
    return CreateRoleUseCase(repo, uow)