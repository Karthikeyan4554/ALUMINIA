from typing import List, Optional, Any, Dict
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# --- Auth Schemas ---
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str = Field(..., pattern="^(student|alumni|admin)$")
    full_name: str
    department: Optional[str] = None
    graduation_year: Optional[int] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]

class TokenData(BaseModel):
    user_id: Optional[str] = None
    role: Optional[str] = None

# --- Skill & Experience Schemas ---
class SkillItem(BaseModel):
    skill_name: str
    category: Optional[str] = "General"
    endorsement_count: Optional[int] = 0

class WorkExperienceItem(BaseModel):
    id: Optional[str] = None
    title: str
    company: str
    location: Optional[str] = None
    start_date: str
    end_date: Optional[str] = None
    is_current: bool = False
    description: Optional[str] = None

class EducationItem(BaseModel):
    id: Optional[str] = None
    institution: str
    degree: str
    field_of_study: str
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    grade: Optional[str] = None

class ProjectItem(BaseModel):
    id: Optional[str] = None
    title: str
    description: Optional[str] = None
    technologies: Optional[str] = None
    project_url: Optional[str] = None

# --- Profile Schemas ---
class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    headline: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    cover_url: Optional[str] = None
    college_email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    department: Optional[str] = None
    degree: Optional[str] = None
    graduation_year: Optional[int] = None
    current_company: Optional[str] = None
    current_job_title: Optional[str] = None
    industry: Optional[str] = None
    years_of_experience: Optional[int] = None
    mentorship_available: Optional[bool] = None
    mentorship_capacity: Optional[int] = None
    mentorship_topics: Optional[List[str]] = None
    target_roles: Optional[List[str]] = None
    preferred_industries: Optional[List[str]] = None
    preferred_locations: Optional[List[str]] = None
    mentorship_goals: Optional[str] = None
    skills: Optional[List[str]] = None
    work_experiences: Optional[List[WorkExperienceItem]] = None
    educations: Optional[List[EducationItem]] = None
    projects: Optional[List[ProjectItem]] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    is_public: Optional[bool] = None
    hide_contact_info: Optional[bool] = None

class ProfileOut(BaseModel):
    id: str
    user_id: str
    full_name: str
    headline: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    cover_url: Optional[str] = None
    role: str
    college_email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    department: Optional[str] = None
    degree: Optional[str] = None
    graduation_year: Optional[int] = None
    current_company: Optional[str] = None
    current_job_title: Optional[str] = None
    industry: Optional[str] = None
    years_of_experience: int = 0
    mentorship_available: bool = False
    mentorship_capacity: int = 3
    mentorship_topics: List[str] = []
    target_roles: List[str] = []
    preferred_industries: List[str] = []
    preferred_locations: List[str] = []
    mentorship_goals: Optional[str] = None
    skills: List[str] = []
    work_experiences: List[WorkExperienceItem] = []
    educations: List[EducationItem] = []
    projects: List[ProjectItem] = []
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    is_profile_complete: bool = False
    profile_completion_percentage: int = 30
    is_public: bool = True
    hide_contact_info: bool = True
    connection_status: Optional[str] = None # 'connected', 'pending_sent', 'pending_received', 'none', 'self'

    class Config:
        from_attributes = True

# --- Recommendation Schemas ---
class RecommendationScoreBreakdown(BaseModel):
    skill_similarity: float = 0.0
    career_alignment: float = 0.0
    industry_alignment: float = 0.0
    desired_role: float = 0.0
    semantic_similarity: float = 0.0
    academic_alignment: float = 0.0
    location_match: float = 0.0
    mentorship_bonus: float = 0.0

class RecommendationOut(BaseModel):
    profile: ProfileOut
    score: float # 0 - 100
    match_percentage: int
    breakdown: RecommendationScoreBreakdown
    explanation: str
    conversation_starter: str
    shared_skills: List[str]
    mutual_attributes: List[str]

class RecommendationFeedbackCreate(BaseModel):
    alumni_id: str
    is_relevant: bool = True
    score: Optional[float] = None
    feedback_notes: Optional[str] = None

class WeightConfig(BaseModel):
    career_weight: float = 0.25
    skill_weight: float = 0.20
    industry_weight: float = 0.20
    semantic_weight: float = 0.15
    academic_weight: float = 0.10
    location_weight: float = 0.05
    mentorship_weight: float = 0.05

# --- Connections Schemas ---
class ConnectionRequestCreate(BaseModel):
    receiver_id: str
    message: Optional[str] = None

class ConnectionRequestOut(BaseModel):
    id: str
    sender_id: str
    receiver_id: str
    message: Optional[str] = None
    status: str
    created_at: datetime
    sender_profile: Optional[ProfileOut] = None
    receiver_profile: Optional[ProfileOut] = None

    class Config:
        from_attributes = True

# --- Messaging Schemas ---
class MessageCreate(BaseModel):
    content: str

class MessageOut(BaseModel):
    id: str
    conversation_id: str
    sender_id: str
    content: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationOut(BaseModel):
    id: str
    other_user: ProfileOut
    last_message: Optional[MessageOut] = None
    unread_count: int = 0
    updated_at: datetime

# --- Mentorship Schemas ---
class MentorshipRequestCreate(BaseModel):
    mentor_id: str
    goals_description: str
    preferred_frequency: Optional[str] = "Bi-weekly"

class MentorshipStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(accepted|declined|cancelled|completed)$")
    response_note: Optional[str] = None

class MentorshipSessionCreate(BaseModel):
    mentorship_request_id: Optional[str] = None
    title: str
    scheduled_at: datetime
    duration_minutes: int = 45
    meeting_link: Optional[str] = None
    notes: Optional[str] = None

class MentorshipSessionOut(BaseModel):
    id: str
    mentorship_request_id: Optional[str] = None
    student_id: str
    mentor_id: str
    title: str
    scheduled_at: datetime
    duration_minutes: int
    meeting_link: Optional[str] = None
    status: str
    notes: Optional[str] = None
    student_profile: Optional[ProfileOut] = None
    mentor_profile: Optional[ProfileOut] = None

    class Config:
        from_attributes = True

class MentorshipRequestOut(BaseModel):
    id: str
    student_id: str
    mentor_id: str
    goals_description: str
    preferred_frequency: str
    status: str
    response_note: Optional[str] = None
    created_at: datetime
    student_profile: Optional[ProfileOut] = None
    mentor_profile: Optional[ProfileOut] = None
    sessions: List[MentorshipSessionOut] = []

    class Config:
        from_attributes = True

# --- Jobs Schemas ---
class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    work_mode: str = "Remote"
    employment_type: str = "Full-time"
    description: str
    requirements: Optional[str] = None
    required_skills: List[str] = []
    salary_range: Optional[str] = None
    external_url: Optional[str] = None
    application_deadline: Optional[str] = None

class JobOut(BaseModel):
    id: str
    posted_by_id: str
    title: str
    company: str
    location: str
    work_mode: str
    employment_type: str
    description: str
    requirements: Optional[str] = None
    required_skills: List[str] = []
    salary_range: Optional[str] = None
    external_url: Optional[str] = None
    application_deadline: Optional[str] = None
    status: str
    is_featured: bool
    created_at: datetime
    is_saved: Optional[bool] = False
    has_applied: Optional[bool] = False
    poster_profile: Optional[ProfileOut] = None

    class Config:
        from_attributes = True

class JobApplicationCreate(BaseModel):
    job_id: Optional[str] = None
    resume_url: Optional[str] = None
    cover_note: Optional[str] = None

# --- Events Schemas ---
class EventCreate(BaseModel):
    title: str
    event_type: str = "Webinar"
    description: str
    location: str = "Virtual / Zoom"
    is_virtual: bool = True
    virtual_meeting_link: Optional[str] = None
    start_time: datetime
    end_time: datetime
    capacity: int = 100
    banner_url: Optional[str] = None

class EventOut(BaseModel):
    id: str
    organizer_id: str
    title: str
    event_type: str
    description: str
    location: str
    is_virtual: bool
    virtual_meeting_link: Optional[str] = None
    start_time: datetime
    end_time: datetime
    capacity: int
    banner_url: Optional[str] = None
    status: str
    registered_count: int = 0
    is_registered: Optional[bool] = False
    created_at: datetime

    class Config:
        from_attributes = True

# --- Notification Schemas ---
class NotificationOut(BaseModel):
    id: str
    user_id: str
    type: str
    title: str
    message: str
    link: Optional[str] = None
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

# --- AI Assistant Schemas ---
class AIAssistantMessage(BaseModel):
    role: str # "user" or "assistant"
    content: str

class AIAssistantRequest(BaseModel):
    message: str
    history: Optional[List[AIAssistantMessage]] = []
    task: Optional[str] = "general" # 'general', 'match_explanation', 'connection_draft', 'interview_prep', 'bio_refine'
    target_user_id: Optional[str] = None

class AIAssistantResponse(BaseModel):
    response: str
    suggested_actions: Optional[List[str]] = []
    recommended_alumni: Optional[List[Dict[str, Any]]] = []
    is_llm_generated: bool = False

# --- Admin Schemas ---
class AdminMetricsOut(BaseModel):
    total_users: int
    total_students: int
    total_alumni: int
    total_connections: int
    total_mentorship_requests: int
    active_mentorship_sessions: int
    total_jobs: int
    total_events: int
    recommendation_feedback_positive_rate: float
    weekly_activity: List[Dict[str, Any]]
    department_distribution: List[Dict[str, Any]]
    industry_distribution: List[Dict[str, Any]]

class ContentReportCreate(BaseModel):
    reported_user_id: Optional[str] = None
    content_type: str
    content_id: Optional[str] = None
    reason: str

class ContentReportOut(BaseModel):
    id: str
    reporter_id: str
    reported_user_id: Optional[str] = None
    content_type: str
    content_id: Optional[str] = None
    reason: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
