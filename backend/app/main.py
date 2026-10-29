import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.config import settings
from app.core.database import engine, Base, SessionLocal
from app.models.models import User
from app.seed_data import seed_database

# Import routers
from app.api.auth import router as auth_router
from app.api.profiles import router as profiles_router
from app.api.recommendations import router as recommendations_router
from app.api.connections import router as connections_router
from app.api.messages import router as messages_router
from app.api.mentorship import router as mentorship_router
from app.api.jobs import router as jobs_router
from app.api.events import router as events_router
from app.api.notifications import router as notifications_router
from app.api.admin import router as admin_router
from app.api.ai_assistant import router as ai_assistant_router

# Initialize tables
Base.metadata.create_all(bind=engine)

# Auto seed database on startup only if database is fresh/empty
db = SessionLocal()
try:
    if db.query(User).count() == 0:
        seed_database(db)
finally:
    db.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Production-grade AI-Powered Alumni Networking Platform with Personalized Connection Recommendations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(profiles_router, prefix=settings.API_V1_STR)
app.include_router(recommendations_router, prefix=settings.API_V1_STR)
app.include_router(connections_router, prefix=settings.API_V1_STR)
app.include_router(messages_router, prefix=settings.API_V1_STR)
app.include_router(mentorship_router, prefix=settings.API_V1_STR)
app.include_router(jobs_router, prefix=settings.API_V1_STR)
app.include_router(events_router, prefix=settings.API_V1_STR)
app.include_router(notifications_router, prefix=settings.API_V1_STR)
app.include_router(admin_router, prefix=settings.API_V1_STR)
app.include_router(ai_assistant_router, prefix=settings.API_V1_STR)

FRONTEND_DIST = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "recommendation_engine": "active"
    }

# Mount static assets and serve Single-Page Application (SPA) directly as a complete website
if FRONTEND_DIST.exists() and (FRONTEND_DIST / "assets").exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")

@app.get("/{full_path:path}")
def serve_frontend_spa(full_path: str = ""):
    # Do not intercept API, docs, or OpenAPI schema endpoints
    if full_path.startswith("api") or full_path.startswith("docs") or full_path.startswith("redoc") or full_path.startswith("openapi.json"):
        raise HTTPException(status_code=404, detail="Not Found")
    
    if FRONTEND_DIST.exists():
        target_file = FRONTEND_DIST / full_path
        if full_path and target_file.is_file():
            return FileResponse(target_file)
        index_file = FRONTEND_DIST / "index.html"
        if index_file.exists():
            return FileResponse(index_file)

    return {
        "platform": "Alumnia — Connect Beyond Graduation",
        "status": "online",
        "version": "1.0.0",
        "api_docs": "/docs",
        "tagline": "Generative AI Based Alumni Networking Platform with Personalized Connection Recommendations"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
