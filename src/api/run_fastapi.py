"""
Run FastAPI app
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

import uvicorn

from src.configurations.database import global_init
from src.api.routers import router


@asynccontextmanager
async def lifespan(application: FastAPI): # pylint: disable=unused-argument
    """
    Lifespan for FastAPI init
    """
    global_init()
    yield

if __name__ == "__main__":

    # Set up FastApi
    app = FastAPI(
        title="ETL project",
        description="",
        version="0.0.1",
        responses={404: {"description": "Not Found!"}},
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )

    # Set up router
    app.include_router(router)

    # Start Server
    uvicorn.run(app, host="0.0.0.0", port=8000)
