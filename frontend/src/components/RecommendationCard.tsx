import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { 
  Sparkles, MessageSquare, UserPlus, Award, Building, 
  MapPin, GraduationCap, ThumbsUp, ThumbsDown, Info, 
  ChevronRight, CheckCircle2, Copy, Check 
} from 'lucide-react';
import { Recommendation } from '../types';
import { api } from '../services/api';
import { Avatar } from './Avatar';

interface RecommendationCardProps {
  recommendation: Recommendation;
  onConnect: (rec: Recommendation) => void;
  onRequestMentorship: (rec: Recommendation) => void;
}

export const RecommendationCard: React.FC<RecommendationCardProps> = ({
  recommendation,
  onConnect,
  onRequestMentorship,
}) => {
  const { profile, score, match_percentage, breakdown, explanation, conversation_starter, shared_skills, mutual_attributes } = recommendation;
  const [showBreakdown, setShowBreakdown] = useState(false);
  const [feedback, setFeedback] = useState<'relevant' | 'not_relevant' | null>(null);
  const [copiedStarter, setCopiedStarter] = useState(false);

  const handleFeedback = async (isRelevant: boolean) => {
    try {
      setFeedback(isRelevant ? 'relevant' : 'not_relevant');
      await api.submitRecommendationFeedback({
        alumni_id: profile.user_id,
        score,
        is_relevant: isRelevant,
        feedback_notes: isRelevant ? 'User confirmed relevant match' : 'User flagged irrelevant match',
      });
    } catch (err) {
      console.error('Feedback submission failed', err);
    }
  };

  const copyStarter = () => {
    navigator.clipboard.writeText(conversation_starter);
    setCopiedStarter(true);
    setTimeout(() => setCopiedStarter(false), 2000);
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200/90 shadow-subtle hover:shadow-premium transition-all duration-300 overflow-hidden flex flex-col justify-between">
      
      {/* Top Banner & Match Score */}
      <div>
        <div className="p-5 pb-0 flex items-start justify-between gap-4">
          <div className="flex items-start gap-3.5">
            <Link to={`/profile/${profile.user_id}`}>
              <Avatar name={profile.full_name} size="lg" className="rounded-2xl" />
            </Link>
            <div>
              <Link to={`/profile/${profile.user_id}`} className="hover:text-brand-600 transition-colors">
                <h3 className="font-bold text-slate-900 text-base flex items-center gap-1.5">
                  {profile.full_name}
                  {profile.mentorship_available && (
                    <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] font-bold bg-amber-50 text-amber-700 border border-amber-200">
                      <Award className="w-3 h-3 text-amber-600" /> Mentor
                    </span>
                  )}
                </h3>
              </Link>
              <p className="text-xs font-semibold text-brand-700 flex items-center gap-1 mt-0.5">
                <Building className="w-3.5 h-3.5 text-slate-400" />
                {profile.current_job_title || 'Engineer'} at {profile.current_company || 'Tech Company'}
              </p>
              <div className="flex items-center gap-2 mt-1 text-[11px] text-slate-500">
                <span className="flex items-center gap-1">
                  <GraduationCap className="w-3 h-3" /> Class of {profile.graduation_year || 2021}
                </span>
                <span>•</span>
                <span className="flex items-center gap-1">
                  <MapPin className="w-3 h-3" /> {profile.location || 'Remote'}
                </span>
              </div>
            </div>
          </div>

          {/* AI Match Score Badge */}
          <div className="flex flex-col items-end">
            <div className="flex items-center gap-1 px-2.5 py-1 rounded-xl bg-gradient-to-r from-brand-600 to-indigo-600 text-white shadow-sm">
              <Sparkles className="w-3.5 h-3.5" />
              <span className="text-xs font-extrabold tracking-tight">{match_percentage}%</span>
            </div>
            <button
              onClick={() => setShowBreakdown(!showBreakdown)}
              className="mt-1 text-[10px] font-medium text-slate-400 hover:text-brand-600 flex items-center gap-0.5"
            >
              <Info className="w-3 h-3" /> Breakdown
            </button>
          </div>
        </div>

        {/* Score Breakdown Popover */}
        {showBreakdown && (
          <div className="mx-5 mt-3 p-3.5 bg-slate-50 border border-slate-200/90 rounded-xl text-xs space-y-2 animate-fade-in shadow-inner">
            <div className="flex justify-between items-center font-bold text-slate-800 border-b border-slate-200 pb-1.5">
              <span>7-Factor Compatibility Breakdown</span>
              <span className="text-brand-600 font-extrabold">{match_percentage}% Score</span>
            </div>
            
            <div>
              <div className="flex justify-between text-[11px] text-slate-600 mb-0.5">
                <span>Career Goal Alignment (25%)</span>
                <span className="font-bold text-slate-900">{breakdown.career_alignment}%</span>
              </div>
              <div className="w-full h-1.5 bg-slate-200 rounded-full overflow-hidden">
                <div className="h-full bg-brand-600 rounded-full" style={{ width: `${breakdown.career_alignment}%` }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-[11px] text-slate-600 mb-0.5">
                <span>Skill Overlap Similarity (20%)</span>
                <span className="font-bold text-slate-900">{breakdown.skill_similarity}%</span>
              </div>
              <div className="w-full h-1.5 bg-slate-200 rounded-full overflow-hidden">
                <div className="h-full bg-indigo-600 rounded-full" style={{ width: `${breakdown.skill_similarity}%` }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-[11px] text-slate-600 mb-0.5">
                <span>Industry Alignment (20%)</span>
                <span className="font-bold text-slate-900">{breakdown.industry_alignment}%</span>
              </div>
              <div className="w-full h-1.5 bg-slate-200 rounded-full overflow-hidden">
                <div className="h-full bg-emerald-600 rounded-full" style={{ width: `${breakdown.industry_alignment}%` }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-[11px] text-slate-600 mb-0.5">
                <span>Semantic Profile Cosine (15%)</span>
                <span className="font-bold text-slate-900">{breakdown.semantic_similarity}%</span>
              </div>
              <div className="w-full h-1.5 bg-slate-200 rounded-full overflow-hidden">
                <div className="h-full bg-violet-600 rounded-full" style={{ width: `${breakdown.semantic_similarity}%` }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-[11px] text-slate-600 mb-0.5">
                <span>Academic Department Alignment (10%)</span>
                <span className="font-bold text-slate-900">{breakdown.academic_alignment}%</span>
              </div>
              <div className="w-full h-1.5 bg-slate-200 rounded-full overflow-hidden">
                <div className="h-full bg-amber-600 rounded-full" style={{ width: `${breakdown.academic_alignment}%` }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-[11px] text-slate-600 mb-0.5">
                <span>Geographic Location (5%)</span>
                <span className="font-bold text-slate-900">{breakdown.location_match}%</span>
              </div>
              <div className="w-full h-1.5 bg-slate-200 rounded-full overflow-hidden">
                <div className="h-full bg-cyan-600 rounded-full" style={{ width: `${breakdown.location_match}%` }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-[11px] text-slate-600 mb-0.5">
                <span>Mentorship Availability Bonus (5%)</span>
                <span className="font-bold text-slate-900">{breakdown.mentorship_bonus}%</span>
              </div>
              <div className="w-full h-1.5 bg-slate-200 rounded-full overflow-hidden">
                <div className="h-full bg-rose-600 rounded-full" style={{ width: `${breakdown.mentorship_bonus}%` }} />
              </div>
            </div>
          </div>
        )}

        {/* AI Explanation Callout */}
        <div className="mx-5 mt-4 p-3 rounded-xl bg-brand-50/70 border border-brand-100 text-xs text-brand-950 flex items-start gap-2.5">
          <Sparkles className="w-4 h-4 text-brand-600 mt-0.5 flex-shrink-0" />
          <div className="flex-1">
            <span className="font-bold text-brand-800 mr-1">Why this connection:</span>
            <span className="text-slate-700 leading-relaxed">{explanation}</span>
          </div>
        </div>

        {/* Mutual Attributes & Shared Skills */}
        <div className="px-5 mt-3 space-y-2">
          {shared_skills.length > 0 && (
            <div className="flex items-center gap-1.5 flex-wrap">
              <span className="text-[11px] font-semibold text-slate-400">Shared Skills:</span>
              {shared_skills.map((skill) => (
                <span
                  key={skill}
                  className="px-2 py-0.5 text-[11px] font-medium rounded-md bg-emerald-50 text-emerald-700 border border-emerald-200"
                >
                  ✓ {skill}
                </span>
              ))}
            </div>
          )}

          {mutual_attributes.length > 0 && (
            <div className="flex items-center gap-1.5 flex-wrap">
              {mutual_attributes.map((attr) => (
                <span
                  key={attr}
                  className="px-2 py-0.5 text-[10px] font-semibold rounded-full bg-slate-100 text-slate-600 border border-slate-200"
                >
                  {attr}
                </span>
              ))}
            </div>
          )}
        </div>

        {/* AI Suggested Conversation Starter */}
        <div className="mx-5 mt-3 p-3 rounded-xl bg-slate-50 border border-slate-200 text-xs">
          <div className="flex items-center justify-between mb-1">
            <span className="text-[11px] font-bold text-slate-600 uppercase tracking-wider flex items-center gap-1">
              <MessageSquare className="w-3 h-3 text-brand-600" />
              Suggested Icebreaker
            </span>
            <button
              onClick={copyStarter}
              className="text-[11px] font-semibold text-brand-600 hover:text-brand-700 flex items-center gap-1"
            >
              {copiedStarter ? <Check className="w-3 h-3 text-emerald-600" /> : <Copy className="w-3 h-3" />}
              {copiedStarter ? 'Copied' : 'Copy'}
            </button>
          </div>
          <p className="text-slate-600 italic text-[11px] leading-relaxed">
            "{conversation_starter}"
          </p>
        </div>
      </div>

      {/* Card Actions & Relevance Feedback */}
      <div className="p-5 pt-4 mt-3 border-t border-slate-100 bg-slate-50/50 flex flex-col sm:flex-row items-center justify-between gap-3">
        {/* Feedback Buttons */}
        <div className="flex items-center gap-1.5 text-xs text-slate-500 w-full sm:w-auto">
          <span className="text-[11px]">Match accurate?</span>
          <button
            onClick={() => handleFeedback(true)}
            className={`p-1.5 rounded-lg border transition-colors ${
              feedback === 'relevant'
                ? 'bg-emerald-50 border-emerald-300 text-emerald-700'
                : 'border-slate-200 text-slate-500 hover:bg-slate-100'
            }`}
            title="Relevant Recommendation"
          >
            <ThumbsUp className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={() => handleFeedback(false)}
            className={`p-1.5 rounded-lg border transition-colors ${
              feedback === 'not_relevant'
                ? 'bg-rose-50 border-rose-300 text-rose-700'
                : 'border-slate-200 text-slate-500 hover:bg-slate-100'
            }`}
            title="Not Relevant"
          >
            <ThumbsDown className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Primary CTA Buttons */}
        <div className="flex items-center gap-2 w-full sm:w-auto justify-end">
          <Link
            to={`/profile/${profile.user_id}`}
            className="px-3 py-1.5 text-xs font-semibold rounded-lg border border-slate-200 bg-white text-slate-700 hover:bg-slate-50 transition-colors"
          >
            Profile
          </Link>

          {profile.mentorship_available && (
            <button
              onClick={() => onRequestMentorship(recommendation)}
              className="px-3 py-1.5 text-xs font-semibold rounded-lg bg-amber-50 text-amber-800 border border-amber-200 hover:bg-amber-100 transition-colors flex items-center gap-1"
            >
              <Award className="w-3.5 h-3.5" />
              Mentorship
            </button>
          )}

          <button
            onClick={() => onConnect(recommendation)}
            disabled={profile.connection_status === 'connected' || profile.connection_status === 'pending_sent'}
            className={`px-3 py-1.5 text-xs font-semibold rounded-lg flex items-center gap-1 shadow-sm transition-all ${
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
              ? 'Request Sent'
              : 'Connect'}
          </button>
        </div>
      </div>

    </div>
  );
};
