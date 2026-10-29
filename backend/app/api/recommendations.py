from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from app.core.database import get_db
from app.models.models import (
    User, Profile, Connection, RecommendationFeedback
)
from app.schemas.schemas import (
    RecommendationOut, RecommendationFeedbackCreate, WeightConfig, RecommendationScoreBreakdown
)
from app.services.recommendation_engine import recommendation_engine
from app.api.deps import get_current_user
from app.api.profiles import format_profile_out

router = APIRouter(prefix="/recommendations", tags=["AI Recommendations"])

@router.get("", response_model=List[RecommendationOut])
def get_recommendations(
    industry: Optional[str] = None,
    department: Optional[str] = None,
    skill: Optional[str] = None,
    job_role: Optional[str] = None,
    graduation_year: Optional[int] = None,
    location: Optional[str] = None,
    mentorship_only: Optional[bool] = False,
    sort_by: Optional[str] = "relevance", # 'relevance', 'experience', 'grad_year'
    limit: int = 15,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    student_profile = current_user.profile
    if not student_profile:
        raise HTTPException(status_code=400, detail="Student profile required for recommendations")

    # Fetch existing connected user IDs to exclude
    existing_conns = db.query(Connection).filter(
        (Connection.user1_id == current_user.id) | (Connection.user2_id == current_user.id)
    ).all()
    excluded_ids = {current_user.id}
    for c in existing_conns:
        excluded_ids.add(c.user1_id)
        excluded_ids.add(c.user2_id)

    # Fetch alumni candidates
    query = db.query(Profile).options(
        joinedload(Profile.skills),
        joinedload(Profile.projects),
        joinedload(Profile.work_experiences)
    ).filter(
        Profile.role == "alumni",
        Profile.is_public == True,
        ~Profile.user_id.in_(excluded_ids)
    )

    if industry:
        query = query.filter(Profile.industry.ilike(f"%{industry}%"))
    if department:
        query = query.filter(Profile.department.ilike(f"%{department}%"))
    if job_role:
        query = query.filter(Profile.current_job_title.ilike(f"%{job_role}%"))
    if graduation_year:
        query = query.filter(Profile.graduation_year == graduation_year)
    if location:
        query = query.filter(Profile.location.ilike(f"%{location}%"))
    if mentorship_only:
        query = query.filter(Profile.mentorship_available == True)

    candidates = query.all()

    # Filter by specific skill if requested
    if skill:
        norm_sk = skill.lower().strip()
        candidates = [c for c in candidates if any(norm_sk in s.lower() for s in c.skills_list)]

    # Fetch feedback history
    feedbacks = db.query(RecommendationFeedback).filter(
        RecommendationFeedback.student_id == current_user.id
    ).all()
    feedback_dict = {f.alumni_id: f.is_relevant for f in feedbacks}

    # Run AI recommendation ranking
    ranked = recommendation_engine.rank_alumni(student_profile, candidates, feedback_dict)

    # Secondary sort if requested
    if sort_by == "experience":
        ranked.sort(key=lambda x: x["profile"].years_of_experience, reverse=True)
    elif sort_by == "grad_year":
        ranked.sort(key=lambda x: x["profile"].graduation_year or 0, reverse=True)

    results = []
    for item in ranked[:limit]:
        p = item["profile"]
        results.append({
            "profile": format_profile_out(p, current_user.id, db),
            "score": item["score"],
            "match_percentage": item["match_percentage"],
            "breakdown": item["breakdown"],
            "explanation": item["explanation"],
            "conversation_starter": item["conversation_starter"],
            "shared_skills": item["shared_skills"],
            "mutual_attributes": item["mutual_attributes"]
        })

    return results

@router.post("/feedback")
def submit_feedback(
    data: RecommendationFeedbackCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing = db.query(RecommendationFeedback).filter(
        RecommendationFeedback.student_id == current_user.id,
        RecommendationFeedback.alumni_id == data.alumni_id
    ).first()

    resolved_score = data.score if data.score is not None else (85.0 if data.is_relevant else 20.0)
    if existing:
        existing.is_relevant = data.is_relevant
        existing.score = resolved_score
        existing.feedback_notes = data.feedback_notes
    else:
        fb = RecommendationFeedback(
            student_id=current_user.id,
            alumni_id=data.alumni_id,
            score=resolved_score,
            is_relevant=data.is_relevant,
            feedback_notes=data.feedback_notes
        )
        db.add(fb)
    db.commit()
    return {"status": "success", "message": "Recommendation feedback successfully recorded and incorporated into ranking model."}

@router.get("/weights", response_model=WeightConfig)
def get_weights():
    w = recommendation_engine.weights
    return WeightConfig(
        career_weight=w.get("career", 0.25),
        skill_weight=w.get("skills", 0.20),
        industry_weight=w.get("industry", 0.20),
        semantic_weight=w.get("semantic", 0.15),
        academic_weight=w.get("academic", 0.10),
        location_weight=w.get("location", 0.05),
        mentorship_weight=w.get("mentorship", 0.05)
    )

@router.put("/weights")
def update_weights(config: WeightConfig):
    recommendation_engine.update_weights({
        "career": config.career_weight,
        "skills": config.skill_weight,
        "industry": config.industry_weight,
        "semantic": config.semantic_weight,
        "academic": config.academic_weight,
        "location": config.location_weight,
        "mentorship": config.mentorship_weight
    })
    return {"message": "Recommendation weights successfully updated.", "weights": recommendation_engine.weights}
