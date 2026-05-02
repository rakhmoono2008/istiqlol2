from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.base import Profile

router = APIRouter()

def _fmt(p: Profile, force_open: bool = False) -> dict:
    open_profile = force_open or p.profile_type == "open"
    return {
        "user_id":      p.user_id,
        "profile_type": p.profile_type,
        "first_name":   p.first_name  if open_profile else None,
        "last_name":    p.last_name   if open_profile else None,
        "photo_url":    p.photo_url   if open_profile else None,
        "bio":          p.bio,
        "skills":       p.skills       or [],
        "experience":   p.experience   or [],
        "education":    p.education    or [],
        "certificates": p.certificates or [],
        "city":         p.city,
    }

@router.get("/{user_id}")
def get_profile(user_id: int, db: Session = Depends(get_db)):
    p = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not p: raise HTTPException(404, "Profile not found")
    return _fmt(p, force_open=True)

@router.put("/{user_id}")
def update_profile(user_id: int, data: dict, db: Session = Depends(get_db)):
    p = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not p:
        p = Profile(user_id=user_id)
        db.add(p)
    ALLOWED = {"first_name","last_name","photo_url","profile_type","bio","skills","experience","education","certificates","city","location_lat","location_lng"}
    for k, v in data.items():
        if k in ALLOWED: setattr(p, k, v)
    db.commit(); db.refresh(p)
    return _fmt(p, force_open=True)
