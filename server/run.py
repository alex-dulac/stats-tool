from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app import settings
from app.router import router
from app.db import session_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await session_manager.init_db()
    yield
    await session_manager.close_db()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.WEB_APP_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app="run:app", host="0.0.0.0", port=8000, reload=True)

