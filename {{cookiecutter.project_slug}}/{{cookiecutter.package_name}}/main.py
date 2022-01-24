import traceback
import logging
import pathlib
import time
import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette_exporter import PrometheusMiddleware, handle_metrics
from starlette.exceptions import ExceptionMiddleware
from starlette.responses import JSONResponse
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from {{cookiecutter.project_slug}}.api import {{cookiecutter.project_slug}}, info
from {{cookiecutter.project_slug}}.exception import UnauthorizedAccess
from {{cookiecutter.project_slug}}.config import GCONFIG
from {{cookiecutter.project_slug}}.exception import {{cookiecutter.baseclass}}Exception


logger = logging.getLogger(__name__)


if "url" in GCONFIG.sentry:
    sentry_sdk.init(  # pylint: disable=abstract-class-instantiated # noqa: E0110
        dsn=GCONFIG.sentry["url"],
        traces_sample_rate=1.0,
        environment=GCONFIG.sentry["environment"],
    )


app = FastAPI()


def _create_tmp_dir():
    pathlib.Path(GCONFIG.{{cookiecutter.project_slug}}["download_dir"]).mkdir(parents=True, exist_ok=True)
    pathlib.Path(GCONFIG.{{cookiecutter.project_slug}}["prometheus_dir"]).mkdir(
        parents=True, exist_ok=True
    )


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


async def add_check_token(request: Request, call_next):
    if GCONFIG.{{cookiecutter.project_slug}}["token"] and (
        "token" not in request.headers
        or request.headers["token"] != GCONFIG.{{cookiecutter.project_slug}}["token"]
    ):
        raise UnauthorizedAccess("NoAuth")
    return await call_next(request)


def exception_handler(exc: Exception, message: str, status: int, request: Request):
    logger.error(exc)
    logger.error("".join(traceback.format_exception(type(exc), exc, exc.__traceback__)))
    request_dict = {
        "url": str(request.url),
        "method": request.method,
        "headers": dict(request.headers.items()),
        "params": dict(request.query_params),
    }

    return JSONResponse(
        content={
            "message": message,
            "request": request_dict,
            "status": status,
        },
        status_code=status,
    )


@app.exception_handler(Exception)
async def any_exception_handler(request: Request, exc: Exception):
    msg = f"Exception Occurred: {exc!r}"
    return exception_handler(exc, msg, 500, request)


@app.exception_handler({{cookiecutter.baseclass}}Exception)
async def custom_exception_handler(request: Request, exc: {{cookiecutter.baseclass}}Exception):
    return exception_handler(exc, exc.to_dict(), exc.status_code, request)


_create_tmp_dir()
app.add_middleware(PrometheusMiddleware, app_name="{{cookiecutter.project_slug}}")
app.add_middleware(ProxyHeadersMiddleware)
app.add_middleware(SentryAsgiMiddleware)
if "cors" in GCONFIG.fastapi["middlewares"]:
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=GCONFIG.fastapi["cors"]["allow_origin_regex"],
        allow_origins=GCONFIG.fastapi["cors"]["allow_origins"],
        allow_credentials=GCONFIG.fastapi["cors"]["allow_credentials"],
        allow_methods=GCONFIG.fastapi["cors"]["allow_methods"],
        allow_headers=GCONFIG.fastapi["cors"]["allow_headers"],
    )
if "tokenAuth" in GCONFIG.fastapi["middlewares"]:
    app.middleware("http")(add_check_token)

app.add_middleware(ExceptionMiddleware, handlers=app.exception_handlers)
app.add_route("/metrics", handle_metrics)
app.include_router(info.router)
app.include_router({{cookiecutter.project_slug}}.router)
