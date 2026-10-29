import React, { useState, useEffect } from 'react';
import { 
  Sparkles, SlidersHorizontal, RefreshCw, Filter, 
  Search, Award, Building, MapPin, Check, Info, AlertCircle 
} from 'lucide-react';
import { Recommendation, Profile } from '../types';
import { api } from '../services/api';
import { RecommendationCard } from '../components/RecommendationCard';
import { ConnectModal } from '../components/ConnectModal';
import { MentorshipModal } from '../components/MentorshipModal';
import { ENGINEERING_DEPARTMENTS, ENGINEERING_INDUSTRIES } from '../constants/engineeringData';

export const RecommendationsPage: React.FC = () => {
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);

  // Filters & sorting
  const [industry, setIndustry] = useState('');
  const [department, setDepartment] = useState('');
  const [skill, setSkill] = useState('');
  const [jobRole, setJobRole] = useState('');
  const [location, setLocation] = useState('');
  const [mentorshipOnly, setMentorshipOnly] = useState(false);
  const [sortBy, setSortBy] = useState('relevance');

  // Configurable Weights Modal
  const [showWeightModal, setShowWeightModal] = useState(false);
  const [weights, setWeights] = useState({
    career_weight: 0.25,
    skill_weight: 0.20,
    industry_weight: 0.20,
    semantic_weight: 0.15,
    academic_weight: 0.10,
    location_weight: 0.05,
    mentorship_weight: 0.05,
  });

  // Action Modals
  const [connectTarget, setConnectTarget] = useState<any | null>(null);
  const [mentorTarget, setMentorTarget] = useState<Profile | null>(null);

  const fetchRecommendations = async () => {
    setIsLoading(true);
    try {
      const data = await api.getRecommendations({
        industry: industry || undefined,
        department: department || undefined,
        skill: skill || undefined,
        job_role: jobRole || undefined,
        location: location || undefined,
        mentorship_only: mentorshipOnly || undefined,
        sort_by: sortBy,
      });
      setRecommendations(data);
    } catch (err) {
      console.error('Failed to load recommendations', err);
    } finally {
      setIsLoading(false);
    }
  };

  const loadWeights = async () => {
    try {
      const w = await api.getRecommendationWeights();
      setWeights(w);
    } catch (err) {
      console.error('Failed to load weights', err);
    }
  };

  useEffect(() => {
    fetchRecommendations();
    loadWeights();
  }, [industry, department, skill, jobRole, location, mentorshipOnly, sortBy]);

  const handleRefresh = async () => {
    setIsRefreshing(true);
    await fetchRecommendations();
    setIsRefreshing(false);
  };

  const handleSaveWeights = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.updateRecommendationWeights(weights);
      setShowWeightModal(false);
      fetchRecommendations();
    } catch (err) {
      console.error('Failed to save weights', err);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      
      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-subtle">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-brand-50 border border-brand-200 text-brand-700 text-xs font-bold mb-2">
            <Sparkles className="w-3.5 h-3.5 text-brand-600" />
            AI-Driven Compatibility Engine
          </div>
          <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">
            Personalized Connection Recommendations
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Alumni ranked by our 7-factor explainable machine learning scoring model
          </p>
        </div>

        <div className="flex items-center gap-2.5">
          <button
            onClick={() => setShowWeightModal(true)}
            className="px-3.5 py-2 rounded-xl text-xs font-bold border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 flex items-center gap-1.5 transition-colors"
          >
            <SlidersHorizontal className="w-3.5 h-3.5" />
            Tune AI Weights
          </button>
          <button
            onClick={handleRefresh}
            disabled={isRefreshing}
            className="px-3.5 py-2 rounded-xl text-xs font-bold bg-brand-600 hover:bg-brand-700 text-white shadow-sm flex items-center gap-1.5 transition-all disabled:opacity-60"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isRefreshing ? 'animate-spin' : ''}`} />
            Refresh
          </button>
        </div>
      </div>

      {/* Filter & Search Bar */}
      <div className="p-4 bg-white rounded-2xl border border-slate-200 shadow-subtle flex flex-wrap items-center justify-between gap-3 text-xs">
        
        <div className="flex flex-wrap items-center gap-3 flex-1 min-w-[280px]">
          {/* Industry dropdown */}
          <select
            value={industry}
            onChange={(e) => setIndustry(e.target.value)}
            className="p-2 rounded-xl border border-slate-200 bg-slate-50 font-medium text-slate-700 focus:outline-none focus:ring-2 focus:ring-brand-500/20 max-w-[190px]"
          >
            <option value="">All Industries</option>
            {ENGINEERING_INDUSTRIES.map((ind) => (
              <option key={ind} value={ind}>{ind}</option>
            ))}
          </select>

          {/* Department dropdown */}
          <select
            value={department}
            onChange={(e) => setDepartment(e.target.value)}
            className="p-2 rounded-xl border border-slate-200 bg-slate-50 font-medium text-slate-700 focus:outline-none focus:ring-2 focus:ring-brand-500/20 max-w-[210px]"
          >
            <option value="">All Departments</option>
            {ENGINEERING_DEPARTMENTS.map((dept) => (
              <option key={dept} value={dept}>{dept}</option>
            ))}
          </select>

          {/* Skill search */}
          <input
            type="text"
            value={skill}
            onChange={(e) => setSkill(e.target.value)}
            placeholder="Filter by skill (e.g. Python, React)..."
            className="p-2 rounded-xl border border-slate-200 bg-slate-50 font-medium text-slate-700 focus:outline-none focus:ring-2 focus:ring-brand-500/20 min-w-[180px]"
          />

          {/* Job Role search */}
          <input
            type="text"
            value={jobRole}
            onChange={(e) => setJobRole(e.target.value)}
            placeholder="Job role (e.g. ML Engineer, SRE)..."
            className="p-2 rounded-xl border border-slate-200 bg-slate-50 font-medium text-slate-700 focus:outline-none focus:ring-2 focus:ring-brand-500/20 w-44"
          />

          {/* Location filter */}
          <input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="Location..."
            className="p-2 rounded-xl border border-slate-200 bg-slate-50 font-medium text-slate-700 focus:outline-none focus:ring-2 focus:ring-brand-500/20 w-32"
          />

          {/* Mentorship Only Toggle */}
          <label className="flex items-center gap-1.5 text-xs font-semibold text-slate-700 cursor-pointer select-none">
            <input
              type="checkbox"
              checked={mentorshipOnly}
              onChange={(e) => setMentorshipOnly(e.target.checked)}
              className="w-4 h-4 text-brand-600 rounded"
            />
            <span>Active Mentors Only</span>
          </label>
        </div>

        {/* Sort selector */}
        <div className="flex items-center gap-2">
          <span className="text-slate-400 font-semibold">Sort:</span>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="p-2 rounded-xl border border-slate-200 bg-slate-50 font-medium text-slate-700 focus:outline-none"
          >
            <option value="relevance">Relevance (AI Compatibility)</option>
            <option value="experience">Years of Experience</option>
            <option value="grad_year">Graduation Year</option>
          </select>
        </div>

      </div>

      {/* Recommendations Feed */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5 py-8">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-64 rounded-2xl bg-white border border-slate-200 animate-pulse p-6 space-y-4">
              <div className="flex items-center gap-4">
                <div className="w-14 h-14 rounded-2xl bg-slate-200" />
                <div className="space-y-2 flex-1">
                  <div className="h-4 bg-slate-200 rounded w-1/2" />
                  <div className="h-3 bg-slate-200 rounded w-1/3" />
                </div>
              </div>
              <div className="h-16 bg-slate-100 rounded-xl" />
              <div className="h-8 bg-slate-200 rounded w-1/4" />
            </div>
          ))}
        </div>
      ) : recommendations.length === 0 ? (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center space-y-3">
          <div className="w-12 h-12 rounded-full bg-brand-50 text-brand-600 flex items-center justify-center mx-auto">
            <Filter className="w-6 h-6" />
          </div>
          <h3 className="text-base font-bold text-slate-900">No Alumni Match Current Filters</h3>
          <p className="text-xs text-slate-500 max-w-sm mx-auto">
            Try broadening your industry or skill search parameters to see more verified alumni connections.
          </p>
          <button
            onClick={() => { setIndustry(''); setSkill(''); setJobRole(''); setLocation(''); setMentorshipOnly(false); }}
            className="mt-2 px-4 py-2 rounded-xl text-xs font-bold bg-brand-50 text-brand-700 hover:bg-brand-100 transition-colors"
          >
            Clear All Filters
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {recommendations.map((rec) => (
            <RecommendationCard
              key={rec.profile.user_id}
              recommendation={rec}
              onConnect={(r) => setConnectTarget({ profile: r.profile, starter: r.conversation_starter })}
              onRequestMentorship={(r) => setMentorTarget(r.profile)}
            />
          ))}
        </div>
      )}

      {/* AI Weights Configuration Modal */}
      {showWeightModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-elevated border border-slate-200">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-4">
              <div>
                <h3 className="text-base font-bold text-slate-900 flex items-center gap-1.5">
                  <SlidersHorizontal className="w-4 h-4 text-brand-600" />
                  Configure AI Matching Weights
                </h3>
                <p className="text-xs text-slate-500">Tune the 7 factors to see how recommendation ranking adapts</p>
              </div>
              <button
                onClick={() => setShowWeightModal(false)}
                className="text-slate-400 hover:text-slate-600 text-xs font-bold"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleSaveWeights} className="space-y-3.5 text-xs">
              <div>
                <div className="flex justify-between font-semibold text-slate-700 mb-1">
                  <span>Career Goal Alignment</span>
                  <span>{Math.round(weights.career_weight * 100)}%</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="0.5"
                  step="0.05"
                  value={weights.career_weight}
                  onChange={(e) => setWeights({ ...weights, career_weight: parseFloat(e.target.value) })}
                  className="w-full accent-brand-600"
                />
              </div>

              <div>
                <div className="flex justify-between font-semibold text-slate-700 mb-1">
                  <span>Skill Similarity Overlap</span>
                  <span>{Math.round(weights.skill_weight * 100)}%</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="0.5"
                  step="0.05"
                  value={weights.skill_weight}
                  onChange={(e) => setWeights({ ...weights, skill_weight: parseFloat(e.target.value) })}
                  className="w-full accent-brand-600"
                />
              </div>

              <div>
                <div className="flex justify-between font-semibold text-slate-700 mb-1">
                  <span>Industry Alignment</span>
                  <span>{Math.round(weights.industry_weight * 100)}%</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="0.5"
                  step="0.05"
                  value={weights.industry_weight}
                  onChange={(e) => setWeights({ ...weights, industry_weight: parseFloat(e.target.value) })}
                  className="w-full accent-brand-600"
                />
              </div>

              <div>
                <div className="flex justify-between font-semibold text-slate-700 mb-1">
                  <span>Semantic Vector Profile Similarity</span>
                  <span>{Math.round(weights.semantic_weight * 100)}%</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="0.5"
                  step="0.05"
                  value={weights.semantic_weight}
                  onChange={(e) => setWeights({ ...weights, semantic_weight: parseFloat(e.target.value) })}
                  className="w-full accent-brand-600"
                />
              </div>

              <div>
                <div className="flex justify-between font-semibold text-slate-700 mb-1">
                  <span>Academic Department Alignment</span>
                  <span>{Math.round(weights.academic_weight * 100)}%</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="0.3"
                  step="0.05"
                  value={weights.academic_weight}
                  onChange={(e) => setWeights({ ...weights, academic_weight: parseFloat(e.target.value) })}
                  className="w-full accent-brand-600"
                />
              </div>

              <div className="flex items-center justify-end gap-2 pt-4 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowWeightModal(false)}
                  className="px-4 py-2 font-semibold text-slate-600 hover:bg-slate-100 rounded-xl"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 font-bold text-white bg-brand-600 hover:bg-brand-700 rounded-xl shadow-sm"
                >
                  Apply & Recalculate
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modals for Connect & Mentorship */}
      <ConnectModal
        isOpen={!!connectTarget}
        target={connectTarget}
        onClose={() => setConnectTarget(null)}
        onSuccess={fetchRecommendations}
      />

      <MentorshipModal
        isOpen={!!mentorTarget}
        mentor={mentorTarget}
        onClose={() => setMentorTarget(null)}
        onSuccess={fetchRecommendations}
      />

    </div>
  );
};
