from datetime import datetime, timezone
import uuid
import json
from sqlalchemy import (
    Column, String, Integer, Boolean, DateTime, ForeignKey, 
    Text, Float, UniqueConstraint, Index
)
from sqlalchemy.orm import relationship
from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

def get_utc_now():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="student")  # 'student', 'alumni', 'admin'
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=True)
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)

    # Relationships
    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    sent_connection_requests = relationship("ConnectionRequest", foreign_keys="ConnectionRequest.sender_id", back_populates="sender", cascade="all, delete-orphan")
    received_connection_requests = relationship("ConnectionRequest", foreign_keys="ConnectionRequest.receiver_id", back_populates="receiver", cascade="all, delete-orphan")
    sent_messages = relationship("Message", back_populates="sender", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    full_name = Column(String(150), nullable=False)
    headline = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(500), nullable=True)
    cover_url = Column(String(500), nullable=True)
    
    role = Column(String(50), nullable=False, default="student")
    college_email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    location = Column(String(150), nullable=True)
    
    # Academic
    department = Column(String(100), nullable=True)  # e.g., Computer Science, Electrical Engineering
    degree = Column(String(100), nullable=True)      # e.g., B.Tech, M.S., Ph.D.
    graduation_year = Column(Integer, nullable=True)
    
    # Professional (for alumni & students)
    current_company = Column(String(150), nullable=True)
    current_job_title = Column(String(150), nullable=True)
    industry = Column(String(100), nullable=True)    # e.g., Software Engineering, FinTech, AI/ML
    years_of_experience = Column(Integer, default=0)
    
    # Mentorship
    mentorship_available = Column(Boolean, default=False)
    mentorship_capacity = Column(Integer, default=3)
    mentorship_topics_json = Column(Text, default="[]")  # JSON list of strings
    
    # Career Goals (for students)
    target_roles_json = Column(Text, default="[]")       # JSON list of strings
    preferred_industries_json = Column(Text, default="[]") # JSON list of strings
    preferred_locations_json = Column(Text, default="[]")  # JSON list of strings
    mentorship_goals = Column(Text, nullable=True)
    
    # Social links
    github_url = Column(String(255), nullable=True)
    linkedin_url = Column(String(255), nullable=True)
    portfolio_url = Column(String(255), nullable=True)
    
    # State & visibility
    is_profile_complete = Column(Boolean, default=False)
    profile_completion_percentage = Column(Integer, default=30)
    is_public = Column(Boolean, default=True)
    hide_contact_info = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)

    # Relationships
    user = relationship("User", back_populates="profile")
    skills = relationship("ProfileSkill", back_populates="profile", cascade="all, delete-orphan")
    work_experiences = relationship("WorkExperience", back_populates="profile", cascade="all, delete-orphan")
    educations = relationship("Education", back_populates="profile", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="profile", cascade="all, delete-orphan")

    @property
    def skills_list(self):
        return [ps.skill_name for ps in self.skills]

    @property
    def target_roles(self):
        try:
            return json.loads(self.target_roles_json or "[]")
        except Exception:
            return []

    @target_roles.setter
    def target_roles(self, val):
        self.target_roles_json = json.dumps(val if isinstance(val, list) else [])

    @property
    def preferred_industries(self):
        try:
            return json.loads(self.preferred_industries_json or "[]")
        except Exception:
            return []

    @preferred_industries.setter
    def preferred_industries(self, val):
        self.preferred_industries_json = json.dumps(val if isinstance(val, list) else [])

    @property
    def preferred_locations(self):
        try:
            return json.loads(self.preferred_locations_json or "[]")
        except Exception:
            return []

    @preferred_locations.setter
    def preferred_locations(self, val):
        self.preferred_locations_json = json.dumps(val if isinstance(val, list) else [])

    @property
    def mentorship_topics(self):
        try:
            return json.loads(self.mentorship_topics_json or "[]")
        except Exception:
            return []

    @mentorship_topics.setter
    def mentorship_topics(self, val):
        self.mentorship_topics_json = json.dumps(val if isinstance(val, list) else [])


class ProfileSkill(Base):
    __tablename__ = "profile_skills"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    profile_id = Column(String(36), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    skill_name = Column(String(100), nullable=False)
    category = Column(String(100), default="General")
    endorsement_count = Column(Integer, default=0)

    profile = relationship("Profile", back_populates="skills")
    __table_args__ = (UniqueConstraint('profile_id', 'skill_name', name='uix_profile_skill'),)


class WorkExperience(Base):
    __tablename__ = "work_experiences"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    profile_id = Column(String(36), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(150), nullable=False)
    company = Column(String(150), nullable=False)
    location = Column(String(150), nullable=True)
    start_date = Column(String(50), nullable=False) # e.g. "2022-01"
    end_date = Column(String(50), nullable=True)   # None if current
    is_current = Column(Boolean, default=False)
    description = Column(Text, nullable=True)

    profile = relationship("Profile", back_populates="work_experiences")


class Education(Base):
    __tablename__ = "educations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    profile_id = Column(String(36), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    institution = Column(String(200), nullable=False)
    degree = Column(String(150), nullable=False)
    field_of_study = Column(String(150), nullable=False)
    start_year = Column(Integer, nullable=True)
    end_year = Column(Integer, nullable=True)
    grade = Column(String(50), nullable=True)

    profile = relationship("Profile", back_populates="educations")


class Project(Base):
    __tablename__ = "projects"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    profile_id = Column(String(36), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    technologies = Column(String(255), nullable=True)
    project_url = Column(String(500), nullable=True)

    profile = relationship("Profile", back_populates="projects")


class ConnectionRequest(Base):
    __tablename__ = "connection_requests"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    sender_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    receiver_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    message = Column(Text, nullable=True)
    status = Column(String(30), default="pending")  # 'pending', 'accepted', 'rejected', 'cancelled'
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)

    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_connection_requests")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_connection_requests")
    __table_args__ = (Index('ix_conn_req_pair', 'sender_id', 'receiver_id'),)


class Connection(Base):
    __tablename__ = "connections"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user1_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user2_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    connected_at = Column(DateTime, default=get_utc_now)

    __table_args__ = (
        UniqueConstraint('user1_id', 'user2_id', name='uix_connection_pair'),
        Index('ix_conn_users', 'user1_id', 'user2_id')
    )


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user1_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user2_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)

    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan", order_by="Message.created_at")
    __table_args__ = (UniqueConstraint('user1_id', 'user2_id', name='uix_conversation_pair'),)


class Message(Base):
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    conversation_id = Column(String(36), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    sender_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=get_utc_now)

    conversation = relationship("Conversation", back_populates="messages")
    sender = relationship("User", back_populates="sent_messages")


class MentorshipRequest(Base):
    __tablename__ = "mentorship_requests"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    student_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    mentor_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    goals_description = Column(Text, nullable=False)
    preferred_frequency = Column(String(50), default="Bi-weekly")
    status = Column(String(30), default="pending")  # 'pending', 'accepted', 'declined', 'cancelled', 'completed'
    response_note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)

    sessions = relationship("MentorshipSession", back_populates="request", cascade="all, delete-orphan")


class MentorshipSession(Base):
    __tablename__ = "mentorship_sessions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    mentorship_request_id = Column(String(36), ForeignKey("mentorship_requests.id", ondelete="CASCADE"), nullable=True)
    student_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    mentor_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    scheduled_at = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=45)
    meeting_link = Column(String(500), nullable=True)
    status = Column(String(30), default="scheduled")  # 'scheduled', 'completed', 'cancelled'
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=get_utc_now)

    request = relationship("MentorshipRequest", back_populates="sessions")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    posted_by_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    company = Column(String(150), nullable=False)
    location = Column(String(150), nullable=False)
    work_mode = Column(String(50), default="Remote") # 'Remote', 'Hybrid', 'On-site'
    employment_type = Column(String(50), default="Full-time") # 'Full-time', 'Internship', 'Part-time', 'Contract'
    description = Column(Text, nullable=False)
    requirements = Column(Text, nullable=True)
    required_skills_json = Column(Text, default="[]")
    salary_range = Column(String(100), nullable=True)
    external_url = Column(String(500), nullable=True)
    application_deadline = Column(String(50), nullable=True)
    status = Column(String(30), default="active") # 'active', 'closed', 'pending_moderation'
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime, default=get_utc_now)

    @property
    def required_skills(self):
        try:
            return json.loads(self.required_skills_json or "[]")
        except Exception:
            return []

    @required_skills.setter
    def required_skills(self, val):
        self.required_skills_json = json.dumps(val if isinstance(val, list) else [])


class SavedJob(Base):
    __tablename__ = "saved_jobs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(String(36), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    saved_at = Column(DateTime, default=get_utc_now)

    __table_args__ = (UniqueConstraint('user_id', 'job_id', name='uix_user_saved_job'),)


class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(String(36), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    resume_url = Column(String(500), nullable=True)
    cover_note = Column(Text, nullable=True)
    status = Column(String(30), default="submitted") # 'submitted', 'reviewing', 'shortlisted', 'rejected'
    created_at = Column(DateTime, default=get_utc_now)

    __table_args__ = (UniqueConstraint('user_id', 'job_id', name='uix_user_job_application'),)


class Event(Base):
    __tablename__ = "events"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    organizer_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    event_type = Column(String(50), default="Webinar") # 'Webinar', 'Alumni Meetup', 'Career Session', 'Technical Workshop'
    description = Column(Text, nullable=False)
    location = Column(String(200), default="Virtual / Zoom")
    is_virtual = Column(Boolean, default=True)
    virtual_meeting_link = Column(String(500), nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    capacity = Column(Integer, default=100)
    banner_url = Column(String(500), nullable=True)
    status = Column(String(30), default="upcoming") # 'upcoming', 'ongoing', 'completed', 'cancelled'
    created_at = Column(DateTime, default=get_utc_now)


class EventRegistration(Base):
    __tablename__ = "event_registrations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_id = Column(String(36), ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(30), default="registered") # 'registered', 'attended', 'cancelled'
    registered_at = Column(DateTime, default=get_utc_now)

    __table_args__ = (UniqueConstraint('event_id', 'user_id', name='uix_event_registration'),)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type = Column(String(50), nullable=False) # 'connection_request', 'connection_accepted', 'message', 'mentorship_request', etc.
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    link = Column(String(255), nullable=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=get_utc_now)

    user = relationship("User", back_populates="notifications")


class RecommendationFeedback(Base):
    __tablename__ = "recommendation_feedback"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    student_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    alumni_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    score = Column(Float, nullable=False)
    is_relevant = Column(Boolean, nullable=False) # True = relevant, False = not relevant
    feedback_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=get_utc_now)

    __table_args__ = (UniqueConstraint('student_id', 'alumni_id', name='uix_student_alumni_feedback'),)


class ContentReport(Base):
    __tablename__ = "content_reports"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    reporter_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    reported_user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    content_type = Column(String(50), nullable=False) # 'profile', 'job', 'message', 'event'
    content_id = Column(String(50), nullable=True)
    reason = Column(Text, nullable=False)
    status = Column(String(30), default="pending") # 'pending', 'resolved', 'dismissed'
    created_at = Column(DateTime, default=get_utc_now)
