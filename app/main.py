from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
import uvicorn
from app.core.di.app_di_container import Container
from app.core.exceptions.common_exceptions import ApiBadRequestException
from app.core.exceptions.setup_exception import setup_exception
from app.core.locales.locale_keys import LocaleKeys
from app.core.middleware.middleware_setup import setup_middleware
from app.core.response.common_response import ApiCommonResponse
from app.core.route.register_route import register_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    container = Container()
    container.wire(packages=["app"])
    app.state.container = container
    yield
    await container.write_engine().dispose()
    await container.read_engine().dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Food Tech Startup",
        description="Clean Architecture implementation",
        lifespan=lifespan,
    )
    setup_middleware(app)
    setup_exception(app)
    register_routers(app)

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)