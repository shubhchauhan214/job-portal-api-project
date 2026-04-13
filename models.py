from sqlalchemy import Column, Integer, Text, String, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import enum


class UserRole(str, enum.Enum):
    seeker = "seeker"
    recruiter = "recruiter"
    admin = "admin"


class ApplicationStatus(str, enum.Enum):
    applied = "applied"
    shortlisted = "Shortlisted"
    rejected = "rejected"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(150), unique=True, index=True)
    password = Column(String(255))
    role = Column(Enum(UserRole))

    created_at = Column(DateTime, default=datetime.utcnow)

    jobs = relationship("Job", back_populates="recruiter")
    applications = relationship("Application", back_populates="user")
    saved_jobs = relationship("SavedJob", back_populates="user")
    skills = relationship("UserSkill", back_populates="user")
    resumes = relationship("Resume", back_populates="user")

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150))
    description = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    jobs = relationship("Job", back_populates="company")

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150))
    description = Column(Text)
    location = Column(String(100))
    salary = Column(Integer)
    experience = Column(Integer)

    company_id = Column(Integer, ForeignKey("companies.id"))
    recruiter_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="jobs")
    recruiter = relationship("User", back_populates="jobs")
    applications = relationship("Application", back_populates="job")
    skill = relationship("JobSkill", back_populates="job")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))

    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.applied)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")

class SavedJob(Base):
    __tablename__ = "saved_jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="saved_jobs")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True)


class UserSkill(Base):
    __tablename__ = "user_skills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))

    user = relationship("User", back_populates="skills")
    skill = relationship("Skill")

class JobSkill(Base):
    __tablename__ = "job_skills"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))

    job = relationship("Job", back_populates="skills")
    skill = relationship("Skill")

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    file_url = Column(String(255))

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="resumes")