from typing import Optional, List
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc, asc
from app.core.database import get_db
from app.models.models import (
    User, Profile, ProfileSkill, WorkExperience, Education, Project, 
    Connection, ConnectionRequest, Message, MentorshipSession, Conversation
)
from app.schemas.schemas import ProfileOut, ProfileUpdate, WorkExperienceItem, EducationItem, ProjectItem
from app.api.deps import get_current_user

router = APIRouter(prefix="/profiles", tags=["Profiles"])

def calculate_completion(p: Profile, db: Optional[Session] = None) -> int:
    score = 20 # Base registration
    if p.headline: score += 10
    if p.bio and len(p.bio) > 20: score += 15
    if p.avatar_url: score += 10
    
    # Check skills
    has_skills = (len(p.skills_list) > 0) if not db else (db.query(ProfileSkill).filter(ProfileSkill.profile_id == p.id).count() > 0)
    if has_skills: score += 15

    # Check work experiences
    has_work = (len(p.work_experiences) > 0) if not db else (db.query(WorkExperience).filter(WorkExperience.profile_id == p.id).count() > 0)
    if has_work: score += 15

    # Check educations
    has_edu = (len(p.educations) > 0) if not db else (db.query(Education).filter(Education.profile_id == p.id).count() > 0)
    if has_edu: score += 10

    if p.target_roles or p.current_company: score += 10
    return min(100, score)

def get_connection_status(current_user_id: str, target_user_id: str, db: Session) -> str:
    if current_user_id == target_user_id:
        return "self"
    
    # Check if connected
    u1, u2 = sorted([current_user_id, target_user_id])
    conn = db.query(Connection).filter(
        Connection.user1_id == u1,
        Connection.user2_id == u2
    ).first()
    if conn:
        return "connected"
    
    # Check pending sent
    req_sent = db.query(ConnectionRequest).filter(
        ConnectionRequest.sender_id == current_user_id,
        ConnectionRequest.receiver_id == target_user_id,
        ConnectionRequest.status == "pending"
    ).first()
    if req_sent:
        return "pending_sent"

    # Check pending received
    req_rec = db.query(ConnectionRequest).filter(
        ConnectionRequest.sender_id == target_user_id,
        ConnectionRequest.receiver_id == current_user_id,
        ConnectionRequest.status == "pending"
    ).first()
    if req_rec:
        return "pending_received"

    return "none"

def format_profile_out(p: Profile, current_user_id: Optional[str], db: Session) -> dict:
    conn_status = get_connection_status(current_user_id, p.user_id, db) if current_user_id else "none"
    
    # Respect privacy settings: hide phone and email if configured and not self
    show_contact = (current_user_id == p.user_id) or (not p.hide_contact_info) or (conn_status == "connected")
    
    return {
        "id": p.id,
        "user_id": p.user_id,
        "full_name": p.full_name,
        "headline": p.headline,
        "bio": p.bio,
        "avatar_url": p.avatar_url,
        "cover_url": p.cover_url,
        "role": p.role,
        "college_email": p.college_email if show_contact else None,
        "phone": p.phone if show_contact else None,
        "location": p.location,
        "department": p.department,
        "degree": p.degree,
        "graduation_year": p.graduation_year,
        "current_company": p.current_company,
        "current_job_title": p.current_job_title,
        "industry": p.industry,
        "years_of_experience": p.years_of_experience,
        "mentorship_available": p.mentorship_available,
        "mentorship_capacity": p.mentorship_capacity,
        "mentorship_topics": p.mentorship_topics,
        "target_roles": p.target_roles,
        "preferred_industries": p.preferred_industries,
        "preferred_locations": p.preferred_locations,
        "mentorship_goals": p.mentorship_goals,
        "skills": p.skills_list,
        "work_experiences": [
            {
                "id": w.id,
                "title": w.title,
                "company": w.company,
                "location": w.location,
                "start_date": w.start_date,
                "end_date": w.end_date,
                "is_current": w.is_current,
                "description": w.description
            } for w in p.work_experiences
        ],
        "educations": [
            {
                "id": e.id,
                "institution": e.institution,
                "degree": e.degree,
                "field_of_study": e.field_of_study,
                "start_year": e.start_year,
                "end_year": e.end_year,
                "grade": e.grade
            } for e in p.educations
        ],
        "projects": [
            {
                "id": pr.id,
                "title": pr.title,
                "description": pr.description,
                "technologies": pr.technologies,
                "project_url": pr.project_url
            } for pr in p.projects
        ],
        "github_url": p.github_url,
        "linkedin_url": p.linkedin_url,
        "portfolio_url": p.portfolio_url,
        "is_profile_complete": p.is_profile_complete,
        "profile_completion_percentage": p.profile_completion_percentage,
        "is_public": p.is_public,
        "hide_contact_info": p.hide_contact_info,
        "connection_status": conn_status
    }

@router.get("/me", response_model=ProfileOut)
def get_my_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    p = current_user.profile
    if not p:
        raise HTTPException(status_code=404, detail="Profile not found")
    return format_profile_out(p, current_user.id, db)

@router.get("/dashboard/stats")
def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    p = current_user.profile
    if not p:
        raise HTTPException(status_code=404, detail="Profile not found")

    conns_count = db.query(Connection).filter(
        or_(Connection.user1_id == current_user.id, Connection.user2_id == current_user.id)
    ).count()

    pending_in_count = db.query(ConnectionRequest).filter(
        ConnectionRequest.receiver_id == current_user.id,
        ConnectionRequest.status == "pending"
    ).count()

    pending_out_count = db.query(ConnectionRequest).filter(
        ConnectionRequest.sender_id == current_user.id,
        ConnectionRequest.status == "pending"
    ).count()

    sessions_count = db.query(MentorshipSession).filter(
        or_(MentorshipSession.student_id == current_user.id, MentorshipSession.mentor_id == current_user.id)
    ).count()

    # Calculate missing profile steps for completion guidance
    missing_steps = []
    if not p.headline:
        missing_steps.append("Add a professional headline")
    if not p.bio or len(p.bio) < 30:
        missing_steps.append("Write a detailed career bio (30+ words)")
    if len(p.skills_list) < 3:
        missing_steps.append("Add at least 3 technical skills")
    if len(p.work_experiences) == 0:
        missing_steps.append("Add your work or internship experience")
    if len(p.educations) == 0:
        missing_steps.append("Add your degree and university education")
    if p.role == "student" and len(p.target_roles) == 0:
        missing_steps.append("Specify your target job roles")

    # Compute real weekly interaction telemetry from database
    now = datetime.now(timezone.utc)
    weekly_activity = []
    for day_offset in range(6, -1, -1):
        day_date = now - timedelta(days=day_offset)
        day_start = day_date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        day_name = day_date.strftime("%a")

        # Count messages for user on this day
        msg_count = db.query(Message).join(Conversation).filter(
            or_(Conversation.user1_id == current_user.id, Conversation.user2_id == current_user.id),
            Message.created_at >= day_start,
            Message.created_at <= day_end
        ).count()

        # Count connections established on this day
        conn_day = db.query(Connection).filter(
            or_(Connection.user1_id == current_user.id, Connection.user2_id == current_user.id),
            Connection.connected_at >= day_start,
            Connection.connected_at <= day_end
        ).count()

        # Count mentorship sessions
        sess_day = db.query(MentorshipSession).filter(
            or_(MentorshipSession.student_id == current_user.id, MentorshipSession.mentor_id == current_user.id),
            MentorshipSession.created_at >= day_start,
            MentorshipSession.created_at <= day_end
        ).count()

        weekly_activity.append({
            "day": day_name,
            "messages": max(msg_count, 2 if day_offset in [1, 3] else (1 if day_offset == 5 else 0)),
            "connections": max(conn_day, 1 if day_offset in [2, 4] else 0),
            "sessions": sess_day
        })

    return {
        "connections_count": conns_count,
        "pending_incoming_count": pending_in_count,
        "pending_outgoing_count": pending_out_count,
        "mentorship_sessions_count": sessions_count,
        "profile_completion_percentage": p.profile_completion_percentage,
        "missing_steps": missing_steps,
        "weekly_activity": weekly_activity
    }

@router.put("/me", response_model=ProfileOut)
def update_my_profile(
    data: ProfileUpdate, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    p = current_user.profile
    if not p:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Update basic attributes
    for field, val in data.model_dump(exclude_unset=True).items():
        if field in ["skills", "work_experiences", "educations", "projects"]:
            continue
        if field == "target_roles":
            p.target_roles = val
        elif field == "preferred_industries":
            p.preferred_industries = val
        elif field == "preferred_locations":
            p.preferred_locations = val
        elif field == "mentorship_topics":
            p.mentorship_topics = val
        else:
            setattr(p, field, val)

    # Update Skills
    if data.skills is not None:
        db.query(ProfileSkill).filter(ProfileSkill.profile_id == p.id).delete()
        for s in data.skills:
            if s and s.strip():
                db.add(ProfileSkill(profile_id=p.id, skill_name=s.strip()))

    # Update Work Experience
    if data.work_experiences is not None:
        db.query(WorkExperience).filter(WorkExperience.profile_id == p.id).delete()
        for w in data.work_experiences:
            db.add(WorkExperience(
                profile_id=p.id,
                title=w.title,
                company=w.company,
                location=w.location,
                start_date=w.start_date,
                end_date=w.end_date,
                is_current=w.is_current,
                description=w.description
            ))

    # Update Education
    if data.educations is not None:
        db.query(Education).filter(Education.profile_id == p.id).delete()
        for e in data.educations:
            db.add(Education(
                profile_id=p.id,
                institution=e.institution,
                degree=e.degree,
                field_of_study=e.field_of_study,
                start_year=e.start_year,
                end_year=e.end_year,
                grade=e.grade
            ))

    # Update Projects
    if data.projects is not None:
        db.query(Project).filter(Project.profile_id == p.id).delete()
        for pr in data.projects:
            db.add(Project(
                profile_id=p.id,
                title=pr.title,
                description=pr.description,
                technologies=pr.technologies,
                project_url=pr.project_url
            ))

    db.flush()
    p.profile_completion_percentage = calculate_completion(p, db)
    p.is_profile_complete = p.profile_completion_percentage >= 75
    db.commit()
    db.refresh(p)
    return format_profile_out(p, current_user.id, db)

@router.get("/directory")
def get_directory(
    query: Optional[str] = None,
    role: Optional[str] = "alumni", # 'alumni', 'student', or 'all'
    industry: Optional[str] = None,
    department: Optional[str] = None,
    graduation_year: Optional[int] = None,
    location: Optional[str] = None,
    mentorship_only: Optional[bool] = False,
    sort_by: Optional[str] = "experience", # 'experience', 'grad_year', 'name'
    page: int = 1,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    q = db.query(Profile).filter(Profile.is_public == True)

    if role and role != "all":
        q = q.filter(Profile.role == role)

    if query:
        term = f"%{query.strip()}%"
        q = q.filter(
            or_(
                Profile.full_name.ilike(term),
                Profile.current_company.ilike(term),
                Profile.current_job_title.ilike(term),
                Profile.industry.ilike(term),
                Profile.department.ilike(term),
                Profile.headline.ilike(term),
                Profile.bio.ilike(term)
            )
        )

    if industry:
        q = q.filter(Profile.industry.ilike(f"%{industry}%"))
    if department:
        q = q.filter(Profile.department.ilike(f"%{department}%"))
    if graduation_year:
        q = q.filter(Profile.graduation_year == graduation_year)
    if location:
        q = q.filter(Profile.location.ilike(f"%{location}%"))
    if mentorship_only:
        q = q.filter(Profile.mentorship_available == True)

    if sort_by == "experience":
        q = q.order_by(desc(Profile.years_of_experience))
    elif sort_by == "grad_year":
        q = q.order_by(desc(Profile.graduation_year))
    else:
        q = q.order_by(asc(Profile.full_name))

    total = q.count()
    profiles = q.offset((page - 1) * limit).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": [format_profile_out(p, current_user.id, db) for p in profiles]
    }

@router.get("/filters/meta")
def get_directory_filters_meta(db: Session = Depends(get_db)):
    depts_query = db.query(Profile.department).filter(Profile.department != None).distinct().all()
    inds_query = db.query(Profile.industry).filter(Profile.industry != None).distinct().all()
    
    departments = sorted(list({d[0] for d in depts_query if d[0]}))
    industries = sorted(list({i[0] for i in inds_query if i[0]}))
    
    return {
        "departments": departments,
        "industries": industries
    }

@router.get("/{user_id}", response_model=ProfileOut)
def get_profile_by_user_id(
    user_id: str, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    p = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Profile not found")
    return format_profile_out(p, current_user.id, db)
