from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.analyzer.routers import router as analyzer_router
from config import get_settings

app = FastAPI(
    title="Table Recognition",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().ALLOW_ORIGINS,
)

@app.on_event("startup")
async def startup() -> None:
    settings = get_settings()

    app.dependency_overrides = {
        get_settings: lambda: settings,
    }

app.include_router(analyzer_router, tags=["Analyzer"], prefix="/api/analyzer")
