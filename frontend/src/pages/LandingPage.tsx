import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Sparkles, GraduationCap, Users, Briefcase, Award, 
  ArrowRight, CheckCircle2, ShieldCheck, Zap, TrendingUp, 
  ChevronRight, Star, Compass, Play
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const LandingPage: React.FC = () => {
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleQuickDemoLogin = async (role: 'student' | 'alumni' | 'admin') => {
    const email = role === 'student' ? 'student@alumnia.edu' : role === 'alumni' ? 'deepa.subramanian@alumni.edu' : 'admin@alumnia.edu';
    await login({ email, password: 'Password123!' });
    navigate(role === 'admin' ? '/admin' : '/dashboard');
  };

  return (
    <div className="space-y-24 py-6">
      
      {/* 1. Hero Section */}
      <section className="relative overflow-hidden pt-8 pb-16 text-center max-w-5xl mx-auto px-4">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-brand-50 border border-brand-200 text-brand-700 text-xs font-semibold mb-6 shadow-sm">
          <Sparkles className="w-4 h-4 text-brand-600 animate-pulse" />
          Generative AI Based Alumni Networking Platform
        </div>

        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-slate-900 tracking-tight leading-[1.15]">
          Your Next Opportunity Starts With a{' '}
          <span className="bg-gradient-to-r from-brand-600 via-indigo-600 to-violet-600 bg-clip-text text-transparent">
            Connection.
          </span>
        </h1>

        <p className="mt-6 text-base sm:text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed">
          Meet the right alumni, find experienced mentors, and discover career opportunities through personalized AI-powered networking. Built for students and graduates to bridge the college-to-career leap.
        </p>

        {/* Hero CTAs */}
        <div className="mt-8 flex flex-wrap items-center justify-center gap-4">
          <Link
            to="/register"
            className="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-bold text-sm shadow-premium hover:shadow-elevated transition-all"
          >
            Get Started Free
            <ArrowRight className="w-4 h-4" />
          </Link>
          <Link
            to="/login"
            className="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl bg-white hover:bg-slate-50 text-slate-700 font-bold text-sm border border-slate-200 shadow-subtle transition-all"
          >
            Sign In to Platform
          </Link>
        </div>

        {/* Quick Demo Role Launchers */}
        <div className="mt-10 p-4 rounded-2xl bg-white border border-slate-200/90 shadow-subtle max-w-xl mx-auto">
          <p className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">
            Instant Demo Access (Click to Test Drive)
          </p>
          <div className="grid grid-cols-3 gap-2.5">
            <button
              onClick={() => handleQuickDemoLogin('student')}
              className="p-2.5 rounded-xl bg-brand-50 hover:bg-brand-100 text-brand-800 text-xs font-bold border border-brand-200/80 transition-all flex flex-col items-center gap-1"
            >
              <GraduationCap className="w-4 h-4 text-brand-600" />
              <span>Student Persona</span>
            </button>
            <button
              onClick={() => handleQuickDemoLogin('alumni')}
              className="p-2.5 rounded-xl bg-indigo-50 hover:bg-indigo-100 text-indigo-800 text-xs font-bold border border-indigo-200/80 transition-all flex flex-col items-center gap-1"
            >
              <Award className="w-4 h-4 text-indigo-600" />
              <span>Alumni Mentor</span>
            </button>
            <button
              onClick={() => handleQuickDemoLogin('admin')}
              className="p-2.5 rounded-xl bg-amber-50 hover:bg-amber-100 text-amber-800 text-xs font-bold border border-amber-200/80 transition-all flex flex-col items-center gap-1"
            >
              <ShieldCheck className="w-4 h-4 text-amber-600" />
              <span>Administrator</span>
            </button>
          </div>
        </div>

        {/* Interactive Dashboard Sneak-Peek */}
        <div className="mt-12 rounded-2xl border border-slate-200/80 bg-white p-3 shadow-elevated overflow-hidden text-left">
          <div className="flex items-center gap-2 px-3 py-2 bg-slate-100/80 rounded-xl mb-3 text-xs text-slate-500 font-mono">
            <span className="w-3 h-3 rounded-full bg-rose-400 inline-block" />
            <span className="w-3 h-3 rounded-full bg-amber-400 inline-block" />
            <span className="w-3 h-3 rounded-full bg-emerald-400 inline-block" />
            <span className="ml-2 font-medium">alumnia.edu/dashboard — Live Recommendation Feed</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 p-2">
            
            {/* Feature preview card 1 */}
            <div className="p-4 rounded-xl border border-brand-100 bg-brand-50/40 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-brand-600 text-white">96% AI MATCH</span>
                <Sparkles className="w-4 h-4 text-brand-600" />
              </div>
              <h4 className="text-xs font-bold text-slate-900">Deepa Subramanian • Google</h4>
              <p className="text-[11px] text-slate-600">Senior ML Engineer • Alumna '21</p>
              <p className="text-[11px] text-brand-900 bg-white p-2 rounded-lg border border-brand-100">
                "Recommended because your target role in AI aligns with her deep learning work at Google Core Search."
              </p>
            </div>

            {/* Feature preview card 2 */}
            <div className="p-4 rounded-xl border border-indigo-100 bg-indigo-50/40 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-indigo-600 text-white">92% AI MATCH</span>
                <Award className="w-4 h-4 text-indigo-600" />
              </div>
              <h4 className="text-xs font-bold text-slate-900">Vignesh Balasubramanian • Stripe</h4>
              <p className="text-[11px] text-slate-600">Lead Full-Stack Architect • Alumnus '19</p>
              <p className="text-[11px] text-indigo-900 bg-white p-2 rounded-lg border border-indigo-100">
                "Shares 4 core skills: React, TypeScript, FastAPI, and PostgreSQL with active mentorship slots."
              </p>
            </div>

            {/* Feature preview card 3 */}
            <div className="p-4 rounded-xl border border-slate-200 bg-slate-50 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-slate-800 text-white">AI COPILOT</span>
                <Compass className="w-4 h-4 text-slate-600" />
              </div>
              <h4 className="text-xs font-bold text-slate-900">Networking Assistant</h4>
              <p className="text-[11px] text-slate-600">Generated Tailored Icebreaker</p>
              <p className="text-[11px] text-slate-700 bg-white p-2 rounded-lg border border-slate-200 italic">
                "Drafted 5 personalized questions for your upcoming Microsoft Azure informational interview."
              </p>
            </div>

          </div>
        </div>
      </section>

      {/* 2. Platform Highlights Grid */}
      <section className="max-w-6xl mx-auto px-4">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900">
            Intelligent Networking Engineered for Student Success
          </h2>
          <p className="mt-3 text-sm text-slate-600">
            Traditional alumni directories are static lists. Alumnia uses semantic vector matching and explainable AI to connect you with the alumni who matter most.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          
          <div className="p-6 rounded-2xl bg-white border border-slate-200/90 shadow-subtle hover:shadow-premium transition-all space-y-3">
            <div className="w-12 h-12 rounded-xl bg-brand-50 text-brand-600 flex items-center justify-center font-bold">
              <Sparkles className="w-6 h-6" />
            </div>
            <h3 className="text-base font-bold text-slate-900">Personalized 7-Factor Matching</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Our transparent algorithm evaluates career alignment, skill overlap, industry focus, semantic profile similarity, academic background, location, and mentorship availability.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-white border border-slate-200/90 shadow-subtle hover:shadow-premium transition-all space-y-3">
            <div className="w-12 h-12 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center font-bold">
              <Award className="w-6 h-6" />
            </div>
            <h3 className="text-base font-bold text-slate-900">Structured Mentorship Engine</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Apply for 1-on-1 alumni mentorship with custom learning objectives, session scheduling, Google Meet links, and automated feedback loops.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-white border border-slate-200/90 shadow-subtle hover:shadow-premium transition-all space-y-3">
            <div className="w-12 h-12 rounded-xl bg-violet-50 text-violet-600 flex items-center justify-center font-bold">
              <Compass className="w-6 h-6" />
            </div>
            <h3 className="text-base font-bold text-slate-900">Conversational AI Assistant</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Ask questions naturally like "Which alumni can guide me toward data science?" and receive personalized cold message drafts, interview prep, and bio suggestions.
            </p>
          </div>

        </div>
      </section>

      {/* 3. How It Works Section */}
      <section className="bg-white border-y border-slate-200/80 py-16">
        <div className="max-w-6xl mx-auto px-4">
          <div className="text-center max-w-2xl mx-auto mb-12">
            <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900">
              How Alumnia Operates
            </h2>
            <p className="mt-2 text-sm text-slate-600">
              Four simple steps from enrollment to landing your target career milestone.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="p-5 rounded-xl bg-slate-50 border border-slate-200 text-center space-y-2">
              <span className="w-8 h-8 rounded-full bg-brand-600 text-white font-bold text-xs inline-flex items-center justify-center">1</span>
              <h4 className="text-xs font-bold text-slate-900">Create & Verify</h4>
              <p className="text-[11px] text-slate-500">Sign up as a student or alumni and specify your department, skills, and target roles.</p>
            </div>
            <div className="p-5 rounded-xl bg-slate-50 border border-slate-200 text-center space-y-2">
              <span className="w-8 h-8 rounded-full bg-brand-600 text-white font-bold text-xs inline-flex items-center justify-center">2</span>
              <h4 className="text-xs font-bold text-slate-900">AI Analysis</h4>
              <p className="text-[11px] text-slate-500">Our recommendation engine calculates compatibility scores across 7 normalized dimensions.</p>
            </div>
            <div className="p-5 rounded-xl bg-slate-50 border border-slate-200 text-center space-y-2">
              <span className="w-8 h-8 rounded-full bg-brand-600 text-white font-bold text-xs inline-flex items-center justify-center">3</span>
              <h4 className="text-xs font-bold text-slate-900">Connect & Learn</h4>
              <p className="text-[11px] text-slate-500">Reach out with AI-crafted icebreakers, schedule mentorship calls, or chat in real-time.</p>
            </div>
            <div className="p-5 rounded-xl bg-slate-50 border border-slate-200 text-center space-y-2">
              <span className="w-8 h-8 rounded-full bg-brand-600 text-white font-bold text-xs inline-flex items-center justify-center">4</span>
              <h4 className="text-xs font-bold text-slate-900">Career Pipeline</h4>
              <p className="text-[11px] text-slate-500">Discover exclusive alumni job referrals, summer internships, and university webinars.</p>
            </div>
          </div>
        </div>
      </section>

      {/* 4. Verified Institutional Metrics */}
      <section className="max-w-5xl mx-auto px-4 text-center">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 p-8 rounded-2xl bg-navy-900 text-white shadow-elevated">
          <div>
            <p className="text-3xl font-extrabold text-brand-400">140+</p>
            <p className="text-xs text-slate-300 mt-1">Verified Demonstration Users</p>
          </div>
          <div>
            <p className="text-3xl font-extrabold text-brand-400">20+</p>
            <p className="text-xs text-slate-300 mt-1">Engineering Disciplines</p>
          </div>
          <div>
            <p className="text-3xl font-extrabold text-brand-400">7-Factor</p>
            <p className="text-xs text-slate-300 mt-1">Weighted Matching Algorithm</p>
          </div>
          <div>
            <p className="text-3xl font-extrabold text-brand-400">100%</p>
            <p className="text-xs text-slate-300 mt-1">Explainable AI Scoring</p>
          </div>
        </div>
      </section>

      {/* 5. Footer */}
      <footer className="border-t border-slate-200 pt-8 pb-12 text-center text-xs text-slate-500 space-y-2">
        <p className="font-semibold text-slate-700">
          Alumnia — Generative AI Based Alumni Networking Platform with Personalized Connection Recommendations
        </p>
        <p>College Final-Year Project Demonstration Platform • Developed with React, TypeScript & Python FastAPI</p>
      </footer>

    </div>
  );
};
