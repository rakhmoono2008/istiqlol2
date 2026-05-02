from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import jwt
from app.core.config import settings
from app.core.database import get_db
from app.models.base import User

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = int(payload.get("sub"))
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

def require_seeker(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "seeker":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Seekers only")
    return current_user

def require_employer(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "employer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Employers only")
    return current_user
