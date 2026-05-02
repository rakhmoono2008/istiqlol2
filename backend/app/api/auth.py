from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.models.base import User
import httpx, jwt
from datetime import datetime, timedelta

router = APIRouter()

def create_token(user_id: int, role: str) -> str:
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

@router.get("/login")
def login(role: str = "seeker"):
    """Redirect to One ID SSO"""
    url = (
        f"{settings.ONE_ID_AUTH_URL}"
        f"?response_type=one_code"
        f"&client_id={settings.ONE_ID_CLIENT_ID}"
        f"&redirect_uri={settings.ONE_ID_REDIRECT_URI}"
        f"&scope=openid"
        f"&state={role}"
    )
    return RedirectResponse(url)

@router.get("/callback")
async def callback(code: str, state: str = "seeker", db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        resp = await client.post(settings.ONE_ID_TOKEN_URL, data={
            "grant_type": "authorization_code",
            "client_id":  settings.ONE_ID_CLIENT_ID,
            "client_secret": settings.ONE_ID_CLIENT_SECRET,
            "code": code,
            "redirect_uri": settings.ONE_ID_REDIRECT_URI,
        })
    if resp.status_code != 200:
        raise HTTPException(400, "One ID auth failed")
    data = resp.json()
    sub = str(data.get("sub") or data.get("user_id") or "unknown")
    user = db.query(User).filter(User.one_id_sub == sub).first()
    if not user:
        user = User(one_id_sub=sub, role=state)
        db.add(user); db.commit(); db.refresh(user)
    return {"access_token": create_token(user.id, user.role), "token_type": "bearer", "role": user.role}

@router.post("/demo-login")
def demo_login(role: str = "seeker", db: Session = Depends(get_db)):
    """Demo endpoint — no One ID needed for local dev"""
    sub = f"demo_{role}"
    user = db.query(User).filter(User.one_id_sub == sub).first()
    if not user:
        user = User(one_id_sub=sub, role=role)
        db.add(user); db.commit(); db.refresh(user)
    return {"access_token": create_token(user.id, user.role), "token_type": "bearer", "role": user.role, "user_id": user.id}
