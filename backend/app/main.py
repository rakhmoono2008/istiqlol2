from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, jobs, profiles, courses, recommendations
from app.core.database import engine, Base
import app.models.base  # ensure models are registered

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Istiqlol API", version="1.0.0", docs_url="/docs")

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
app.include_router(recommendations.router, prefix="/recommendations",  tags=["ai"])

@app.get("/")
def root():
    return {"status": "ok", "platform": "Istiqlol — Women Career Platform"}
