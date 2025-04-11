# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from app.config import settings
from app.api import auth, courses, topics, lessons, users, progress, code_execution, games

# Create the FastAPI app with documentation settings
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for Pythonchick, an interactive Python learning platform for kids",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=None  # We'll create a custom endpoint for docs
)

# Set up CORS to allow requests from the frontend
origins = [
    "http://localhost",
    "http://localhost:3000",  # React frontend
    "http://frontend:3000",   # Docker service name
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(courses.router, prefix=settings.API_V1_STR)
app.include_router(topics.router, prefix=settings.API_V1_STR)
app.include_router(lessons.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)
app.include_router(progress.router, prefix=settings.API_V1_STR)
app.include_router(code_execution.router, prefix=settings.API_V1_STR)
app.include_router(games.router, prefix=settings.API_V1_STR)

# Mount static files if needed
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Redirect root to docs
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

# Custom Swagger UI
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        title=f"{settings.PROJECT_NAME} - API Documentation",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui.css",
    )

# Health check endpoint
@app.get("/health", include_in_schema=False)
def health_check():
    return {"status": "healthy", "message": "Pythonchick API is running"}