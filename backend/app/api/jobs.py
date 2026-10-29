from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from app.core.database import get_db
from app.models.models import User, Profile, Job, SavedJob, JobApplication
from app.schemas.schemas import JobCreate, JobOut, JobApplicationCreate
from app.api.deps import get_current_user
from app.api.profiles import format_profile_out

router = APIRouter(prefix="/jobs", tags=["Jobs & Opportunities"])

def format_job_out(j: Job, current_user_id: str, db: Session) -> dict:
    is_saved = db.query(SavedJob).filter(
        SavedJob.user_id == current_user_id,
        SavedJob.job_id == j.id
    ).first() is not None

    has_applied = db.query(JobApplication).filter(
        JobApplication.user_id == current_user_id,
        JobApplication.job_id == j.id
    ).first() is not None

    poster = db.query(User).filter(User.id == j.posted_by_id).first()
    poster_profile = format_profile_out(poster.profile, current_user_id, db) if poster and poster.profile else None

    return {
        "id": j.id,
        "posted_by_id": j.posted_by_id,
        "title": j.title,
        "company": j.company,
        "location": j.location,
        "work_mode": j.work_mode,
        "employment_type": j.employment_type,
        "description": j.description,
        "requirements": j.requirements,
        "required_skills": j.required_skills,
        "salary_range": j.salary_range,
        "external_url": j.external_url,
        "application_deadline": j.application_deadline,
        "status": j.status,
        "is_featured": j.is_featured,
        "created_at": j.created_at,
        "is_saved": is_saved,
        "has_applied": has_applied,
        "poster_profile": poster_profile
    }

@router.get("", response_model=List[JobOut])
def list_jobs(
    query: Optional[str] = None,
    work_mode: Optional[str] = None, # 'Remote', 'Hybrid', 'On-site'
    employment_type: Optional[str] = None, # 'Full-time', 'Internship'
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    q = db.query(Job).filter(Job.status == "active")

    if query:
        term = f"%{query.strip()}%"
        q = q.filter(
            or_(
                Job.title.ilike(term),
                Job.company.ilike(term),
                Job.description.ilike(term),
                Job.location.ilike(term)
            )
        )

    if work_mode and work_mode != "All":
        q = q.filter(Job.work_mode == work_mode)

    if employment_type and employment_type != "All":
        q = q.filter(Job.employment_type == employment_type)

    jobs = q.order_by(desc(Job.is_featured), desc(Job.created_at)).all()
    return [format_job_out(j, current_user.id, db) for j in jobs]

@router.post("", response_model=JobOut)
def create_job(
    data: JobCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["alumni", "admin"]:
        raise HTTPException(status_code=403, detail="Only alumni and administrators can post opportunities")

    job = Job(
        posted_by_id=current_user.id,
        title=data.title,
        company=data.company,
        location=data.location,
        work_mode=data.work_mode,
        employment_type=data.employment_type,
        description=data.description,
        requirements=data.requirements,
        salary_range=data.salary_range,
        external_url=data.external_url,
        application_deadline=data.application_deadline,
        status="active",
        is_featured=False
    )
    job.required_skills = data.required_skills
    db.add(job)
    db.commit()
    db.refresh(job)

    return format_job_out(job, current_user.id, db)

@router.post("/{job_id}/save")
def toggle_save_job(
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job opportunity not found")

    existing = db.query(SavedJob).filter(
        SavedJob.user_id == current_user.id,
        SavedJob.job_id == job_id
    ).first()

    if existing:
        db.delete(existing)
        db.commit()
        return {"saved": False, "message": "Job removed from saved opportunities"}
    else:
        saved = SavedJob(user_id=current_user.id, job_id=job_id)
        db.add(saved)
        db.commit()
        return {"saved": True, "message": "Job saved to your opportunities"}

@router.get("/saved", response_model=List[JobOut])
def get_saved_jobs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    saved_entries = db.query(SavedJob).filter(SavedJob.user_id == current_user.id).all()
    job_ids = [s.job_id for s in saved_entries]
    jobs = db.query(Job).filter(Job.id.in_(job_ids)).all()
    return [format_job_out(j, current_user.id, db) for j in jobs]

@router.post("/{job_id}/apply")
def apply_to_job(
    job_id: str,
    data: JobApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    existing = db.query(JobApplication).filter(
        JobApplication.user_id == current_user.id,
        JobApplication.job_id == job_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="You have already submitted an application for this role")

    app = JobApplication(
        user_id=current_user.id,
        job_id=job_id,
        resume_url=data.resume_url or current_user.profile.portfolio_url,
        cover_note=data.cover_note,
        status="submitted"
    )
    db.add(app)
    db.commit()

    return {"message": "Application successfully submitted for this opportunity"}
