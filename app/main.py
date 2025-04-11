import sys
import traceback

try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.openapi.docs import get_swagger_ui_html
    from fastapi.responses import RedirectResponse

    from app.config import settings
    from app.api import (
        auth, 
        courses, 
        topics, 
        lessons, 
        users, 
        progress, 
        code_execution, 
        games
    )

    # Create the FastAPI app
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="API for Pythonchick, an interactive Python learning platform for kids",
        version="1.0.0",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=None
    )

    # CORS configuration
    origins = [
        "http://localhost",
        "http://localhost:3000",
        "http://frontend:3000",
        "http://127.0.0.1:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(auth.router, prefix=settings.API_V1_STR)
    app.include_router(courses.router, prefix=settings.API_V1_STR)
    app.include_router(topics.router, prefix=settings.API_V1_STR)
    app.include_router(lessons.router, prefix=settings.API_V1_STR)
    app.include_router(users.router, prefix=settings.API_V1_STR)
    app.include_router(progress.router, prefix=settings.API_V1_STR)
    app.include_router(code_execution.router, prefix=settings.API_V1_STR)
    app.include_router(games.router, prefix=settings.API_V1_STR)

    # Redirect root to docs
    @app.get("/", include_in_schema=False)
    async def root():
        return RedirectResponse(url="/docs")

    # Custom Swagger UI
    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=f"{settings.API_V1_STR}/openapi.json",
            title=f"{settings.PROJECT_NAME} - API Documentation"
        )

except Exception as e:
    print(f"Error importing modules: {e}")
    print(traceback.format_exc())
    raise