import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Sparkles, Users, Award, Briefcase, Calendar, MessageSquare, 
  ArrowRight, CheckCircle2, Clock, MapPin, ExternalLink, 
  UserPlus, Check, X, Shield, ChevronRight 
} from 'lucide-react';
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, 
  ResponsiveContainer, BarChart, Bar 
} from 'recharts';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import { api } from '../services/api';
import { Recommendation, Job, AlumniEvent, MentorshipSession } from '../types';
import { RecommendationCard } from '../components/RecommendationCard';
import { ConnectModal } from '../components/ConnectModal';
import { MentorshipModal } from '../components/MentorshipModal';
import { Avatar } from '../components/Avatar';

export const DashboardPage: React.FC = () => {
  const { user, profile } = useAuth();
  const navigate = useNavigate();
  const toast = useToast();

  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [events, setEvents] = useState<AlumniEvent[]>([]);
  const [sessions, setSessions] = useState<MentorshipSession[]>([]);
  const [pendingRequests, setPendingRequests] = useState<any[]>([]);
  const [connectionsCount, setConnectionsCount] = useState<number>(0);
  const [dashboardStats, setDashboardStats] = useState<any | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Modals state
  const [selectedRecForConnect, setSelectedRecForConnect] = useState<any | null>(null);
  const [selectedRecForMentor, setSelectedRecForMentor] = useState<any | null>(null);

  const fetchDashboardData = async () => {
    setIsLoading(true);
    try {
      const [recsData, jobsData, eventsData, sessionsData, requestsData, connsData, statsData] = await Promise.all([
        api.getRecommendations({ limit: 4 }),
        api.getJobs({ limit: 3 }),
        api.getEvents({ limit: 3 }),
        api.getMentorshipSessions(),
        api.getConnectionRequests(),
        api.getConnections(),
        api.getDashboardStats().catch(() => null),
      ]);

      setRecommendations(recsData);
      setJobs(jobsData);
      setEvents(eventsData);
      setSessions(sessionsData);
      setPendingRequests(requestsData.incoming || []);
      setConnectionsCount(statsData?.connections_count ?? connsData.length);
      setDashboardStats(statsData);
    } catch (err) {
      console.error('Failed to load dashboard data', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const handleAcceptRequest = async (requestId: string) => {
    try {
      await api.acceptConnectionRequest(requestId);
      toast.success('Connection request accepted!');
      fetchDashboardData();
    } catch (err: any) {
      toast.error(err.message || 'Failed to accept request');
    }
  };

  const handleRejectRequest = async (requestId: string) => {
    try {
      await api.rejectConnectionRequest(requestId);
      toast.info('Connection request declined');
      fetchDashboardData();
    } catch (err: any) {
      toast.error(err.message || 'Failed to reject request');
    }
  };

  const greetingTime = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 17) return 'Good afternoon';
    return 'Good evening';
  };

  const fallbackActivityData = [
    { day: 'Mon', connections: 2, messages: 5, sessions: 1 },
    { day: 'Tue', connections: 4, messages: 8, sessions: 0 },
    { day: 'Wed', connections: 3, messages: 12, sessions: 2 },
    { day: 'Thu', connections: 5, messages: 9, sessions: 1 },
    { day: 'Fri', connections: 7, messages: 15, sessions: 2 },
    { day: 'Sat', connections: 3, messages: 4, sessions: 0 },
    { day: 'Sun', connections: 2, messages: 6, sessions: 1 },
  ];

  const chartData = dashboardStats?.weekly_activity && dashboardStats.weekly_activity.length > 0
    ? dashboardStats.weekly_activity
    : fallbackActivityData;

  return (
    <div className="space-y-8 animate-fade-in">
      
      {/* 1. Header Banner */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-subtle">
        <div>
          <span className="text-xs font-bold text-brand-700 uppercase tracking-wider flex items-center gap-1.5 mb-1">
            <Sparkles className="w-3.5 h-3.5" />
            Personalized Networking Portal
          </span>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            {greetingTime()}, {profile?.full_name?.split(' ')[0] || 'Member'}! 👋
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            You have {recommendations.length} new high-compatibility alumni recommendations ready to explore.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Link
            to="/recommendations"
            className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-gradient-to-r from-brand-600 to-indigo-600 text-white text-xs font-bold shadow-sm hover:opacity-95 transition-all"
          >
            <Sparkles className="w-4 h-4" />
            AI Matches
          </Link>
          <Link
            to="/assistant"
            className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold transition-colors"
          >
            AI Assistant
          </Link>
        </div>
      </div>

      {/* 2. Top Metric Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 bg-white rounded-2xl border border-slate-200 shadow-subtle flex items-center justify-between">
          <div>
            <p className="text-xs text-slate-500 font-medium">My Network</p>
            <p className="text-2xl font-extrabold text-slate-900 mt-1">{connectionsCount}</p>
            <span className="text-[11px] text-emerald-600 font-medium">Active connections</span>
          </div>
          <div className="w-10 h-10 rounded-xl bg-brand-50 text-brand-600 flex items-center justify-center">
            <Users className="w-5 h-5" />
          </div>
        </div>

        <div className="p-5 bg-white rounded-2xl border border-slate-200 shadow-subtle flex items-center justify-between">
          <div>
            <p className="text-xs text-slate-500 font-medium">Pending Requests</p>
            <p className="text-2xl font-extrabold text-slate-900 mt-1">{pendingRequests.length}</p>
            <span className="text-[11px] text-brand-600 font-medium">Action required</span>
          </div>
          <div className="w-10 h-10 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center">
            <UserPlus className="w-5 h-5" />
          </div>
        </div>

        <div className="p-5 bg-white rounded-2xl border border-slate-200 shadow-subtle flex items-center justify-between">
          <div>
            <p className="text-xs text-slate-500 font-medium">Mentorship Sessions</p>
            <p className="text-2xl font-extrabold text-slate-900 mt-1">{sessions.length}</p>
            <span className="text-[11px] text-amber-600 font-medium">Scheduled</span>
          </div>
          <div className="w-10 h-10 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center">
            <Award className="w-5 h-5" />
          </div>
        </div>

        <div className="p-5 bg-white rounded-2xl border border-slate-200 shadow-subtle flex items-center justify-between">
          <div>
            <p className="text-xs text-slate-500 font-medium">Profile Strength</p>
            <p className="text-2xl font-extrabold text-slate-900 mt-1">
              {dashboardStats?.profile_completion_percentage ?? profile?.profile_completion_percentage ?? 50}%
            </p>
            <span className="text-[11px] text-indigo-600 font-medium">
              {(dashboardStats?.profile_completion_percentage ?? profile?.profile_completion_percentage) >= 75 ? 'All set!' : 'Needs details'}
            </span>
          </div>
          <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
            <CheckCircle2 className="w-5 h-5" />
          </div>
        </div>
      </div>

      {/* Profile Completion Guidance */}
      {dashboardStats?.missing_steps && dashboardStats.missing_steps.length > 0 && (
        <div className="bg-gradient-to-r from-brand-50 via-indigo-50/50 to-white p-5 rounded-2xl border border-brand-200 shadow-subtle flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1.5">
            <div className="flex items-center gap-2">
              <span className="text-[10px] font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-brand-600 text-white">
                Profile Optimization
              </span>
              <span className="text-xs font-bold text-slate-800">
                Boost AI Match Accuracy ({dashboardStats.profile_completion_percentage || 50}% complete)
              </span>
            </div>
            <p className="text-xs text-slate-600">
              Complete these steps so the 7-factor engine can calculate maximum compatibility:
            </p>
            <div className="flex flex-wrap gap-2 pt-1">
              {dashboardStats.missing_steps.map((step: string, idx: number) => (
                <span key={idx} className="inline-flex items-center gap-1 text-[11px] font-medium text-brand-900 bg-white px-2.5 py-1 rounded-lg border border-brand-200 shadow-2xs">
                  <span className="w-1.5 h-1.5 rounded-full bg-brand-500" />
                  {step}
                </span>
              ))}
            </div>
          </div>
          <Link
            to="/edit-profile"
            className="shrink-0 inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-brand-600 hover:bg-brand-700 text-white text-xs font-bold transition-all shadow-xs"
          >
            Update Profile <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      )}

      {/* 3. Main Dashboard Grid: AI Recommendations & Weekly Trend */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left 2 Cols: AI Recommendations */}
        <div className="lg:col-span-2 space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-brand-600" />
                AI-Recommended Alumni Matches
              </h2>
              <p className="text-xs text-slate-500">Based on your career interests, skills, and department</p>
            </div>
            <Link to="/recommendations" className="text-xs font-bold text-brand-600 hover:text-brand-700 flex items-center gap-1">
              View All ({recommendations.length})
              <ChevronRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="grid grid-cols-1 gap-5">
            {recommendations.slice(0, 3).map((rec) => (
              <RecommendationCard
                key={rec.profile.user_id}
                recommendation={rec}
                onConnect={(r) => setSelectedRecForConnect({ profile: r.profile, starter: r.conversation_starter })}
                onRequestMentorship={(r) => setSelectedRecForMentor(r.profile)}
              />
            ))}
          </div>

          {/* Weekly Activity Recharts Section */}
          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-subtle">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-sm font-bold text-slate-900">Weekly Networking Activity</h3>
                <p className="text-xs text-slate-500">Connections, messages exchanged, and mentorship sessions</p>
              </div>
            </div>
            <div className="h-60 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorMessages" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#6366f1" stopOpacity={0.4} />
                      <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="colorConnections" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#10b981" stopOpacity={0.4} />
                      <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                  <XAxis dataKey="day" tick={{ fontSize: 11, fill: '#64748b' }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fontSize: 11, fill: '#64748b' }} axisLine={false} tickLine={false} />
                  <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderRadius: '12px', border: '1px solid #e2e8f0', fontSize: '12px' }} />
                  <Area type="monotone" dataKey="messages" stroke="#6366f1" strokeWidth={2} fillOpacity={1} fill="url(#colorMessages)" name="Messages" />
                  <Area type="monotone" dataKey="connections" stroke="#10b981" strokeWidth={2} fillOpacity={1} fill="url(#colorConnections)" name="New Connections" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

        </div>

        {/* Right Col: Pending Requests, Upcoming Mentorship, Jobs & Events */}
        <div className="space-y-6">
          
          {/* Incoming Requests Box */}
          <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-subtle space-y-3">
            <h3 className="text-sm font-bold text-slate-900 flex items-center justify-between">
              <span>Incoming Connection Requests</span>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-brand-50 text-brand-700">
                {pendingRequests.length}
              </span>
            </h3>

            {pendingRequests.length === 0 ? (
              <p className="text-xs text-slate-400 py-4 text-center">No pending connection requests right now.</p>
            ) : (
              <div className="space-y-3">
                {pendingRequests.map((req) => (
                  <div key={req.id} className="p-3 rounded-xl bg-slate-50 border border-slate-200 text-xs space-y-2">
                    <div className="flex items-center gap-2.5">
                      <Avatar name={req.sender_profile?.full_name} size="sm" />
                      <div className="min-w-0 flex-1">
                        <p className="font-bold text-slate-900 truncate">{req.sender_profile?.full_name}</p>
                        <p className="text-[11px] text-slate-500 truncate">{req.sender_profile?.current_job_title || req.sender_profile?.department}</p>
                      </div>
                    </div>
                    {req.message && (
                      <p className="text-[11px] text-slate-600 bg-white p-2 rounded-lg border border-slate-100 italic">
                        "{req.message}"
                      </p>
                    )}
                    <div className="flex items-center gap-2 pt-1">
                      <button
                        onClick={() => handleAcceptRequest(req.id)}
                        className="flex-1 py-1.5 rounded-lg bg-brand-600 text-white font-bold text-[11px] hover:bg-brand-700 transition-colors flex items-center justify-center gap-1"
                      >
                        <Check className="w-3.5 h-3.5" /> Accept
                      </button>
                      <button
                        onClick={() => handleRejectRequest(req.id)}
                        className="flex-1 py-1.5 rounded-lg bg-slate-200 text-slate-700 font-semibold text-[11px] hover:bg-slate-300 transition-colors"
                      >
                        Decline
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Upcoming Mentorship Sessions */}
          <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-subtle space-y-3">
            <h3 className="text-sm font-bold text-slate-900 flex items-center justify-between">
              <span>Upcoming Mentorship</span>
              <Award className="w-4 h-4 text-amber-600" />
            </h3>

            {sessions.length === 0 ? (
              <div className="text-center py-4">
                <p className="text-xs text-slate-400">No scheduled sessions.</p>
                <Link to="/mentorship" className="mt-2 inline-block text-xs font-bold text-brand-600 hover:text-brand-700">
                  Find a Mentor →
                </Link>
              </div>
            ) : (
              sessions.slice(0, 2).map((s) => (
                <div key={s.id} className="p-3 rounded-xl bg-amber-50/60 border border-amber-200 text-xs space-y-1.5">
                  <p className="font-bold text-amber-950">{s.title}</p>
                  <p className="text-[11px] text-amber-800 flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {new Date(s.scheduled_at).toLocaleDateString()} at {new Date(s.scheduled_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </p>
                  {s.meeting_link && (
                    <a
                      href={s.meeting_link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 text-[11px] font-bold text-amber-900 hover:underline pt-1"
                    >
                      Join Google Meet <ExternalLink className="w-3 h-3" />
                    </a>
                  )}
                </div>
              ))
            )}
          </div>

          {/* Featured Alumni Jobs */}
          <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-subtle space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-slate-900">Alumni Opportunities</h3>
              <Link to="/jobs" className="text-xs font-bold text-brand-600 hover:text-brand-700">
                All Jobs →
              </Link>
            </div>

            <div className="space-y-2.5">
              {jobs.slice(0, 3).map((j) => (
                <div key={j.id} className="p-3 rounded-xl bg-slate-50 border border-slate-200 text-xs space-y-1">
                  <div className="flex items-center justify-between">
                    <p className="font-bold text-slate-900 truncate">{j.title}</p>
                    <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-200">
                      {j.work_mode}
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-500">{j.company} • {j.location}</p>
                </div>
              ))}
            </div>
          </div>

        </div>

      </div>

      {/* Modals for Connect & Mentorship */}
      <ConnectModal
        isOpen={!!selectedRecForConnect}
        target={selectedRecForConnect}
        onClose={() => setSelectedRecForConnect(null)}
        onSuccess={fetchDashboardData}
      />

      <MentorshipModal
        isOpen={!!selectedRecForMentor}
        mentor={selectedRecForMentor}
        onClose={() => setSelectedRecForMentor(null)}
        onSuccess={fetchDashboardData}
      />

    </div>
  );
};
