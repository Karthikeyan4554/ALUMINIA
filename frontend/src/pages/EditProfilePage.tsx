import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  User, Save, CheckCircle2, AlertCircle, Plus, X, 
  Building, GraduationCap, Award, MapPin, Globe, Lock, 
  Briefcase, FolderGit2, Trash2, Calendar
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import { api } from '../services/api';
import { WorkExperienceItem, EducationItem, ProjectItem } from '../types';
import { ENGINEERING_DEPARTMENTS, ENGINEERING_INDUSTRIES } from '../constants/engineeringData';

export const EditProfilePage: React.FC = () => {
  const { profile, refreshProfile } = useAuth();
  const navigate = useNavigate();
  const toast = useToast();

  const [formData, setFormData] = useState<any>({
    full_name: '',
    headline: '',
    bio: '',
    location: '',
    college_email: '',
    phone: '',
    department: '',
    degree: '',
    graduation_year: new Date().getFullYear(),
    current_company: '',
    current_job_title: '',
    industry: '',
    years_of_experience: 0,
    mentorship_available: false,
    mentorship_capacity: 3,
    mentorship_goals: '',
    github_url: '',
    linkedin_url: '',
    portfolio_url: '',
    hide_contact_info: true,
  });

  const [skills, setSkills] = useState<string[]>([]);
  const [skillInput, setSkillInput] = useState('');
  const [targetRoles, setTargetRoles] = useState<string[]>([]);
  const [targetRoleInput, setTargetRoleInput] = useState('');

  // Experience, Education & Projects
  const [workExperiences, setWorkExperiences] = useState<WorkExperienceItem[]>([]);
  const [educations, setEducations] = useState<EducationItem[]>([]);
  const [projects, setProjects] = useState<ProjectItem[]>([]);

  // Modals / Temporary form states for adding items
  const [showAddExp, setShowAddExp] = useState(false);
  const [newExp, setNewExp] = useState<WorkExperienceItem>({
    title: '',
    company: '',
    location: '',
    start_date: '',
    end_date: '',
    is_current: false,
    description: '',
  });

  const [showAddEdu, setShowAddEdu] = useState(false);
  const [newEdu, setNewEdu] = useState<EducationItem>({
    institution: '',
    degree: '',
    field_of_study: '',
    start_year: new Date().getFullYear() - 4,
    end_year: new Date().getFullYear(),
    grade: '',
  });

  const [showAddProject, setShowAddProject] = useState(false);
  const [newProject, setNewProject] = useState<ProjectItem>({
    title: '',
    description: '',
    technologies: '',
    project_url: '',
  });

  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    if (profile) {
      setFormData({
        full_name: profile.full_name || '',
        headline: profile.headline || '',
        bio: profile.bio || '',
        location: profile.location || '',
        college_email: profile.college_email || '',
        phone: profile.phone || '',
        department: profile.department || 'Computer Science & Engineering',
        degree: profile.degree || 'B.Tech',
        graduation_year: profile.graduation_year || new Date().getFullYear(),
        current_company: profile.current_company || '',
        current_job_title: profile.current_job_title || '',
        industry: profile.industry || 'Software & Cloud',
        years_of_experience: profile.years_of_experience || 0,
        mentorship_available: profile.mentorship_available || false,
        mentorship_capacity: profile.mentorship_capacity || 3,
        mentorship_goals: profile.mentorship_goals || '',
        github_url: profile.github_url || '',
        linkedin_url: profile.linkedin_url || '',
        portfolio_url: profile.portfolio_url || '',
        hide_contact_info: profile.hide_contact_info !== false,
      });
      setSkills(profile.skills || []);
      setTargetRoles(profile.target_roles || []);
      setWorkExperiences(profile.work_experiences || []);
      setEducations(profile.educations || []);
      setProjects(profile.projects || []);
    }
  }, [profile]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    if (type === 'checkbox') {
      const checked = (e.target as HTMLInputElement).checked;
      setFormData((prev: any) => ({ ...prev, [name]: checked }));
    } else {
      setFormData((prev: any) => ({ ...prev, [name]: value }));
    }
  };

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

  const handleAddExperience = () => {
    if (!newExp.title.trim() || !newExp.company.trim() || !newExp.start_date.trim()) {
      toast.error('Please enter title, company, and start date.');
      return;
    }
    setWorkExperiences([...workExperiences, { ...newExp }]);
    setNewExp({
      title: '',
      company: '',
      location: '',
      start_date: '',
      end_date: '',
      is_current: false,
      description: '',
    });
    setShowAddExp(false);
  };

  const handleRemoveExperience = (index: number) => {
    setWorkExperiences(workExperiences.filter((_, i) => i !== index));
  };

  const handleAddEducation = () => {
    if (!newEdu.institution.trim() || !newEdu.degree.trim() || !newEdu.field_of_study.trim()) {
      toast.error('Please enter institution, degree, and field of study.');
      return;
    }
    setEducations([...educations, { ...newEdu }]);
    setNewEdu({
      institution: '',
      degree: '',
      field_of_study: '',
      start_year: new Date().getFullYear() - 4,
      end_year: new Date().getFullYear(),
      grade: '',
    });
    setShowAddEdu(false);
  };

  const handleRemoveEducation = (index: number) => {
    setEducations(educations.filter((_, i) => i !== index));
  };

  const handleAddProject = () => {
    if (!newProject.title.trim()) {
      toast.error('Please enter a project title.');
      return;
    }
    setProjects([...projects, { ...newProject }]);
    setNewProject({
      title: '',
      description: '',
      technologies: '',
      project_url: '',
    });
    setShowAddProject(false);
  };

  const handleRemoveProject = (index: number) => {
    setProjects(projects.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    try {
      await api.updateMyProfile({
        ...formData,
        skills,
        target_roles: targetRoles,
        work_experiences: workExperiences,
        educations,
        projects,
      });
      await refreshProfile();
      toast.success('Profile and career history saved successfully!');
    } catch (err: any) {
      toast.error(err.message || 'Failed to update profile');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-16 animate-fade-in">
      
      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-subtle">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">
            Edit Profile & Preferences
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Keep your credentials, experiences, and networking goals updated to optimize AI recommendations
          </p>
        </div>
        <button
          type="button"
          onClick={() => navigate('/profile/me')}
          className="px-4 py-2 text-xs font-bold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-xl transition-colors"
        >
          View Public Profile
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        
        {/* 1. Basic Info */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-subtle space-y-4">
          <h2 className="text-xs font-bold text-brand-700 uppercase tracking-wider flex items-center gap-1.5">
            <User className="w-4 h-4" />
            Personal & Headline Information
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Full Name</label>
              <input
                type="text"
                name="full_name"
                value={formData.full_name}
                onChange={handleChange}
                required
                className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/20"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Location</label>
              <input
                type="text"
                name="location"
                value={formData.location}
                onChange={handleChange}
                placeholder="e.g. San Francisco, CA"
                className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/20"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Professional Headline</label>
            <input
              type="text"
              name="headline"
              value={formData.headline}
              onChange={handleChange}
              placeholder="e.g. Senior Machine Learning Engineer at Google • Alum '21"
              className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/20"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Biography</label>
            <textarea
              rows={4}
              name="bio"
              value={formData.bio}
              onChange={handleChange}
              placeholder="Tell other students and alumni about your background, passions, and current journey..."
              className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/20 resize-none"
            />
          </div>
        </div>

        {/* 2. Academic Information */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-subtle space-y-4">
          <h2 className="text-xs font-bold text-brand-700 uppercase tracking-wider flex items-center gap-1.5">
            <GraduationCap className="w-4 h-4" />
            Academic Background
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Department</label>
              <input
                type="text"
                name="department"
                list="engineering-departments"
                value={formData.department}
                onChange={handleChange}
                placeholder="Select or enter engineering department"
                className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/20"
              />
              <datalist id="engineering-departments">
                {ENGINEERING_DEPARTMENTS.map((dept) => (
                  <option key={dept} value={dept} />
                ))}
              </datalist>
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Degree</label>
              <input
                type="text"
                name="degree"
                value={formData.degree}
                onChange={handleChange}
                placeholder="B.Tech / M.S. / Ph.D."
                className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/20"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Graduation Year</label>
              <input
                type="number"
                name="graduation_year"
                value={formData.graduation_year}
                onChange={handleChange}
                className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/20"
              />
            </div>
          </div>
        </div>

        {/* 3. Professional Experience & Industry */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-subtle space-y-4">
          <h2 className="text-xs font-bold text-brand-700 uppercase tracking-wider flex items-center gap-1.5">
            <Building className="w-4 h-4" />
            Current Role & Mentorship Availability
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Current Company</label>
              <input
                type="text"
                name="current_company"
                value={formData.current_company}
                onChange={handleChange}
                placeholder="Google / Stripe / University"
                className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/20"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Current Job Title</label>
              <input
                type="text"
                name="current_job_title"
                value={formData.current_job_title}
                onChange={handleChange}
                placeholder="Software Engineer / Student"
                className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/20"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Industry</label>
              <select
                name="industry"
                value={formData.industry}
                onChange={handleChange}
                className="w-full text-xs p-2.5 rounded-xl border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-brand-500/20"
              >
                {ENGINEERING_INDUSTRIES.map((ind) => (
                  <option key={ind} value={ind}>{ind}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Years of Professional Experience</label>
              <input
                type="number"
                name="years_of_experience"
                min="0"
                value={formData.years_of_experience}
                onChange={handleChange}
                className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/20"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Max Mentorship Mentees</label>
              <input
                type="number"
                name="mentorship_capacity"
                min="1"
                max="10"
                value={formData.mentorship_capacity}
                onChange={handleChange}
                className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/20"
              />
            </div>
          </div>

          {/* Mentorship Settings */}
          <div className="p-4 rounded-xl bg-amber-50/70 border border-amber-200 space-y-3">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs font-bold text-amber-950">Active Mentorship Guidance</p>
                <p className="text-[11px] text-amber-700">Display open mentor badge and accept 1-on-1 career mentorship bookings</p>
              </div>
              <input
                type="checkbox"
                name="mentorship_available"
                checked={formData.mentorship_available}
                onChange={handleChange}
                className="w-4 h-4 text-amber-600 rounded"
              />
            </div>
            {formData.mentorship_available && (
              <div>
                <label className="block text-xs font-semibold text-amber-950 mb-1">Mentorship Offering / Goals</label>
                <input
                  type="text"
                  name="mentorship_goals"
                  value={formData.mentorship_goals}
                  onChange={handleChange}
                  placeholder="e.g. Resume reviews, system design mock interviews, career transitions"
                  className="w-full text-xs p-2 rounded-lg border border-amber-200 bg-white focus:outline-none"
                />
              </div>
            )}
          </div>
        </div>

        {/* 4. Skills & Competencies */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-subtle space-y-4">
          <h2 className="text-xs font-bold text-brand-700 uppercase tracking-wider flex items-center gap-1.5">
            <Award className="w-4 h-4" />
            Skills & Competencies
          </h2>
          <div className="flex gap-2">
            <input
              type="text"
              value={skillInput}
              onChange={(e) => setSkillInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), addSkill())}
              placeholder="Add skill (e.g. PyTorch, React, SQL, Distributed Systems)..."
              className="flex-1 text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/20"
            />
            <button
              type="button"
              onClick={addSkill}
              className="px-4 py-2 bg-slate-900 text-white rounded-xl text-xs font-bold hover:bg-slate-800"
            >
              Add
            </button>
          </div>
          <div className="flex flex-wrap gap-2">
            {skills.map((s) => (
              <span key={s} className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg bg-brand-50 text-brand-700 border border-brand-200 text-xs font-medium">
                {s}
                <button type="button" onClick={() => removeSkill(s)} className="hover:text-rose-600">
                  <X className="w-3.5 h-3.5" />
                </button>
              </span>
            ))}
          </div>
        </div>

        {/* 5. Target Job Roles */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-subtle space-y-4">
          <h2 className="text-xs font-bold text-brand-700 uppercase tracking-wider flex items-center gap-1.5">
            <Briefcase className="w-4 h-4" />
            Target Career Roles (Used for AI Matching)
          </h2>
          <div className="flex gap-2">
            <input
              type="text"
              value={targetRoleInput}
              onChange={(e) => setTargetRoleInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), addTargetRole())}
              placeholder="Add target role (e.g. Machine Learning Engineer, Product Manager)..."
              className="flex-1 text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/20"
            />
            <button
              type="button"
              onClick={addTargetRole}
              className="px-4 py-2 bg-slate-900 text-white rounded-xl text-xs font-bold hover:bg-slate-800"
            >
              Add
            </button>
          </div>
          <div className="flex flex-wrap gap-2">
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

        {/* 6. Work Experience History */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-subtle space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xs font-bold text-brand-700 uppercase tracking-wider flex items-center gap-1.5">
                <Briefcase className="w-4 h-4" />
                Work Experiences ({workExperiences.length})
              </h2>
              <p className="text-[11px] text-slate-500">Your professional roles, internships, and research appointments</p>
            </div>
            <button
              type="button"
              onClick={() => setShowAddExp(!showAddExp)}
              className="inline-flex items-center gap-1 text-xs font-bold px-3 py-1.5 rounded-xl bg-brand-50 text-brand-700 hover:bg-brand-100"
            >
              <Plus className="w-3.5 h-3.5" />
              {showAddExp ? 'Cancel' : 'Add Experience'}
            </button>
          </div>

          {/* Add Experience Form */}
          {showAddExp && (
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-3">
              <h3 className="text-xs font-bold text-slate-900">Add Work Experience</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <input
                  type="text"
                  placeholder="Job Title (e.g. Software Engineer Intern)"
                  value={newExp.title}
                  onChange={(e) => setNewExp({ ...newExp, title: e.target.value })}
                  className="text-xs p-2.5 rounded-lg border border-slate-200 bg-white"
                />
                <input
                  type="text"
                  placeholder="Company (e.g. Stripe)"
                  value={newExp.company}
                  onChange={(e) => setNewExp({ ...newExp, company: e.target.value })}
                  className="text-xs p-2.5 rounded-lg border border-slate-200 bg-white"
                />
                <input
                  type="text"
                  placeholder="Location (e.g. Seattle, WA)"
                  value={newExp.location || ''}
                  onChange={(e) => setNewExp({ ...newExp, location: e.target.value })}
                  className="text-xs p-2.5 rounded-lg border border-slate-200 bg-white"
                />
                <div className="grid grid-cols-2 gap-2">
                  <input
                    type="text"
                    placeholder="Start (e.g. 2022-06)"
                    value={newExp.start_date}
                    onChange={(e) => setNewExp({ ...newExp, start_date: e.target.value })}
                    className="text-xs p-2.5 rounded-lg border border-slate-200 bg-white"
                  />
                  <input
                    type="text"
                    placeholder="End (e.g. 2023-08)"
                    disabled={newExp.is_current}
                    value={newExp.end_date || ''}
                    onChange={(e) => setNewExp({ ...newExp, end_date: e.target.value })}
                    className="text-xs p-2.5 rounded-lg border border-slate-200 bg-white disabled:opacity-50"
                  />
                </div>
              </div>
              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  id="is_current"
                  checked={newExp.is_current}
                  onChange={(e) => setNewExp({ ...newExp, is_current: e.target.checked })}
                  className="w-4 h-4 text-brand-600 rounded"
                />
                <label htmlFor="is_current" className="text-xs text-slate-700">Currently working in this role</label>
              </div>
              <textarea
                placeholder="Describe your responsibilities, impact, and technologies used..."
                rows={3}
                value={newExp.description || ''}
                onChange={(e) => setNewExp({ ...newExp, description: e.target.value })}
                className="w-full text-xs p-2.5 rounded-lg border border-slate-200 bg-white resize-none"
              />
              <button
                type="button"
                onClick={handleAddExperience}
                className="px-4 py-2 bg-brand-600 hover:bg-brand-700 text-white rounded-lg text-xs font-bold"
              >
                Save This Experience
              </button>
            </div>
          )}

          {/* List of existing experiences */}
          <div className="space-y-3">
            {workExperiences.length === 0 ? (
              <p className="text-xs text-slate-400 py-2">No work experiences added yet.</p>
            ) : (
              workExperiences.map((exp, idx) => (
                <div key={idx} className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 flex items-start justify-between gap-4">
                  <div className="space-y-1">
                    <p className="text-xs font-bold text-slate-900">{exp.title}</p>
                    <p className="text-xs font-semibold text-brand-700">{exp.company} • {exp.location}</p>
                    <p className="text-[11px] text-slate-500">
                      {exp.start_date} — {exp.is_current ? 'Present' : exp.end_date}
                    </p>
                    {exp.description && <p className="text-xs text-slate-600 pt-1">{exp.description}</p>}
                  </div>
                  <button
                    type="button"
                    onClick={() => handleRemoveExperience(idx)}
                    className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              ))
            )}
          </div>
        </div>

        {/* 7. Education History */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-subtle space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xs font-bold text-brand-700 uppercase tracking-wider flex items-center gap-1.5">
                <GraduationCap className="w-4 h-4" />
                Education History ({educations.length})
              </h2>
              <p className="text-[11px] text-slate-500">Colleges, universities, and degrees completed</p>
            </div>
            <button
              type="button"
              onClick={() => setShowAddEdu(!showAddEdu)}
              className="inline-flex items-center gap-1 text-xs font-bold px-3 py-1.5 rounded-xl bg-brand-50 text-brand-700 hover:bg-brand-100"
            >
              <Plus className="w-3.5 h-3.5" />
              {showAddEdu ? 'Cancel' : 'Add Education'}
            </button>
          </div>

          {/* Add Education Form */}
          {showAddEdu && (
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-3">
              <h3 className="text-xs font-bold text-slate-900">Add Education</h3>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <input
                  type="text"
                  placeholder="Institution (e.g. Stanford University)"
                  value={newEdu.institution}
                  onChange={(e) => setNewEdu({ ...newEdu, institution: e.target.value })}
                  className="text-xs p-2.5 rounded-lg border border-slate-200 bg-white"
                />
                <input
                  type="text"
                  placeholder="Degree (e.g. B.Tech / B.S.)"
                  value={newEdu.degree}
                  onChange={(e) => setNewEdu({ ...newEdu, degree: e.target.value })}
                  className="text-xs p-2.5 rounded-lg border border-slate-200 bg-white"
                />
                <input
                  type="text"
                  placeholder="Field of Study (e.g. Computer Science)"
                  value={newEdu.field_of_study}
                  onChange={(e) => setNewEdu({ ...newEdu, field_of_study: e.target.value })}
                  className="text-xs p-2.5 rounded-lg border border-slate-200 bg-white"
                />
                <input
                  type="number"
                  placeholder="Start Year"
                  value={newEdu.start_year || ''}
                  onChange={(e) => setNewEdu({ ...newEdu, start_year: parseInt(e.target.value) || undefined })}
                  className="text-xs p-2.5 rounded-lg border border-slate-200 bg-white"
                />
                <input
                  type="number"
                  placeholder="End Year"
                  value={newEdu.end_year || ''}
                  onChange={(e) => setNewEdu({ ...newEdu, end_year: parseInt(e.target.value) || undefined })}
                  className="text-xs p-2.5 rounded-lg border border-slate-200 bg-white"
                />
                <input
                  type="text"
                  placeholder="Grade / GPA (optional)"
                  value={newEdu.grade || ''}
                  onChange={(e) => setNewEdu({ ...newEdu, grade: e.target.value })}
                  className="text-xs p-2.5 rounded-lg border border-slate-200 bg-white"
                />
              </div>
              <button
                type="button"
                onClick={handleAddEducation}
                className="px-4 py-2 bg-brand-600 hover:bg-brand-700 text-white rounded-lg text-xs font-bold"
              >
                Save This Education
              </button>
            </div>
          )}

          <div className="space-y-3">
            {educations.length === 0 ? (
              <p className="text-xs text-slate-400 py-2">No education records added yet.</p>
            ) : (
              educations.map((edu, idx) => (
                <div key={idx} className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 flex items-start justify-between gap-4">
                  <div className="space-y-0.5">
                    <p className="text-xs font-bold text-slate-900">{edu.institution}</p>
                    <p className="text-xs text-slate-600">{edu.degree} in {edu.field_of_study}</p>
                    <p className="text-[11px] text-slate-500">
                      {edu.start_year} — {edu.end_year} {edu.grade ? `• ${edu.grade}` : ''}
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={() => handleRemoveEducation(idx)}
                    className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              ))
            )}
          </div>
        </div>

        {/* 8. Portfolio Projects */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-subtle space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xs font-bold text-brand-700 uppercase tracking-wider flex items-center gap-1.5">
                <FolderGit2 className="w-4 h-4" />
                Featured Projects ({projects.length})
              </h2>
              <p className="text-[11px] text-slate-500">Highlight open source repos, systems, research, or apps</p>
            </div>
            <button
              type="button"
              onClick={() => setShowAddProject(!showAddProject)}
              className="inline-flex items-center gap-1 text-xs font-bold px-3 py-1.5 rounded-xl bg-brand-50 text-brand-700 hover:bg-brand-100"
            >
              <Plus className="w-3.5 h-3.5" />
              {showAddProject ? 'Cancel' : 'Add Project'}
            </button>
          </div>

          {/* Add Project Form */}
          {showAddProject && (
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-3">
              <h3 className="text-xs font-bold text-slate-900">Add Project</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <input
                  type="text"
                  placeholder="Project Title (e.g. Distributed Task Queue)"
                  value={newProject.title}
                  onChange={(e) => setNewProject({ ...newProject, title: e.target.value })}
                  className="text-xs p-2.5 rounded-lg border border-slate-200 bg-white"
                />
                <input
                  type="text"
                  placeholder="Technologies (e.g. Python, Redis, Docker, FastAPI)"
                  value={newProject.technologies || ''}
                  onChange={(e) => setNewProject({ ...newProject, technologies: e.target.value })}
                  className="text-xs p-2.5 rounded-lg border border-slate-200 bg-white"
                />
              </div>
              <input
                type="text"
                placeholder="Project URL / GitHub Repo (optional)"
                value={newProject.project_url || ''}
                onChange={(e) => setNewProject({ ...newProject, project_url: e.target.value })}
                className="w-full text-xs p-2.5 rounded-lg border border-slate-200 bg-white"
              />
              <textarea
                placeholder="Project description, architecture, and personal contributions..."
                rows={3}
                value={newProject.description || ''}
                onChange={(e) => setNewProject({ ...newProject, description: e.target.value })}
                className="w-full text-xs p-2.5 rounded-lg border border-slate-200 bg-white resize-none"
              />
              <button
                type="button"
                onClick={handleAddProject}
                className="px-4 py-2 bg-brand-600 hover:bg-brand-700 text-white rounded-lg text-xs font-bold"
              >
                Save This Project
              </button>
            </div>
          )}

          <div className="space-y-3">
            {projects.length === 0 ? (
              <p className="text-xs text-slate-400 py-2">No projects added yet.</p>
            ) : (
              projects.map((proj, idx) => (
                <div key={idx} className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 flex items-start justify-between gap-4">
                  <div className="space-y-1">
                    <p className="text-xs font-bold text-slate-900">{proj.title}</p>
                    {proj.technologies && (
                      <p className="text-xs text-brand-700 font-medium">{proj.technologies}</p>
                    )}
                    {proj.description && <p className="text-xs text-slate-600">{proj.description}</p>}
                    {proj.project_url && (
                      <a href={proj.project_url} target="_blank" rel="noopener noreferrer" className="inline-block text-[11px] text-brand-600 font-bold hover:underline">
                        View Project Repository →
                      </a>
                    )}
                  </div>
                  <button
                    type="button"
                    onClick={() => handleRemoveProject(idx)}
                    className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              ))
            )}
          </div>
        </div>

        {/* 9. Social Links & Privacy */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-subtle space-y-4">
          <h2 className="text-xs font-bold text-brand-700 uppercase tracking-wider flex items-center gap-1.5">
            <Globe className="w-4 h-4" />
            Social Profiles & Privacy
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">GitHub URL</label>
              <input
                type="text"
                name="github_url"
                value={formData.github_url}
                onChange={handleChange}
                placeholder="https://github.com/..."
                className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">LinkedIn URL</label>
              <input
                type="text"
                name="linkedin_url"
                value={formData.linkedin_url}
                onChange={handleChange}
                placeholder="https://linkedin.com/in/..."
                className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Portfolio Website</label>
              <input
                type="text"
                name="portfolio_url"
                value={formData.portfolio_url}
                onChange={handleChange}
                placeholder="https://mywebsite.dev"
                className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none"
              />
            </div>
          </div>

          <div className="pt-3 border-t border-slate-100 flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold text-slate-800">Hide Personal Contact Details</p>
              <p className="text-[11px] text-slate-500">Only connected members can view your email and phone number</p>
            </div>
            <input
              type="checkbox"
              name="hide_contact_info"
              checked={formData.hide_contact_info}
              onChange={handleChange}
              className="w-4 h-4 text-brand-600 rounded"
            />
          </div>
        </div>

        {/* Submit Button Bar */}
        <div className="flex items-center justify-end gap-3 pt-2">
          <button
            type="button"
            onClick={() => navigate('/profile/me')}
            className="px-5 py-2.5 rounded-xl text-xs font-bold text-slate-600 hover:bg-slate-100"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={isSaving}
            className="px-6 py-2.5 rounded-xl text-xs font-bold text-white bg-brand-600 hover:bg-brand-700 shadow-sm flex items-center gap-1.5 transition-all disabled:opacity-60"
          >
            <Save className="w-4 h-4" />
            {isSaving ? 'Saving Changes...' : 'Save All Changes'}
          </button>
        </div>

      </form>
    </div>
  );
};
