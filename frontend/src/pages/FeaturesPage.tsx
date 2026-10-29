import React from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, Brain, Award, Briefcase, Calendar, MessageSquare, Shield, Users } from 'lucide-react';

export const FeaturesPage: React.FC = () => {
  return (
    <div className="max-w-5xl mx-auto py-10 px-4 space-y-12">
      <div className="text-center max-w-2xl mx-auto">
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900">
          Platform Architecture & Features
        </h1>
        <p className="mt-3 text-sm text-slate-600">
          Discover how generative AI, semantic vector retrieval, and structured mentorship pipelines power Alumnia.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        
        {/* Feature 1 */}
        <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-subtle space-y-3">
          <div className="w-10 h-10 rounded-xl bg-brand-50 text-brand-600 flex items-center justify-center">
            <Sparkles className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-slate-900">AI-Powered 7-Factor Recommendation Engine</h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            Eliminates cold searching through algorithmic scoring: Career Alignment (25%), Skill Similarity (20%), Industry Alignment (20%), Semantic Profile Cosine Similarity (15%), Academic Background (10%), Location Match (5%), and Mentorship Bonus (5%).
          </p>
        </div>

        {/* Feature 2 */}
        <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-subtle space-y-3">
          <div className="w-10 h-10 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center">
            <Brain className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-slate-900">Conversational AI Networking Assistant</h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            An intelligent advisor that analyzes authorized alumni profiles to answer career inquiries, draft respectful cold connection notes, formulate mock interview questions, and suggest profile refinements.
          </p>
        </div>

        {/* Feature 3 */}
        <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-subtle space-y-3">
          <div className="w-10 h-10 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center">
            <Award className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-slate-900">Structured Mentorship Module</h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            Students apply with structured learning goals and desired meeting frequencies. Mentors can accept, decline, or schedule 45-minute sessions complete with Google Meet links and session agendas.
          </p>
        </div>

        {/* Feature 4 */}
        <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-subtle space-y-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
            <Briefcase className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-slate-900">Verified Alumni Opportunity Board</h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            Alumni post direct career openings and internships at leading companies like Google, Stripe, Microsoft, and Goldman Sachs. Students can filter by skills, save opportunities, and submit in-app applications.
          </p>
        </div>

        {/* Feature 5 */}
        <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-subtle space-y-3">
          <div className="w-10 h-10 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center">
            <Calendar className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-slate-900">Alumni Events & Technical Webinars</h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            Interactive virtual webinars, mock system design bootcamps, and on-campus mentorship galas with capacity tracking, duplicate registration prevention, and calendar reminders.
          </p>
        </div>

        {/* Feature 6 */}
        <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-subtle space-y-3">
          <div className="w-10 h-10 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center">
            <Shield className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-slate-900">Enterprise Administration & Moderation</h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            Protected admin dashboard featuring institutional KPI analytics, user status controls, moderation queues for content safety reports, and algorithmic weight configuration.
          </p>
        </div>

      </div>

      <div className="text-center pt-6">
        <Link
          to="/register"
          className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-bold text-xs shadow-md transition-all"
        >
          Explore the Platform Now
        </Link>
      </div>
    </div>
  );
};
