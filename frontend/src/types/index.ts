export type UserRole = 'student' | 'alumni' | 'admin';

export interface User {
  id: string;
  email: string;
  role: UserRole;
  full_name?: string;
  avatar_url?: string;
  is_active?: boolean;
}

export interface WorkExperienceItem {
  id?: string;
  title: string;
  company: string;
  location?: string;
  start_date: string;
  end_date?: string;
  is_current?: boolean;
  description?: string;
}

export interface EducationItem {
  id?: string;
  institution: string;
  degree: string;
  field_of_study: string;
  start_year?: number;
  end_year?: number;
  grade?: string;
}

export interface ProjectItem {
  id?: string;
  title: string;
  description?: string;
  technologies?: string;
  project_url?: string;
}

export interface Profile {
  id: string;
  user_id: string;
  full_name: string;
  headline?: string;
  bio?: string;
  avatar_url?: string;
  cover_url?: string;
  role: UserRole;
  college_email?: string;
  phone?: string;
  location?: string;
  department?: string;
  degree?: string;
  graduation_year?: number;
  current_company?: string;
  current_job_title?: string;
  industry?: string;
  years_of_experience: number;
  mentorship_available: boolean;
  mentorship_capacity: number;
  mentorship_topics: string[];
  target_roles: string[];
  preferred_industries: string[];
  preferred_locations: string[];
  mentorship_goals?: string;
  skills: string[];
  work_experiences: WorkExperienceItem[];
  educations: EducationItem[];
  projects: ProjectItem[];
  github_url?: string;
  linkedin_url?: string;
  portfolio_url?: string;
  is_profile_complete: boolean;
  profile_completion_percentage: number;
  is_public: boolean;
  hide_contact_info: boolean;
  connection_status?: 'connected' | 'pending_sent' | 'pending_received' | 'none' | 'self';
}

export interface RecommendationBreakdown {
  career_alignment: number;
  skill_similarity: number;
  industry_alignment: number;
  semantic_similarity: number;
  academic_alignment: number;
  location_match: number;
  mentorship_bonus: number;
}

export interface Recommendation {
  profile: Profile;
  score: number;
  match_percentage: number;
  breakdown: RecommendationBreakdown;
  explanation: string;
  conversation_starter: string;
  shared_skills: string[];
  mutual_attributes: string[];
}

export interface ConnectionRequest {
  id: string;
  sender_id: string;
  receiver_id: string;
  message?: string;
  status: 'pending' | 'accepted' | 'rejected' | 'cancelled';
  created_at: string;
  sender_profile?: Profile;
  receiver_profile?: Profile;
}

export interface Message {
  id: string;
  conversation_id: string;
  sender_id: string;
  content: string;
  is_read: boolean;
  created_at: string;
}

export interface Conversation {
  id: string;
  other_user: Profile;
  last_message?: Message;
  unread_count: number;
  updated_at: string;
}

export interface MentorshipSession {
  id: string;
  mentorship_request_id?: string;
  student_id: string;
  mentor_id: string;
  title: string;
  scheduled_at: string;
  duration_minutes: number;
  meeting_link?: string;
  status: 'scheduled' | 'completed' | 'cancelled';
  notes?: string;
  student_profile?: Profile;
  mentor_profile?: Profile;
}

export interface MentorshipRequest {
  id: string;
  student_id: string;
  mentor_id: string;
  goals_description: string;
  preferred_frequency: string;
  status: 'pending' | 'accepted' | 'declined' | 'cancelled' | 'completed';
  response_note?: string;
  created_at: string;
  student_profile?: Profile;
  mentor_profile?: Profile;
  sessions: MentorshipSession[];
}

export interface Job {
  id: string;
  posted_by_id: string;
  title: string;
  company: string;
  location: string;
  work_mode: string;
  employment_type: string;
  description: string;
  requirements?: string;
  required_skills: string[];
  salary_range?: string;
  external_url?: string;
  application_deadline?: string;
  status: string;
  is_featured: boolean;
  created_at: string;
  is_saved: boolean;
  has_applied: boolean;
  poster_profile?: Profile;
}

export interface AlumniEvent {
  id: string;
  organizer_id: string;
  title: string;
  event_type: string;
  description: string;
  location: string;
  is_virtual: boolean;
  virtual_meeting_link?: string;
  start_time: string;
  end_time: string;
  capacity: number;
  banner_url?: string;
  status: string;
  registered_count: number;
  is_registered: boolean;
  created_at: string;
}

export interface NotificationItem {
  id: string;
  user_id: string;
  type: string;
  title: string;
  message: string;
  link?: string;
  is_read: boolean;
  created_at: string;
}

export interface AdminMetrics {
  total_users: number;
  total_students: number;
  total_alumni: number;
  total_connections: number;
  total_mentorship_requests: number;
  active_mentorship_sessions: number;
  total_jobs: number;
  total_events: number;
  recommendation_feedback_positive_rate: number;
  weekly_activity: { day: string; connections: number; messages: number; mentorship: number }[];
  department_distribution: { name: string; value: number }[];
  industry_distribution: { name: string; value: number }[];
}

export interface ContentReport {
  id: string;
  reporter_id: string;
  reported_user_id?: string;
  content_type: string;
  content_id?: string;
  reason: string;
  status: 'pending' | 'resolved' | 'dismissed';
  created_at: string;
}
