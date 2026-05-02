from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.base import Job, Profile, Course
import math

router = APIRouter()

def _cosine(a: list, b: list) -> float:
    if not a or not b: return 0.0
    sa, sb = {x.lower() for x in a}, {x.lower() for x in b}
    inter = sa & sb
    return len(inter) / math.sqrt(len(sa) * len(sb)) if inter else 0.0

def _haversine(lat1, lng1, lat2, lng2) -> float:
    R = 6371
    dl, dg = math.radians(lat2-lat1), math.radians(lng2-lng1)
    a = math.sin(dl/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dg/2)**2
    return R * 2 * math.asin(math.sqrt(a))

@router.get("/jobs")
def recommended_jobs(user_id: int = Query(...), limit: int = 10, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    user_tags = (profile.skills or []) + (profile.certificates or []) if profile else []
    jobs = db.query(Job).filter(Job.is_active == True).all()
    scored = []
    for job in jobs:
        score = _cosine(user_tags, job.required_skills or [])
        if profile and profile.location_lat and job.location_lat:
            dist = _haversine(profile.location_lat, profile.location_lng, job.location_lat, job.location_lng)
            score += max(0, 0.2 * (1 - dist/50))
        if score > 0:
            scored.append({"job_id": job.id, "title": job.title,
                "company_name": job.company.name if job.company else "",
                "company_verified": job.company.verified if job.company else False,
                "match_percent": round(min(score,1.0)*100),
                "work_format": job.work_format,
                "salary_min": job.salary_min, "salary_max": job.salary_max,
                "salary_currency": job.salary_currency,
                "city": job.city, "required_skills": job.required_skills or []})
    scored.sort(key=lambda x: x["match_percent"], reverse=True)
    return scored[:limit]

@router.get("/courses")
def recommended_courses(user_id: int = Query(...), limit: int = 6, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    user_tags = (profile.skills or []) + (profile.certificates or []) if profile else []
    courses = db.query(Course).all()
    scored = []
    for c in courses:
        score = _cosine(user_tags, c.related_skills or [])
        scored.append({"course_id": c.id, "title": c.title, "category": c.category,
            "duration_hours": c.duration_hours, "has_certificate": c.has_certificate,
            "emoji": c.emoji, "bg_color": c.bg_color, "url": c.url,
            "relevance": round(score * 100)})
    scored.sort(key=lambda x: x["relevance"], reverse=True)
    return scored[:limit]
