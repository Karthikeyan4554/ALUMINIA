import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Sparkles, CheckCircle2, ArrowRight, ArrowLeft, 
  Briefcase, Award, Plus, X, User, Target 
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { api } from '../services/api';
import { ENGINEERING_INDUSTRIES } from '../constants/engineeringData';

export const OnboardingPage: React.FC = () => {
  const { profile, refreshProfile } = useAuth();
  const navigate = useNavigate();

  const [step, setStep] = useState(1);
  const [headline, setHeadline] = useState(profile?.headline || '');
  const [bio, setBio] = useState(profile?.bio || '');
  const [skillInput, setSkillInput] = useState('');
  const [skills, setSkills] = useState<string[]>(profile?.skills || ['Python', 'React', 'Machine Learning']);
  
  // Student fields
  const [targetRoleInput, setTargetRoleInput] = useState('');
  const [targetRoles, setTargetRoles] = useState<string[]>(profile?.target_roles || ['Software Engineer', 'Machine Learning Engineer']);
  const [preferredIndustry, setPreferredIndustry] = useState('Artificial Intelligence');
  const [mentorshipGoals, setMentorshipGoals] = useState(profile?.mentorship_goals || 'Prepare for technical interviews and explore career growth.');

  // Alumni fields
  const [currentCompany, setCurrentCompany] = useState(profile?.current_company || 'Tech Corp');
  const [currentJobTitle, setCurrentJobTitle] = useState(profile?.current_job_title || 'Software Engineer');
  const [industry, setIndustry] = useState(profile?.industry || 'Software & Cloud');
  const [mentorshipAvailable, setMentorshipAvailable] = useState(true);

  const [isLoading, setIsLoading] = useState(false);

  const isStudent = profile?.role === 'student';

  const addSkill = () => {
    if (skillInput.trim() && !skills.includes(skillInput.trim())) {
      setSkills([...skills, skillInput.trim()]);
      setSkillInput('');
    }
  };

  const removeSkill = (s: string) => {
    setSkills(skills.filter(x => x !== s));
  };

  const addTargetRole = () => {
    if (targetRoleInput.trim() && !targetRoles.includes(targetRoleInput.trim())) {
      setTargetRoles([...targetRoles, targetRoleInput.trim()]);
      setTargetRoleInput('');
    }
  };

  const removeTargetRole = (r: string) => {
    setTargetRoles(targetRoles.filter(x => x !== r));
  };

  const handleFinish = async () => {
    setIsLoading(true);
    try {
      const payload: any = {
        headline,
        bio,
        skills,
      };

      if (isStudent) {
        payload.target_roles = targetRoles;
        payload.preferred_industries = [preferredIndustry];
        payload.mentorship_goals = mentorshipGoals;
      } else {
        payload.current_company = currentCompany;
        payload.current_job_title = currentJobTitle;
        payload.industry = industry;
        payload.mentorship_available = mentorshipAvailable;
      }

      await api.updateMyProfile(payload);
      await refreshProfile();
      navigate('/dashboard');
    } catch (err) {
      console.error('Failed to complete onboarding', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto py-10 px-4">
      <div className="bg-white rounded-2xl border border-slate-200/90 p-8 shadow-elevated">
        
        {/* Progress Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
            <span>Step {step} of 3</span>
            <span className="text-brand-600">{Math.round((step / 3) * 100)}% Completed</span>
          </div>
          <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
            <div
              className="h-full bg-brand-600 transition-all duration-300 rounded-full"
              style={{ width: `${(step / 3) * 100}%` }}
            />
          </div>
        </div>

        {/* Step 1: Headline & Bio */}
        {step === 1 && (
          <div className="space-y-5 animate-fade-in">
            <div>
              <h2 className="text-xl font-extrabold text-slate-900">Professional Introduction</h2>
              <p className="text-xs text-slate-500 mt-1">
                Tell your university network about your academic journey and aspirations.
              </p>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Headline / Current Status *
              </label>
              <input
                type="text"
                value={headline}
                onChange={(e) => setHeadline(e.target.value)}
                placeholder={isStudent ? "Final-Year CS Student | Aspiring Machine Learning Engineer" : "Senior Software Architect at Stripe"}
                className="w-full text-xs p-3 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/30 focus:border-brand-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Brief Professional Bio *
              </label>
              <textarea
                rows={4}
                value={bio}
                onChange={(e) => setBio(e.target.value)}
                placeholder="Share your focus areas, projects, and what you hope to achieve through networking..."
                className="w-full text-xs p-3 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/30 focus:border-brand-500 resize-none"
              />
            </div>
          </div>
        )}

        {/* Step 2: Skills */}
        {step === 2 && (
          <div className="space-y-5 animate-fade-in">
            <div>
              <h2 className="text-xl font-extrabold text-slate-900">Your Technical & Professional Skills</h2>
              <p className="text-xs text-slate-500 mt-1">
                Our recommendation engine uses these to calculate semantic and skill overlap compatibility.
              </p>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Add Skills (e.g. Python, React, Cloud, Finance)
              </label>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={skillInput}
                  onChange={(e) => setSkillInput(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), addSkill())}
                  placeholder="Type a skill and press Enter"
                  className="flex-1 text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/30 focus:border-brand-500"
                />
                <button
                  type="button"
                  onClick={addSkill}
                  className="px-4 py-2.5 bg-slate-900 text-white rounded-xl text-xs font-semibold hover:bg-slate-800 transition-colors"
                >
                  <Plus className="w-4 h-4" />
                </button>
              </div>

              <div className="flex flex-wrap gap-2 mt-3">
                {skills.map((s) => (
                  <span
                    key={s}
                    className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg bg-brand-50 text-brand-700 border border-brand-200 text-xs font-medium"
                  >
                    {s}
                    <button type="button" onClick={() => removeSkill(s)} className="hover:text-rose-600">
                      <X className="w-3.5 h-3.5" />
                    </button>
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Step 3: Career Goals or Mentorship Settings */}
        {step === 3 && (
          <div className="space-y-5 animate-fade-in">
            <div>
              <h2 className="text-xl font-extrabold text-slate-900">
                {isStudent ? 'Career Objectives & Mentorship' : 'Current Experience & Availability'}
              </h2>
              <p className="text-xs text-slate-500 mt-1">
                {isStudent ? 'Define target job roles so AI can match you with relevant alumni.' : 'Indicate your willingness to mentor graduating students.'}
              </p>
            </div>

            {isStudent ? (
              <>
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">
                    Target Job Roles
                  </label>
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={targetRoleInput}
                      onChange={(e) => setTargetRoleInput(e.target.value)}
                      onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), addTargetRole())}
                      placeholder="e.g. Machine Learning Engineer"
                      className="flex-1 text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/30 focus:border-brand-500"
                    />
                    <button
                      type="button"
                      onClick={addTargetRole}
                      className="px-4 py-2.5 bg-slate-900 text-white rounded-xl text-xs font-semibold hover:bg-slate-800 transition-colors"
                    >
                      <Plus className="w-4 h-4" />
                    </button>
                  </div>
                  <div className="flex flex-wrap gap-2 mt-2">
                    {targetRoles.map((r) => (
                      <span key={r} className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg bg-indigo-50 text-indigo-700 border border-indigo-200 text-xs font-medium">
                        {r}
                        <button type="button" onClick={() => removeTargetRole(r)} className="hover:text-rose-600">
                          <X className="w-3.5 h-3.5" />
                        </button>
                      </span>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">
                    Preferred Industry
                  </label>
                  <select
                    value={preferredIndustry}
                    onChange={(e) => setPreferredIndustry(e.target.value)}
                    className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/30 focus:border-brand-500 bg-white"
                  >
                    {ENGINEERING_INDUSTRIES.map((ind) => (
                      <option key={ind} value={ind}>{ind}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">
                    Mentorship Goals
                  </label>
                  <textarea
                    rows={3}
                    value={mentorshipGoals}
                    onChange={(e) => setMentorshipGoals(e.target.value)}
                    className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/30 focus:border-brand-500 resize-none"
                  />
                </div>
              </>
            ) : (
              <>
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Current Company</label>
                    <input
                      type="text"
                      value={currentCompany}
                      onChange={(e) => setCurrentCompany(e.target.value)}
                      className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/30 focus:border-brand-500"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Job Title</label>
                    <input
                      type="text"
                      value={currentJobTitle}
                      onChange={(e) => setCurrentJobTitle(e.target.value)}
                      className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/30 focus:border-brand-500"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Industry Domain</label>
                  <select
                    value={industry}
                    onChange={(e) => setIndustry(e.target.value)}
                    className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/30 focus:border-brand-500 bg-white"
                  >
                    {ENGINEERING_INDUSTRIES.map((ind) => (
                      <option key={ind} value={ind}>{ind}</option>
                    ))}
                  </select>
                </div>

                <div className="p-4 rounded-xl bg-amber-50/60 border border-amber-200 flex items-center justify-between">
                  <div>
                    <p className="text-xs font-bold text-amber-900">Accept Mentorship Guidance</p>
                    <p className="text-[11px] text-amber-700">Display open mentor badge to matching students</p>
                  </div>
                  <input
                    type="checkbox"
                    checked={mentorshipAvailable}
                    onChange={(e) => setMentorshipAvailable(e.target.checked)}
                    className="w-4 h-4 text-amber-600 rounded"
                  />
                </div>
              </>
            )}
          </div>
        )}

        {/* Navigation Step Buttons */}
        <div className="flex items-center justify-between mt-8 pt-6 border-t border-slate-100">
          {step > 1 ? (
            <button
              type="button"
              onClick={() => setStep(step - 1)}
              className="px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded-xl transition-colors flex items-center gap-1.5"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              Previous
            </button>
          ) : <div />}

          {step < 3 ? (
            <button
              type="button"
              onClick={() => setStep(step + 1)}
              className="px-5 py-2.5 text-xs font-bold text-white bg-brand-600 hover:bg-brand-700 rounded-xl shadow-sm transition-all flex items-center gap-1.5"
            >
              Next Step
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          ) : (
            <button
              type="button"
              disabled={isLoading}
              onClick={handleFinish}
              className="px-6 py-2.5 text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 rounded-xl shadow-sm transition-all flex items-center gap-1.5 disabled:opacity-60"
            >
              <CheckCircle2 className="w-4 h-4" />
              {isLoading ? 'Saving Profile...' : 'Complete & Open Dashboard'}
            </button>
          )}
        </div>

      </div>
    </div>
  );
};
