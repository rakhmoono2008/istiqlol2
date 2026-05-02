from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.base import Course, Biography

router = APIRouter()

@router.get("/")
def list_courses(db: Session = Depends(get_db)):
    rows = db.query(Course).all()
    return [{
        "id": c.id, "title": c.title, "description": c.description,
        "category": c.category, "duration_hours": c.duration_hours,
        "has_certificate": c.has_certificate, "thumbnail_url": c.thumbnail_url,
        "emoji": c.emoji, "bg_color": c.bg_color,
        "related_skills": c.related_skills or [], "url": c.url,
        "is_featured": c.is_featured,
    } for c in rows]

@router.get("/biographies")
def list_bios(db: Session = Depends(get_db)):
    rows = db.query(Biography).filter(Biography.is_published == True).all()
    return [{
        "id": b.id, "name": b.name, "role": b.role, "company": b.company,
        "quote": b.quote, "photo_url": b.photo_url,
        "emoji": b.emoji, "bg_color": b.bg_color,
    } for b in rows]
