from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    id          = Column(Integer, primary_key=True, index=True)
    one_id_sub  = Column(String, unique=True, index=True)
    email       = Column(String, unique=True, index=True, nullable=True)
    role        = Column(String, default="seeker")   # seeker | employer
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
    profile     = relationship("Profile", back_populates="user", uselist=False)
    company     = relationship("Company", back_populates="user", uselist=False)

class Profile(Base):
    __tablename__ = "profiles"
    id           = Column(Integer, primary_key=True, index=True)
    user_id      = Column(Integer, ForeignKey("users.id"), unique=True)
    first_name   = Column(String, nullable=True)
    last_name    = Column(String, nullable=True)
    photo_url    = Column(String, nullable=True)
    profile_type = Column(String, default="open")   # open | anonymous
    bio          = Column(Text, nullable=True)
    skills       = Column(JSON, default=list)
    experience   = Column(JSON, default=list)
    education    = Column(JSON, default=list)
    certificates = Column(JSON, default=list)
    location_lat = Column(Float, nullable=True)
    location_lng = Column(Float, nullable=True)
    city         = Column(String, nullable=True)
    user         = relationship("User", back_populates="profile")

class Company(Base):
    __tablename__ = "companies"
    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id"), unique=True)
    name        = Column(String, nullable=False)
    description = Column(Text)
    website     = Column(String, nullable=True)
    phone       = Column(String, nullable=True)
    address     = Column(String, nullable=True)
    logo_url    = Column(String, nullable=True)
    verified    = Column(Boolean, default=False)
    user        = relationship("User", back_populates="company")
    jobs        = relationship("Job", back_populates="company")

class Job(Base):
    __tablename__ = "jobs"
    id              = Column(Integer, primary_key=True, index=True)
    company_id      = Column(Integer, ForeignKey("companies.id"))
    title           = Column(String, nullable=False)
    description     = Column(Text)
    category        = Column(String)
    work_format     = Column(String, default="office")  # office|remote|hybrid
    salary_min      = Column(Integer, nullable=True)
    salary_max      = Column(Integer, nullable=True)
    salary_currency = Column(String, default="UZS")
    required_skills = Column(JSON, default=list)
    city            = Column(String, nullable=True)
    location_lat    = Column(Float, nullable=True)
    location_lng    = Column(Float, nullable=True)
    is_active       = Column(Boolean, default=True)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())
    company         = relationship("Company", back_populates="jobs")

class Course(Base):
    __tablename__ = "courses"
    id             = Column(Integer, primary_key=True, index=True)
    title          = Column(String, nullable=False)
    description    = Column(Text)
    category       = Column(String)
    duration_hours = Column(Integer)
    has_certificate= Column(Boolean, default=True)
    thumbnail_url  = Column(String, nullable=True)
    emoji          = Column(String, nullable=True)
    bg_color       = Column(String, nullable=True)
    url            = Column(String, nullable=True)
    related_skills = Column(JSON, default=list)
    is_featured    = Column(Boolean, default=False)

class Biography(Base):
    __tablename__ = "biographies"
    id           = Column(Integer, primary_key=True, index=True)
    name         = Column(String, nullable=False)
    role         = Column(String)
    company      = Column(String, nullable=True)
    quote        = Column(Text)
    story        = Column(Text)
    photo_url    = Column(String, nullable=True)
    emoji        = Column(String, nullable=True)
    bg_color     = Column(String, nullable=True)
    is_published = Column(Boolean, default=True)
