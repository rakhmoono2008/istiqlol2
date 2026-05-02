from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./istiqlol.db"
    SECRET_KEY: str = "change-me-in-production-please"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    ONE_ID_CLIENT_ID:     str = ""
    ONE_ID_CLIENT_SECRET: str = ""
    ONE_ID_REDIRECT_URI:  str = "http://localhost:8000/auth/callback"
    ONE_ID_AUTH_URL:  str = "https://sso.egov.uz/sso/oauth/Authorization.do"
    ONE_ID_TOKEN_URL: str = "https://sso.egov.uz/sso/oauth/token"

    class Config:
        env_file = ".env"

settings = Settings()
