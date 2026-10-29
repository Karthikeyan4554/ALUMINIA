import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { 
  Building, MapPin, GraduationCap, Award, Mail, Phone, 
  Globe, Github, Linkedin, MessageSquare, UserPlus, 
  Calendar, Briefcase, Sparkles, CheckCircle2, ShieldCheck, Edit3 
} from 'lucide-react';
import { Profile } from '../types';
import { api } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { ConnectModal } from '../components/ConnectModal';
import { MentorshipModal } from '../components/MentorshipModal';
import { Avatar } from '../components/Avatar';

export const ProfilePage: React.FC = () => {
  const { userId } = useParams<{ userId: string }>();
  const { user: currentUser } = useAuth();

  const [profile, setProfile] = useState<Profile | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [connectOpen, setConnectOpen] = useState(false);
  const [mentorOpen, setMentorOpen] = useState(false);

  const isSelf = userId === 'me' || userId === currentUser?.id;

  const fetchProfile = async () => {
    setIsLoading(true);
    try {
      if (isSelf) {
        const data = await api.getMyProfile();
        setProfile(data);
      } else if (userId) {
        const data = await api.getProfile(userId);
        setProfile(data);
      }
    } catch (err) {
      console.error('Failed to load profile', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchProfile();
  }, [userId]);

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto space-y-6 py-6 animate-pulse">
        <div className="h-48 bg-slate-200 rounded-3xl" />
        <div className="h-64 bg-white rounded-3xl border border-slate-200" />
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="max-w-md mx-auto py-16 text-center space-y-3">
        <h2 className="text-lg font-bold text-slate-900">Profile Not Found</h2>
        <p className="text-xs text-slate-500">The requested user profile does not exist or has been removed.</p>
        <Link to="/directory" className="inline-block text-xs font-bold text-brand-600 hover:underline">
          Return to Directory
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12 animate-fade-in">
      
      {/* Cover Banner & Main Header Card */}
      <div className="bg-white rounded-3xl border border-slate-200 shadow-subtle overflow-hidden">
        
        {/* Cover Photo */}
        <div className="h-44 sm:h-52 w-full bg-gradient-to-r from-brand-700 via-indigo-700 to-violet-800 relative">
          {profile.cover_url && (
            <img
              src={profile.cover_url}
              alt="Cover"
              className="w-full h-full object-cover opacity-60"
            />
          )}
          {isSelf && (
            <Link
              to="/edit-profile"
              className="absolute top-4 right-4 px-3 py-1.5 rounded-xl bg-white/90 hover:bg-white text-slate-800 text-xs font-bold backdrop-blur-sm shadow-sm flex items-center gap-1.5 transition-colors"
            >
              <Edit3 className="w-3.5 h-3.5" />
              Edit Profile
            </Link>
          )}
        </div>

        {/* Profile Details Area */}
        <div className="p-6 sm:p-8 pt-0 relative">
          
          <div className="flex flex-col sm:flex-row items-start sm:items-end justify-between gap-4 -mt-16 sm:-mt-20 mb-6">
            <Avatar name={profile.full_name} size="3xl" className="border-4 border-white shadow-elevated" />

            {!isSelf && (
              <div className="flex items-center gap-2">
                <Link
                  to={`/messages?start_with=${profile.user_id}`}
                  className="px-4 py-2 text-xs font-bold rounded-xl border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 shadow-sm flex items-center gap-1.5 transition-colors"
                >
                  <MessageSquare className="w-3.5 h-3.5" />
                  Message
                </Link>

                {profile.mentorship_available && (
                  <button
                    onClick={() => setMentorOpen(true)}
                    className="px-4 py-2 text-xs font-bold rounded-xl bg-amber-50 text-amber-800 border border-amber-200 hover:bg-amber-100 flex items-center gap-1.5 transition-colors"
                  >
                    <Award className="w-3.5 h-3.5" />
                    Request Mentorship
                  </button>
                )}

                <button
                  onClick={() => setConnectOpen(true)}
                  disabled={profile.connection_status === 'connected' || profile.connection_status === 'pending_sent'}
                  className={`px-4 py-2 text-xs font-bold rounded-xl shadow-sm flex items-center gap-1.5 transition-all ${
                    profile.connection_status === 'connected'
                      ? 'bg-emerald-100 text-emerald-800 cursor-default'
                      : profile.connection_status === 'pending_sent'
                      ? 'bg-slate-200 text-slate-600 cursor-default'
                      : 'bg-brand-600 hover:bg-brand-700 text-white'
                  }`}
                >
                  <UserPlus className="w-3.5 h-3.5" />
                  {profile.connection_status === 'connected'
                    ? 'Connected'
                    : profile.connection_status === 'pending_sent'
                    ? 'Request Pending'
                    : 'Connect'}
                </button>
              </div>
            )}
          </div>

          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">
                {profile.full_name}
              </h1>
              <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-brand-100 text-brand-700 capitalize">
                {profile.role}
              </span>
              {profile.mentorship_available && (
                <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-100 text-amber-800 flex items-center gap-1">
                  <Award className="w-3.5 h-3.5" /> Open Mentor
                </span>
              )}
            </div>

            <p className="text-sm font-semibold text-brand-700 mt-1">
              {profile.headline || `${profile.role === 'alumni' ? 'Alumnus' : 'Student'} • ${profile.department}`}
            </p>

            <div className="flex flex-wrap items-center gap-4 mt-3 text-xs text-slate-500">
              {profile.current_company && (
                <span className="flex items-center gap-1">
                  <Building className="w-4 h-4 text-slate-400" />
                  {profile.current_job_title} at {profile.current_company}
                </span>
              )}
              {profile.department && (
                <span className="flex items-center gap-1">
                  <GraduationCap className="w-4 h-4 text-slate-400" />
                  {profile.degree || profile.department} ({profile.graduation_year})
                </span>
              )}
              {profile.location && (
                <span className="flex items-center gap-1">
                  <MapPin className="w-4 h-4 text-slate-400" />
                  {profile.location}
                </span>
              )}
            </div>

            {/* Social & Contact Links */}
            <div className="flex items-center gap-3 mt-4 pt-4 border-t border-slate-100 text-xs">
              {profile.college_email && (
                <a href={`mailto:${profile.college_email}`} className="text-slate-600 hover:text-brand-600 flex items-center gap-1">
                  <Mail className="w-3.5 h-3.5" /> {profile.college_email}
                </a>
              )}
              {profile.github_url && (
                <a href={profile.github_url} target="_blank" rel="noopener noreferrer" className="text-slate-600 hover:text-brand-600 flex items-center gap-1">
                  <Github className="w-3.5 h-3.5" /> GitHub
                </a>
              )}
              {profile.linkedin_url && (
                <a href={profile.linkedin_url} target="_blank" rel="noopener noreferrer" className="text-slate-600 hover:text-brand-600 flex items-center gap-1">
                  <Linkedin className="w-3.5 h-3.5" /> LinkedIn
                </a>
              )}
              {profile.portfolio_url && (
                <a href={profile.portfolio_url} target="_blank" rel="noopener noreferrer" className="text-slate-600 hover:text-brand-600 flex items-center gap-1">
                  <Globe className="w-3.5 h-3.5" /> Portfolio
                </a>
              )}
            </div>

          </div>

        </div>
      </div>

      {/* Bio & About */}
      {profile.bio && (
        <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-subtle space-y-2">
          <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider text-slate-400">
            About & Career Focus
          </h2>
          <p className="text-xs text-slate-700 leading-relaxed whitespace-pre-line">
            {profile.bio}
          </p>
        </div>
      )}

      {/* Skills & Endorsements */}
      {profile.skills && profile.skills.length > 0 && (
        <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-subtle space-y-3">
          <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider text-slate-400">
            Skills & Competencies
          </h2>
          <div className="flex flex-wrap gap-2">
            {profile.skills.map((s) => (
              <span
                key={s}
                className="px-3 py-1.5 rounded-xl bg-slate-50 border border-slate-200 text-xs font-semibold text-slate-700 flex items-center gap-1.5"
              >
                <CheckCircle2 className="w-3.5 h-3.5 text-brand-600" />
                {s}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Experience History */}
      {profile.work_experiences && profile.work_experiences.length > 0 && (
        <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-subtle space-y-4">
          <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider text-slate-400">
            Experience History
          </h2>
          <div className="space-y-4 divide-y divide-slate-100">
            {profile.work_experiences.map((exp, i) => (
              <div key={i} className={`space-y-1 ${i > 0 ? 'pt-4' : ''}`}>
                <div className="flex items-center justify-between">
                  <h3 className="text-xs font-bold text-slate-900">{exp.title}</h3>
                  <span className="text-[11px] font-medium text-slate-400">
                    {exp.start_date} — {exp.is_current ? 'Present' : exp.end_date}
                  </span>
                </div>
                <p className="text-xs font-semibold text-brand-700">{exp.company} • {exp.location}</p>
                {exp.description && (
                  <p className="text-xs text-slate-600 pt-1 leading-relaxed">{exp.description}</p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Education */}
      {profile.educations && profile.educations.length > 0 && (
        <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-subtle space-y-4">
          <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider text-slate-400">
            Education
          </h2>
          <div className="space-y-3">
            {profile.educations.map((edu, i) => (
              <div key={i} className="space-y-0.5">
                <h3 className="text-xs font-bold text-slate-900">{edu.institution}</h3>
                <p className="text-xs text-slate-600">{edu.degree} in {edu.field_of_study}</p>
                <p className="text-[11px] text-slate-400">
                  {edu.start_year} — {edu.end_year} {edu.grade ? `• ${edu.grade}` : ''}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Modals */}
      <ConnectModal
        isOpen={connectOpen}
        target={{ profile }}
        onClose={() => setConnectOpen(false)}
        onSuccess={fetchProfile}
      />

      <MentorshipModal
        isOpen={mentorOpen}
        mentor={profile}
        onClose={() => setMentorOpen(false)}
        onSuccess={fetchProfile}
      />

    </div>
  );
};
