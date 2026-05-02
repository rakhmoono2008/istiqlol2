from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.api import auth, jobs, profiles, courses, recommendations
from app.core.database import engine
from app.models import base

base.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Istiqlol API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,            prefix="/auth",            tags=["auth"])
app.include_router(jobs.router,            prefix="/jobs",            tags=["jobs"])
app.include_router(profiles.router,        prefix="/profile",         tags=["profile"])
app.include_router(courses.router,         prefix="/courses",         tags=["courses"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])

frontend_dist = os.path.join(
    os.path.dirname(__file__), "..", "..", "frontend", "dist"
)

if os.path.exists(frontend_dist):
    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/")
    def serve_index():
        return FileResponse(os.path.join(frontend_dist, "index.html"))

    @app.get("/{full_path:path}")
    def serve_spa(full_path: str):
        return FileResponse(os.path.join(frontend_dist, "index.html"))

else:
    @app.get("/")
    def root():
        return {"status": "ok", "platform": "Istiqlol"}
