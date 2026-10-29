from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc
from app.core.database import get_db
from app.models.models import (
    User, Profile, MentorshipRequest, MentorshipSession, Notification
)
from app.schemas.schemas import (
    MentorshipRequestCreate, MentorshipRequestOut, MentorshipStatusUpdate,
    MentorshipSessionCreate, MentorshipSessionOut, ProfileOut
)
from app.api.deps import get_current_user
from app.api.profiles import format_profile_out

router = APIRouter(prefix="/mentorship", tags=["Mentorship"])

@router.get("/mentors", response_model=List[ProfileOut])
def list_available_mentors(
    industry: Optional[str] = None,
    skill: Optional[str] = None,
    department: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Profile).filter(
        Profile.role == "alumni",
        Profile.mentorship_available == True,
        Profile.user_id != current_user.id
    )

    if industry:
        query = query.filter(Profile.industry.ilike(f"%{industry}%"))
    if department:
        query = query.filter(Profile.department.ilike(f"%{department}%"))

    mentors = query.all()
    if skill:
        norm_skill = skill.lower().strip()
        mentors = [m for m in mentors if any(norm_skill in s.lower() for s in m.skills_list)]

    return [format_profile_out(m, current_user.id, db) for m in mentors]

@router.post("/request", response_model=MentorshipRequestOut)
def create_mentorship_request(
    data: MentorshipRequestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.id == data.mentor_id:
        raise HTTPException(status_code=400, detail="Cannot request mentorship from yourself")

    mentor = db.query(User).filter(User.id == data.mentor_id).first()
    if not mentor or not mentor.profile or not mentor.profile.mentorship_available:
        raise HTTPException(status_code=400, detail="Selected mentor is not currently accepting students")

    # Check existing active request
    existing = db.query(MentorshipRequest).filter(
        MentorshipRequest.student_id == current_user.id,
        MentorshipRequest.mentor_id == data.mentor_id,
        MentorshipRequest.status.in_(["pending", "accepted"])
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="An active or pending mentorship relationship already exists")

    req = MentorshipRequest(
        student_id=current_user.id,
        mentor_id=data.mentor_id,
        goals_description=data.goals_description,
        preferred_frequency=data.preferred_frequency or "Bi-weekly",
        status="pending"
    )
    db.add(req)

    # Notify mentor
    student_name = current_user.profile.full_name if current_user.profile else "A student"
    notif = Notification(
        user_id=data.mentor_id,
        type="mentorship_request",
        title="New Mentorship Request",
        message=f"{student_name} has requested your mentorship guidance.",
        link="/mentorship"
    )
    db.add(notif)
    db.commit()
    db.refresh(req)

    student_p = current_user.profile
    mentor_p = mentor.profile
    return {
        "id": req.id,
        "student_id": req.student_id,
        "mentor_id": req.mentor_id,
        "goals_description": req.goals_description,
        "preferred_frequency": req.preferred_frequency,
        "status": req.status,
        "response_note": req.response_note,
        "created_at": req.created_at,
        "student_profile": format_profile_out(student_p, current_user.id, db) if student_p else None,
        "mentor_profile": format_profile_out(mentor_p, current_user.id, db) if mentor_p else None,
        "sessions": []
    }

@router.get("/requests")
def get_my_mentorship_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    requests = db.query(MentorshipRequest).filter(
        or_(MentorshipRequest.student_id == current_user.id, MentorshipRequest.mentor_id == current_user.id)
    ).order_by(desc(MentorshipRequest.created_at)).all()

    result = []
    for r in requests:
        student = db.query(User).filter(User.id == r.student_id).first()
        mentor = db.query(User).filter(User.id == r.mentor_id).first()
        sessions = db.query(MentorshipSession).filter(MentorshipSession.mentorship_request_id == r.id).all()
        result.append({
            "id": r.id,
            "student_id": r.student_id,
            "mentor_id": r.mentor_id,
            "goals_description": r.goals_description,
            "preferred_frequency": r.preferred_frequency,
            "status": r.status,
            "response_note": r.response_note,
            "created_at": r.created_at,
            "student_profile": format_profile_out(student.profile, current_user.id, db) if student and student.profile else None,
            "mentor_profile": format_profile_out(mentor.profile, current_user.id, db) if mentor and mentor.profile else None,
            "sessions": [
                {
                    "id": s.id,
                    "mentorship_request_id": s.mentorship_request_id,
                    "student_id": s.student_id,
                    "mentor_id": s.mentor_id,
                    "title": s.title,
                    "scheduled_at": s.scheduled_at,
                    "duration_minutes": s.duration_minutes,
                    "meeting_link": s.meeting_link,
                    "status": s.status,
                    "notes": s.notes
                } for s in sessions
            ]
        })
    return result

@router.post("/requests/{request_id}/status")
def update_mentorship_status(
    request_id: str,
    data: MentorshipStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    req = db.query(MentorshipRequest).filter(MentorshipRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Mentorship request not found")

    # Only mentor can accept/decline; student can cancel
    if data.status in ["accepted", "declined"] and req.mentor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the mentor can accept or decline this request")
    if data.status == "cancelled" and req.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the student can cancel this request")

    req.status = data.status
    if data.response_note:
        req.response_note = data.response_note
    req.updated_at = datetime.now(timezone.utc)

    # Notify recipient
    target_id = req.student_id if current_user.id == req.mentor_id else req.mentor_id
    notif = Notification(
        user_id=target_id,
        type="mentorship_status",
        title=f"Mentorship Request {data.status.capitalize()}",
        message=f"Your mentorship request has been {data.status}.",
        link="/mentorship"
    )
    db.add(notif)
    db.commit()

    return {"message": f"Mentorship request status updated to {data.status}"}

@router.post("/sessions", response_model=MentorshipSessionOut)
def schedule_session(
    data: MentorshipSessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    req = None
    if data.mentorship_request_id:
        req = db.query(MentorshipRequest).filter(MentorshipRequest.id == data.mentorship_request_id).first()
        if not req:
            raise HTTPException(status_code=404, detail="Mentorship request not found")

    student_id = req.student_id if req else current_user.id
    mentor_id = req.mentor_id if req else current_user.id

    session = MentorshipSession(
        mentorship_request_id=data.mentorship_request_id,
        student_id=student_id,
        mentor_id=mentor_id,
        title=data.title,
        scheduled_at=data.scheduled_at,
        duration_minutes=data.duration_minutes,
        meeting_link=data.meeting_link or "https://meet.google.com/alm-xynp-vkr",
        notes=data.notes,
        status="scheduled"
    )
    db.add(session)

    # Notify counterpart
    counterpart = mentor_id if current_user.id == student_id else student_id
    notif = Notification(
        user_id=counterpart,
        type="mentorship_session",
        title="Mentorship Session Scheduled",
        message=f"A new session '{data.title}' has been scheduled.",
        link="/mentorship"
    )
    db.add(notif)
    db.commit()
    db.refresh(session)

    student = db.query(User).filter(User.id == student_id).first()
    mentor = db.query(User).filter(User.id == mentor_id).first()

    return {
        "id": session.id,
        "mentorship_request_id": session.mentorship_request_id,
        "student_id": session.student_id,
        "mentor_id": session.mentor_id,
        "title": session.title,
        "scheduled_at": session.scheduled_at,
        "duration_minutes": session.duration_minutes,
        "meeting_link": session.meeting_link,
        "status": session.status,
        "notes": session.notes,
        "student_profile": format_profile_out(student.profile, current_user.id, db) if student and student.profile else None,
        "mentor_profile": format_profile_out(mentor.profile, current_user.id, db) if mentor and mentor.profile else None
    }

@router.get("/sessions")
def list_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sessions = db.query(MentorshipSession).filter(
        or_(MentorshipSession.student_id == current_user.id, MentorshipSession.mentor_id == current_user.id)
    ).order_by(MentorshipSession.scheduled_at.asc()).all()

    result = []
    for s in sessions:
        student = db.query(User).filter(User.id == s.student_id).first()
        mentor = db.query(User).filter(User.id == s.mentor_id).first()
        result.append({
            "id": s.id,
            "mentorship_request_id": s.mentorship_request_id,
            "student_id": s.student_id,
            "mentor_id": s.mentor_id,
            "title": s.title,
            "scheduled_at": s.scheduled_at,
            "duration_minutes": s.duration_minutes,
            "meeting_link": s.meeting_link,
            "status": s.status,
            "notes": s.notes,
            "student_profile": format_profile_out(student.profile, current_user.id, db) if student and student.profile else None,
            "mentor_profile": format_profile_out(mentor.profile, current_user.id, db) if mentor and mentor.profile else None
        })
    return result
