import React, { useState, useEffect } from 'react';
import { 
  Briefcase, Search, Bookmark, BookmarkCheck, ExternalLink, 
  Plus, MapPin, Building, DollarSign, Calendar, CheckCircle2, Clock 
} from 'lucide-react';
import { Job } from '../types';
import { api } from '../services/api';
import { useAuth } from '../context/AuthContext';

export const JobsPage: React.FC = () => {
  const { user } = useAuth();
  const [jobs, setJobs] = useState<Job[]>([]);
  const [activeTab, setActiveTab] = useState<'all' | 'saved'>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [workMode, setWorkMode] = useState('All');
  const [employmentType, setEmploymentType] = useState('All');
  const [isLoading, setIsLoading] = useState(true);

  // Application & Post Job Modals
  const [selectedJobForApply, setSelectedJobForApply] = useState<Job | null>(null);
  const [coverNote, setCoverNote] = useState('');
  const [isApplying, setIsApplying] = useState(false);
  const [applySuccess, setApplySuccess] = useState(false);

  const [showPostJobModal, setShowPostJobModal] = useState(false);
  const [newJob, setNewJob] = useState({
    title: '',
    company: '',
    location: 'Remote',
    work_mode: 'Remote',
    employment_type: 'Full-time',
    description: '',
    requirements: '',
    required_skills: '',
    salary_range: '$120k - $160k',
    external_url: '',
  });

  const fetchJobs = async () => {
    setIsLoading(true);
    try {
      if (activeTab === 'saved') {
        const data = await api.getSavedJobs();
        setJobs(data);
      } else {
        const data = await api.getJobs({
          query: searchQuery || undefined,
          work_mode: workMode !== 'All' ? workMode : undefined,
          employment_type: employmentType !== 'All' ? employmentType : undefined,
        });
        setJobs(data);
      }
    } catch (err) {
      console.error('Failed to load jobs', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, [activeTab, searchQuery, workMode, employmentType]);

  const handleToggleSave = async (jobId: string) => {
    try {
      await api.toggleSaveJob(jobId);
      setJobs(jobs.map(j => j.id === jobId ? { ...j, is_saved: !j.is_saved } : j));
    } catch (err) {
      console.error('Failed to toggle save', err);
    }
  };

  const handleApplySubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedJobForApply) return;
    setIsApplying(true);
    try {
      await api.applyToJob(selectedJobForApply.id, { cover_note: coverNote });
      setApplySuccess(true);
      setTimeout(() => {
        setApplySuccess(false);
        setSelectedJobForApply(null);
        setCoverNote('');
        fetchJobs();
      }, 1500);
    } catch (err) {
      console.error('Failed to apply', err);
    } finally {
      setIsApplying(false);
    }
  };

  const handleCreateJobSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const skillsArray = newJob.required_skills
        ? newJob.required_skills.split(',').map(s => s.trim())
        : [];
      await api.createJob({
        ...newJob,
        required_skills: skillsArray,
      });
      setShowPostJobModal(false);
      fetchJobs();
    } catch (err) {
      console.error('Failed to create job', err);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      
      {/* Header Banner */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-subtle flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-bold mb-2">
            <Briefcase className="w-3.5 h-3.5 text-emerald-600" />
            Verified Alumni Career Pipeline
          </div>
          <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">
            Jobs & Internship Opportunities
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Exclusive openings shared directly by university alumni and corporate recruiters
          </p>
        </div>

        {(user?.role === 'alumni' || user?.role === 'admin') && (
          <button
            onClick={() => setShowPostJobModal(true)}
            className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shadow-sm flex items-center gap-1.5 transition-all"
          >
            <Plus className="w-4 h-4" />
            Post Opportunity
          </button>
        )}
      </div>

      {/* Tabs and Filters */}
      <div className="p-4 bg-white rounded-2xl border border-slate-200 shadow-subtle flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setActiveTab('all')}
            className={`px-3.5 py-1.5 rounded-xl font-bold transition-colors ${
              activeTab === 'all' ? 'bg-slate-900 text-white' : 'text-slate-600 hover:bg-slate-100'
            }`}
          >
            All Openings
          </button>
          <button
            onClick={() => setActiveTab('saved')}
            className={`px-3.5 py-1.5 rounded-xl font-bold transition-colors ${
              activeTab === 'saved' ? 'bg-slate-900 text-white' : 'text-slate-600 hover:bg-slate-100'
            }`}
          >
            Saved Opportunities
          </button>
        </div>

        {activeTab === 'all' && (
          <div className="flex flex-wrap items-center gap-2.5">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search title, company, skills..."
              className="p-2 rounded-xl border border-slate-200 bg-slate-50 font-medium text-slate-700 focus:outline-none min-w-[200px]"
            />
            <select
              value={workMode}
              onChange={(e) => setWorkMode(e.target.value)}
              className="p-2 rounded-xl border border-slate-200 bg-slate-50 font-medium text-slate-700 focus:outline-none"
            >
              <option value="All">All Modes</option>
              <option value="Remote">Remote</option>
              <option value="Hybrid">Hybrid</option>
              <option value="On-site">On-site</option>
            </select>
            <select
              value={employmentType}
              onChange={(e) => setEmploymentType(e.target.value)}
              className="p-2 rounded-xl border border-slate-200 bg-slate-50 font-medium text-slate-700 focus:outline-none"
            >
              <option value="All">All Types</option>
              <option value="Full-time">Full-time</option>
              <option value="Internship">Internship</option>
            </select>
          </div>
        )}
      </div>

      {/* Jobs List */}
      {isLoading ? (
        <div className="space-y-4 py-6">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-36 rounded-2xl bg-white border border-slate-200 animate-pulse p-5" />
          ))}
        </div>
      ) : jobs.length === 0 ? (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center text-xs text-slate-500">
          No job opportunities found matching criteria.
        </div>
      ) : (
        <div className="space-y-4">
          {jobs.map((j) => (
            <div
              key={j.id}
              className="bg-white rounded-2xl border border-slate-200 p-6 shadow-subtle hover:shadow-premium transition-all space-y-3"
            >
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <h3 className="text-base font-bold text-slate-900">{j.title}</h3>
                    {j.is_featured && (
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-800">
                        Featured
                      </span>
                    )}
                  </div>
                  <p className="text-xs font-semibold text-brand-700 flex items-center gap-3">
                    <span className="flex items-center gap-1">
                      <Building className="w-3.5 h-3.5 text-slate-400" />
                      {j.company}
                    </span>
                    <span className="flex items-center gap-1 text-slate-500">
                      <MapPin className="w-3.5 h-3.5 text-slate-400" />
                      {j.location} ({j.work_mode})
                    </span>
                    {j.salary_range && (
                      <span className="flex items-center gap-1 text-emerald-700">
                        <DollarSign className="w-3.5 h-3.5" />
                        {j.salary_range}
                      </span>
                    )}
                  </p>
                </div>

                <div className="flex items-center gap-2 w-full sm:w-auto justify-end">
                  <button
                    onClick={() => handleToggleSave(j.id)}
                    className="p-2 rounded-xl border border-slate-200 hover:bg-slate-50 text-slate-500 transition-colors"
                    title={j.is_saved ? 'Remove from saved' : 'Save opportunity'}
                  >
                    {j.is_saved ? <BookmarkCheck className="w-4 h-4 text-brand-600" /> : <Bookmark className="w-4 h-4" />}
                  </button>

                  {j.external_url ? (
                    <a
                      href={j.external_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="px-4 py-2 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-bold text-xs flex items-center gap-1.5 shadow-sm transition-all"
                    >
                      Apply on Company Site <ExternalLink className="w-3.5 h-3.5" />
                    </a>
                  ) : (
                    <button
                      onClick={() => setSelectedJobForApply(j)}
                      disabled={j.has_applied}
                      className={`px-4 py-2 rounded-xl font-bold text-xs flex items-center gap-1.5 shadow-sm transition-all ${
                        j.has_applied
                          ? 'bg-emerald-100 text-emerald-800 cursor-default'
                          : 'bg-emerald-600 hover:bg-emerald-700 text-white'
                      }`}
                    >
                      {j.has_applied ? 'Applied ✓' : 'Quick Apply'}
                    </button>
                  )}
                </div>
              </div>

              <p className="text-xs text-slate-600 leading-relaxed">
                {j.description}
              </p>

              {j.required_skills && j.required_skills.length > 0 && (
                <div className="flex flex-wrap items-center gap-1.5 pt-1">
                  <span className="text-[11px] font-semibold text-slate-400">Required Skills:</span>
                  {j.required_skills.map((sk) => (
                    <span key={sk} className="px-2 py-0.5 rounded text-[10px] font-medium bg-slate-100 text-slate-700">
                      {sk}
                    </span>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Apply Modal */}
      {selectedJobForApply && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-elevated border border-slate-200">
            <h3 className="text-base font-bold text-slate-900 mb-1">
              Apply to {selectedJobForApply.title}
            </h3>
            <p className="text-xs text-slate-500 mb-4">{selectedJobForApply.company} • {selectedJobForApply.location}</p>

            {applySuccess ? (
              <div className="p-6 text-center space-y-2">
                <CheckCircle2 className="w-10 h-10 text-emerald-600 mx-auto" />
                <h4 className="font-bold text-slate-900 text-sm">Application Submitted!</h4>
                <p className="text-xs text-slate-500">Your profile credentials were transmitted to the alumnus recruiter.</p>
              </div>
            ) : (
              <form onSubmit={handleApplySubmit} className="space-y-4 text-xs">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">
                    Introduction / Cover Note to Alumnus Recruiter
                  </label>
                  <textarea
                    rows={4}
                    value={coverNote}
                    onChange={(e) => setCoverNote(e.target.value)}
                    placeholder="Briefly state why you're a great fit for this role and your experience with required technologies..."
                    className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none resize-none"
                  />
                </div>

                <div className="flex justify-end gap-2 pt-2 border-t border-slate-100">
                  <button
                    type="button"
                    onClick={() => setSelectedJobForApply(null)}
                    className="px-4 py-2 font-semibold text-slate-600 hover:bg-slate-100 rounded-xl"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={isApplying}
                    className="px-5 py-2 font-bold text-white bg-emerald-600 hover:bg-emerald-700 rounded-xl shadow-sm"
                  >
                    {isApplying ? 'Submitting...' : 'Confirm Application'}
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}

      {/* Post Job Modal (For Alumni & Admin) */}
      {showPostJobModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-elevated border border-slate-200 max-h-[90vh] overflow-y-auto">
            <h3 className="text-base font-bold text-slate-900 mb-1">Post Opportunity for Students</h3>
            <p className="text-xs text-slate-500 mb-4">Share job or internship openings from your company</p>

            <form onSubmit={handleCreateJobSubmit} className="space-y-3.5 text-xs">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Job Title *</label>
                  <input
                    type="text"
                    required
                    value={newJob.title}
                    onChange={(e) => setNewJob({ ...newJob, title: e.target.value })}
                    placeholder="e.g. Software Engineer"
                    className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Company *</label>
                  <input
                    type="text"
                    required
                    value={newJob.company}
                    onChange={(e) => setNewJob({ ...newJob, company: e.target.value })}
                    placeholder="e.g. Stripe"
                    className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none"
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-2">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Location</label>
                  <input
                    type="text"
                    value={newJob.location}
                    onChange={(e) => setNewJob({ ...newJob, location: e.target.value })}
                    className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Work Mode</label>
                  <select
                    value={newJob.work_mode}
                    onChange={(e) => setNewJob({ ...newJob, work_mode: e.target.value })}
                    className="w-full p-2.5 rounded-xl border border-slate-200 bg-white focus:outline-none"
                  >
                    <option value="Remote">Remote</option>
                    <option value="Hybrid">Hybrid</option>
                    <option value="On-site">On-site</option>
                  </select>
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Employment Type</label>
                  <select
                    value={newJob.employment_type}
                    onChange={(e) => setNewJob({ ...newJob, employment_type: e.target.value })}
                    className="w-full p-2.5 rounded-xl border border-slate-200 bg-white focus:outline-none"
                  >
                    <option value="Full-time">Full-time</option>
                    <option value="Internship">Internship</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Required Skills (Comma separated)</label>
                <input
                  type="text"
                  value={newJob.required_skills}
                  onChange={(e) => setNewJob({ ...newJob, required_skills: e.target.value })}
                  placeholder="Python, React, TypeScript, Docker"
                  className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none"
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Role Description *</label>
                <textarea
                  rows={3}
                  required
                  value={newJob.description}
                  onChange={(e) => setNewJob({ ...newJob, description: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none resize-none"
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">External Application Link</label>
                <input
                  type="url"
                  value={newJob.external_url}
                  onChange={(e) => setNewJob({ ...newJob, external_url: e.target.value })}
                  placeholder="https://company.com/careers/..."
                  className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowPostJobModal(false)}
                  className="px-4 py-2 font-semibold text-slate-600 hover:bg-slate-100 rounded-xl"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 font-bold text-white bg-emerald-600 hover:bg-emerald-700 rounded-xl shadow-sm"
                >
                  Publish Listing
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
};
