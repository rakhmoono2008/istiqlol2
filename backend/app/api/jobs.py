from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.base import Job, Company
from typing import Optional
from pydantic import BaseModel

router = APIRouter()

class JobCreate(BaseModel):
    company_id:      int
    title:           str
    description:     str = ""
    category:        str = ""
    work_format:     str = "office"
    salary_min:      Optional[int] = None
    salary_max:      Optional[int] = None
    salary_currency: str = "UZS"
    required_skills: list = []
    city:            str = ""

def _fmt(job: Job) -> dict:
    return {
        "id":           job.id,
        "title":        job.title,
        "description":  job.description,
        "category":     job.category,
        "work_format":  job.work_format,
        "salary_min":   job.salary_min,
        "salary_max":   job.salary_max,
        "salary_currency": job.salary_currency,
        "required_skills": job.required_skills or [],
        "city":         job.city,
        "created_at":   str(job.created_at),
        "company": {
            "id":       job.company.id,
            "name":     job.company.name,
            "verified": job.company.verified,
            "logo_url": job.company.logo_url,
        } if job.company else None,
    }

@router.get("/")
def list_jobs(
    category:    Optional[str] = None,
    work_format: Optional[str] = None,
    city:        Optional[str] = None,
    skip: int = 0, limit: int = 20,
    db: Session = Depends(get_db)
):
    q = db.query(Job).filter(Job.is_active == True)
    if category:    q = q.filter(Job.category == category)
    if work_format: q = q.filter(Job.work_format == work_format)
    if city:        q = q.filter(Job.city.ilike(f"%{city}%"))
    return [_fmt(j) for j in q.offset(skip).limit(limit).all()]

@router.get("/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job: raise HTTPException(404, "Job not found")
    return _fmt(job)

@router.post("/")
def create_job(data: JobCreate, db: Session = Depends(get_db)):
    job = Job(**data.dict())
    db.add(job); db.commit(); db.refresh(job)
    return _fmt(job)

@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job: raise HTTPException(404, "Job not found")
    job.is_active = False
    db.commit()
    return {"ok": True}
