import React, { useState, useEffect } from 'react';
import { 
  Award, Calendar, Clock, Check, X, Search, 
  ExternalLink, Plus, CheckCircle2, AlertCircle, MessageSquare 
} from 'lucide-react';
import { Profile, MentorshipRequest, MentorshipSession } from '../types';
import { api } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { MentorshipModal } from '../components/MentorshipModal';
import { Avatar } from '../components/Avatar';
import { ENGINEERING_DEPARTMENTS, ENGINEERING_INDUSTRIES } from '../constants/engineeringData';

export const MentorshipPage: React.FC = () => {
  const { user, profile } = useAuth();

  const [activeTab, setActiveTab] = useState<'mentors' | 'requests' | 'sessions'>('mentors');
  const [mentors, setMentors] = useState<Profile[]>([]);
  const [requests, setRequests] = useState<MentorshipRequest[]>([]);
  const [sessions, setSessions] = useState<MentorshipSession[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Search & filter
  const [industryFilter, setIndustryFilter] = useState('');
  const [departmentFilter, setDepartmentFilter] = useState('');
  const [skillFilter, setSkillFilter] = useState('');

  // Modals
  const [selectedMentor, setSelectedMentor] = useState<Profile | null>(null);
  const [showScheduleModal, setShowScheduleModal] = useState(false);
  const [scheduleData, setScheduleData] = useState({
    mentorship_request_id: '',
    title: 'Bi-weekly Mentorship & Technical Strategy Review',
    scheduled_at: new Date(Date.now() + 86400000 * 2).toISOString().slice(0, 16),
    duration_minutes: 45,
    meeting_link: 'https://meet.google.com/alm-mentor-session',
    notes: 'Discuss portfolio architectures and interview preparation roadmap.',
  });

  const fetchData = async () => {
    setIsLoading(true);
    try {
      const [mList, rList, sList] = await Promise.all([
        api.getMentors({
          industry: industryFilter || undefined,
          department: departmentFilter || undefined,
          skill: skillFilter || undefined,
        }),
        api.getMentorshipRequests(),
        api.getMentorshipSessions(),
      ]);
      setMentors(mList);
      setRequests(rList);
      setSessions(sList);
    } catch (err) {
      console.error('Failed to load mentorship data', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [industryFilter, departmentFilter, skillFilter]);

  const handleUpdateStatus = async (requestId: string, status: string) => {
    try {
      await api.updateMentorshipStatus(requestId, status);
      fetchData();
    } catch (err) {
      console.error('Failed to update status', err);
    }
  };

  const handleScheduleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.scheduleSession({
        ...scheduleData,
        scheduled_at: new Date(scheduleData.scheduled_at).toISOString(),
      });
      setShowScheduleModal(false);
      fetchData();
    } catch (err) {
      console.error('Failed to schedule session', err);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      
      {/* Header Banner */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-subtle flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-50 border border-amber-200 text-amber-800 text-xs font-bold mb-2">
            <Award className="w-3.5 h-3.5 text-amber-600" />
            1-on-1 Mentorship Module
          </div>
          <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">
            Alumni Guidance & Mentorship
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Connect with experienced graduates for structured technical coaching, resume critiques, and industry roadmaps
          </p>
        </div>

        {sessions.length > 0 && (
          <button
            onClick={() => setShowScheduleModal(true)}
            className="px-4 py-2 rounded-xl bg-amber-600 hover:bg-amber-700 text-white font-bold text-xs shadow-sm flex items-center gap-1.5 transition-all"
          >
            <Plus className="w-4 h-4" />
            Schedule Session
          </button>
        )}
      </div>

      {/* Navigation Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-200 pb-2 text-xs font-bold">
        <button
          onClick={() => setActiveTab('mentors')}
          className={`px-4 py-2 rounded-xl transition-all ${
            activeTab === 'mentors' ? 'bg-amber-600 text-white shadow-sm' : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          Available Mentors ({mentors.length})
        </button>
        <button
          onClick={() => setActiveTab('requests')}
          className={`px-4 py-2 rounded-xl transition-all flex items-center gap-1.5 ${
            activeTab === 'requests' ? 'bg-amber-600 text-white shadow-sm' : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          Applications & Requests ({requests.length})
        </button>
        <button
          onClick={() => setActiveTab('sessions')}
          className={`px-4 py-2 rounded-xl transition-all flex items-center gap-1.5 ${
            activeTab === 'sessions' ? 'bg-amber-600 text-white shadow-sm' : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          Scheduled Sessions ({sessions.length})
        </button>
      </div>

      {/* Tab 1: Available Mentors */}
      {activeTab === 'mentors' && (
        <div className="space-y-5">
          <div className="p-3.5 bg-white rounded-xl border border-slate-200 flex flex-wrap gap-3 text-xs">
            <select
              value={industryFilter}
              onChange={(e) => setIndustryFilter(e.target.value)}
              className="p-2 rounded-lg border border-slate-200 bg-slate-50 font-medium text-slate-700 focus:outline-none max-w-[200px]"
            >
              <option value="">All Industries</option>
              {ENGINEERING_INDUSTRIES.map((ind) => (
                <option key={ind} value={ind}>{ind}</option>
              ))}
            </select>
            <select
              value={departmentFilter}
              onChange={(e) => setDepartmentFilter(e.target.value)}
              className="p-2 rounded-lg border border-slate-200 bg-slate-50 font-medium text-slate-700 focus:outline-none max-w-[220px]"
            >
              <option value="">All Departments</option>
              {ENGINEERING_DEPARTMENTS.map((dept) => (
                <option key={dept} value={dept}>{dept}</option>
              ))}
            </select>
            <input
              type="text"
              value={skillFilter}
              onChange={(e) => setSkillFilter(e.target.value)}
              placeholder="Filter by mentor skills..."
              className="p-2 rounded-lg border border-slate-200 bg-slate-50 font-medium text-slate-700 focus:outline-none flex-1 min-w-[200px]"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {mentors.map((m) => (
              <div
                key={m.user_id}
                className="bg-white rounded-2xl border border-slate-200 p-5 shadow-subtle hover:shadow-premium transition-all flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-start gap-3.5">
                    <Avatar
                      name={m.full_name}
                      size="md"
                      className="rounded-xl flex-shrink-0"
                    />
                    <div className="min-w-0 flex-1">
                      <h3 className="font-bold text-slate-900 text-sm truncate">{m.full_name}</h3>
                      <p className="text-xs font-semibold text-amber-700 truncate">{m.current_job_title}</p>
                      <p className="text-[11px] text-slate-500 truncate">{m.current_company} • Class of {m.graduation_year}</p>
                    </div>
                  </div>

                  {m.bio && (
                    <p className="text-xs text-slate-600 line-clamp-2 mt-3 leading-relaxed">
                      {m.bio}
                    </p>
                  )}

                  {m.mentorship_topics && m.mentorship_topics.length > 0 && (
                    <div className="mt-3 flex flex-wrap gap-1">
                      {m.mentorship_topics.map((t) => (
                        <span key={t} className="px-2 py-0.5 rounded text-[10px] font-semibold bg-amber-50 text-amber-800 border border-amber-200">
                          {t}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">
                  <span className="text-[11px] text-slate-400 font-medium">Capacity: Open</span>
                  <button
                    onClick={() => setSelectedMentor(m)}
                    className="px-4 py-1.5 rounded-lg bg-amber-600 hover:bg-amber-700 text-white font-bold text-xs shadow-sm transition-all"
                  >
                    Request Mentorship
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 2: Requests & Applications */}
      {activeTab === 'requests' && (
        <div className="space-y-4">
          {requests.length === 0 ? (
            <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center text-xs text-slate-500">
              No mentorship applications currently on file.
            </div>
          ) : (
            requests.map((r) => {
              const isMentor = r.mentor_id === user?.id;
              const counterpart = isMentor ? r.student_profile : r.mentor_profile;
              return (
                <div
                  key={r.id}
                  className="bg-white rounded-2xl border border-slate-200 p-5 shadow-subtle space-y-3"
                >
                  <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
                    <div className="flex items-center gap-3">
                      <Avatar
                        name={counterpart?.full_name || 'User'}
                        size="sm"
                        className="rounded-full flex-shrink-0"
                      />
                      <div>
                        <p className="font-bold text-slate-900 text-xs">
                          {isMentor ? `Student: ${counterpart?.full_name}` : `Mentor: ${counterpart?.full_name}`}
                        </p>
                        <p className="text-[11px] text-slate-500">
                          {counterpart?.current_job_title || counterpart?.department} • Cadence: {r.preferred_frequency}
                        </p>
                      </div>
                    </div>

                    <span
                      className={`px-3 py-1 rounded-full text-xs font-bold capitalize ${
                        r.status === 'accepted'
                          ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                          : r.status === 'declined'
                          ? 'bg-rose-50 text-rose-700 border border-rose-200'
                          : 'bg-amber-50 text-amber-700 border border-amber-200'
                      }`}
                    >
                      {r.status}
                    </span>
                  </div>

                  <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs text-slate-700">
                    <span className="font-bold text-slate-900 block mb-1">Stated Learning Goals:</span>
                    {r.goals_description}
                  </div>

                  {r.response_note && (
                    <div className="p-3 bg-amber-50/60 rounded-xl border border-amber-200 text-xs text-amber-900">
                      <span className="font-bold block mb-1">Mentor Note:</span>
                      {r.response_note}
                    </div>
                  )}

                  {/* Actions for mentor if pending */}
                  {isMentor && r.status === 'pending' && (
                    <div className="flex items-center gap-2 pt-2 border-t border-slate-100">
                      <button
                        onClick={() => handleUpdateStatus(r.id, 'accepted')}
                        className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs flex items-center gap-1"
                      >
                        <Check className="w-4 h-4" /> Accept Mentorship
                      </button>
                      <button
                        onClick={() => handleUpdateStatus(r.id, 'declined')}
                        className="px-4 py-2 rounded-xl border border-slate-200 hover:bg-slate-50 text-slate-700 font-semibold text-xs"
                      >
                        Decline
                      </button>
                    </div>
                  )}
                </div>
              );
            })
          )}
        </div>
      )}

      {/* Tab 3: Scheduled Sessions */}
      {activeTab === 'sessions' && (
        <div className="space-y-4">
          {sessions.length === 0 ? (
            <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center text-xs text-slate-500">
              No sessions scheduled. Once your mentorship request is accepted, schedule your 45-minute meetings here.
            </div>
          ) : (
            sessions.map((s) => (
              <div
                key={s.id}
                className="bg-white rounded-2xl border border-slate-200 p-5 shadow-subtle flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4"
              >
                <div className="space-y-1">
                  <h3 className="font-bold text-slate-900 text-sm">{s.title}</h3>
                  <div className="flex flex-wrap items-center gap-3 text-xs text-slate-500">
                    <span className="flex items-center gap-1 text-brand-700 font-semibold">
                      <Calendar className="w-3.5 h-3.5" />
                      {new Date(s.scheduled_at).toLocaleDateString()}
                    </span>
                    <span className="flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5 text-slate-400" />
                      {new Date(s.scheduled_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} ({s.duration_minutes}m)
                    </span>
                  </div>
                  {s.notes && (
                    <p className="text-xs text-slate-600 pt-1">{s.notes}</p>
                  )}
                </div>

                <div className="flex items-center gap-2 w-full sm:w-auto">
                  {s.meeting_link && (
                    <a
                      href={s.meeting_link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex-1 sm:flex-none px-4 py-2 rounded-xl bg-amber-600 hover:bg-amber-700 text-white font-bold text-xs flex items-center justify-center gap-1.5 shadow-sm transition-all"
                    >
                      Join Google Meet <ExternalLink className="w-3.5 h-3.5" />
                    </a>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {/* Schedule Session Modal */}
      {showScheduleModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-elevated border border-slate-200">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-4">
              <h3 className="text-base font-bold text-slate-900">Schedule Mentorship Session</h3>
              <button onClick={() => setShowScheduleModal(false)} className="text-slate-400 hover:text-slate-600 text-xs">✕</button>
            </div>

            <form onSubmit={handleScheduleSubmit} className="space-y-4 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Session Title *</label>
                <input
                  type="text"
                  required
                  value={scheduleData.title}
                  onChange={(e) => setScheduleData({ ...scheduleData, title: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none"
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Meeting Date & Time *</label>
                <input
                  type="datetime-local"
                  required
                  value={scheduleData.scheduled_at}
                  onChange={(e) => setScheduleData({ ...scheduleData, scheduled_at: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none"
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Virtual Meeting Link</label>
                <input
                  type="url"
                  value={scheduleData.meeting_link}
                  onChange={(e) => setScheduleData({ ...scheduleData, meeting_link: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none"
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Agenda / Discussion Notes</label>
                <textarea
                  rows={3}
                  value={scheduleData.notes}
                  onChange={(e) => setScheduleData({ ...scheduleData, notes: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none resize-none"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowScheduleModal(false)}
                  className="px-4 py-2 font-semibold text-slate-600 hover:bg-slate-100 rounded-xl"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 font-bold text-white bg-amber-600 hover:bg-amber-700 rounded-xl shadow-sm"
                >
                  Schedule Call
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Mentorship Application Modal */}
      <MentorshipModal
        isOpen={!!selectedMentor}
        mentor={selectedMentor}
        onClose={() => setSelectedMentor(null)}
        onSuccess={fetchData}
      />

    </div>
  );
};
