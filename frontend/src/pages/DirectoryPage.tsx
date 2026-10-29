import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Search, Users, Filter, Building, MapPin, GraduationCap, 
  Award, LayoutGrid, List, UserPlus, Eye, ChevronLeft, ChevronRight 
} from 'lucide-react';
import { Profile } from '../types';
import { api } from '../services/api';
import { ConnectModal } from '../components/ConnectModal';
import { MentorshipModal } from '../components/MentorshipModal';
import { Avatar } from '../components/Avatar';

const DEFAULT_DEPARTMENTS = [
  'Aerospace & Aeronautical Engineering',
  'Agriculture & Food Engineering',
  'Artificial Intelligence and Data Science',
  'Automotive & Electric Vehicle Engineering',
  'Autonomous Aerial Systems',
  'Biomedical & Medical Electronics Engineering',
  'Biotechnology & Bioprocess Engineering',
  'Chemical & Process Engineering',
  'Civil & Structural Engineering',
  'Computer Science and Engineering',
  'Cybersecurity & Digital Forensics Engineering',
  'Electrical and Electronics Engineering',
  'Electronics & Embedded IoT',
  'Electronics & VLSI Engineering',
  'Electronics and Communication Engineering',
  'Environmental Engineering & Sustainability',
  'Industrial Engineering & Operations Research',
  'Information Technology',
  'Marine & Ocean Engineering',
  'Materials Science & Metallurgical Engineering',
  'Mechanical Engineering',
  'Mechatronics & Precision Engineering',
  'Renewable Energy & Power Engineering',
  'Robotics & Automation Engineering',
  'Smart Grid & Electric Mobility',
  'Textile & Fashion Technology'
];

const DEFAULT_INDUSTRIES = [
  'Advanced Materials & Metallurgy',
  'Aerospace & Defense',
  'Agritech & Food Processing',
  'Artificial Intelligence',
  'Automotive & Clean Mobility',
  'Biotech & Healthcare',
  'Clean Energy & Power Systems',
  'Cloud & Enterprise Software',
  'Consumer Tech',
  'Cybersecurity & Critical Infrastructure',
  'E-Commerce',
  'Environmental Tech & Sustainability',
  'FinTech',
  'Healthcare & MedTech',
  'Infrastructure & Smart Cities',
  'Marine & Ocean Technology',
  'Medical Devices & MedTech',
  'Process Engineering & Petrochemicals',
  'Robotics & Industrial Automation',
  'Semiconductors',
  'Smart Textiles & Apparel Manufacturing',
  'Software & Cloud',
  'VLSI & Semiconductor Tech'
];

export const DirectoryPage: React.FC = () => {
  const [profiles, setProfiles] = useState<Profile[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [isLoading, setIsLoading] = useState(true);

  // Dynamic filter options
  const [departmentsList, setDepartmentsList] = useState<string[]>(DEFAULT_DEPARTMENTS);
  const [industriesList, setIndustriesList] = useState<string[]>(DEFAULT_INDUSTRIES);

  // Filters
  const [searchQuery, setSearchQuery] = useState('');
  const [role, setRole] = useState('alumni');
  const [industry, setIndustry] = useState('');
  const [department, setDepartment] = useState('');
  const [mentorshipOnly, setMentorshipOnly] = useState(false);
  const [sortBy, setSortBy] = useState('experience');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  // Modals
  const [connectTarget, setConnectTarget] = useState<any | null>(null);
  const [mentorTarget, setMentorTarget] = useState<Profile | null>(null);

  useEffect(() => {
    const fetchFilters = async () => {
      try {
        const meta = await api.getDirectoryFilters();
        if (meta.departments?.length) setDepartmentsList(meta.departments);
        if (meta.industries?.length) setIndustriesList(meta.industries);
      } catch (err) {
        console.error('Failed to load filter options', err);
      }
    };
    fetchFilters();
  }, []);

  const fetchDirectory = async () => {
    setIsLoading(true);
    try {
      const res = await api.getDirectory({
        query: searchQuery || undefined,
        role: role !== 'all' ? role : undefined,
        industry: industry || undefined,
        department: department || undefined,
        mentorship_only: mentorshipOnly || undefined,
        sort_by: sortBy,
        page,
        limit: 12,
      });
      setProfiles(res.items);
      setTotal(res.total);
    } catch (err) {
      console.error('Failed to load directory', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchDirectory();
  }, [searchQuery, role, industry, department, mentorshipOnly, sortBy, page]);

  return (
    <div className="space-y-6 animate-fade-in">
      
      {/* Top Banner */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-subtle">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-brand-50 border border-brand-200 text-brand-700 text-xs font-bold mb-2">
            <Users className="w-3.5 h-3.5 text-brand-600" />
            University Network Registry
          </div>
          <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">
            Alumni & Student Directory
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Browse verified graduates, faculty, mentors, and peers across industries and programs
          </p>
        </div>

        <div className="flex items-center gap-2 border border-slate-200 rounded-xl p-1 bg-slate-50">
          <button
            onClick={() => setViewMode('grid')}
            className={`p-1.5 rounded-lg text-xs font-semibold transition-colors ${
              viewMode === 'grid' ? 'bg-white shadow-sm text-brand-700' : 'text-slate-500 hover:text-slate-900'
            }`}
            title="Grid View"
          >
            <LayoutGrid className="w-4 h-4" />
          </button>
          <button
            onClick={() => setViewMode('list')}
            className={`p-1.5 rounded-lg text-xs font-semibold transition-colors ${
              viewMode === 'list' ? 'bg-white shadow-sm text-brand-700' : 'text-slate-500 hover:text-slate-900'
            }`}
            title="List View"
          >
            <List className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="p-4 bg-white rounded-2xl border border-slate-200 shadow-subtle space-y-3 text-xs">
        <div className="flex flex-wrap items-center gap-3">
          
          {/* Search box */}
          <div className="relative flex-1 min-w-[240px]">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search by name, skill, company, title..."
              className="w-full pl-9 pr-3 py-2 rounded-xl border border-slate-200 bg-slate-50 focus:outline-none focus:ring-2 focus:ring-brand-500/20"
            />
          </div>

          {/* Role selector */}
          <select
            value={role}
            onChange={(e) => { setRole(e.target.value); setPage(1); }}
            className="p-2 rounded-xl border border-slate-200 bg-slate-50 font-medium text-slate-700 focus:outline-none"
          >
            <option value="alumni">Alumni Only</option>
            <option value="student">Students Only</option>
            <option value="all">All Members</option>
          </select>

          {/* Industry filter */}
          <select
            value={industry}
            onChange={(e) => { setIndustry(e.target.value); setPage(1); }}
            className="p-2 rounded-xl border border-slate-200 bg-slate-50 font-medium text-slate-700 focus:outline-none max-w-[190px] truncate"
          >
            <option value="">All Industries ({industriesList.length})</option>
            {industriesList.map((ind) => (
              <option key={ind} value={ind} title={ind}>{ind}</option>
            ))}
          </select>

          {/* Department filter */}
          <select
            value={department}
            onChange={(e) => { setDepartment(e.target.value); setPage(1); }}
            className="p-2 rounded-xl border border-slate-200 bg-slate-50 font-medium text-slate-700 focus:outline-none max-w-[210px] truncate"
          >
            <option value="">All Departments ({departmentsList.length})</option>
            {departmentsList.map((dept) => (
              <option key={dept} value={dept} title={dept}>{dept}</option>
            ))}
          </select>

          {/* Mentorship toggle */}
          <label className="flex items-center gap-1.5 font-semibold text-slate-700 cursor-pointer select-none">
            <input
              type="checkbox"
              checked={mentorshipOnly}
              onChange={(e) => setMentorshipOnly(e.target.checked)}
              className="w-4 h-4 text-brand-600 rounded"
            />
            <span>Open Mentors</span>
          </label>

          {/* Sort selector */}
          <div className="flex items-center gap-1.5 ml-auto">
            <span className="text-slate-400 font-semibold">Sort:</span>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="p-2 rounded-xl border border-slate-200 bg-slate-50 font-medium text-slate-700 focus:outline-none"
            >
              <option value="experience">Experience</option>
              <option value="grad_year">Grad Year</option>
              <option value="name">Name</option>
            </select>
          </div>

        </div>
      </div>

      {/* Directory Grid / List View */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5 py-8">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="h-48 rounded-2xl bg-white border border-slate-200 animate-pulse p-5 space-y-3">
              <div className="w-12 h-12 rounded-full bg-slate-200" />
              <div className="h-4 bg-slate-200 rounded w-1/2" />
              <div className="h-3 bg-slate-100 rounded w-3/4" />
            </div>
          ))}
        </div>
      ) : profiles.length === 0 ? (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center space-y-3">
          <Users className="w-10 h-10 text-slate-300 mx-auto" />
          <h3 className="text-base font-bold text-slate-900">No Members Match the Criteria</h3>
          <p className="text-xs text-slate-500">Try loosening your search filters or resetting to view all alumni.</p>
        </div>
      ) : viewMode === 'grid' ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {profiles.map((p) => (
            <div
              key={p.user_id}
              className="bg-white rounded-2xl border border-slate-200/90 p-5 shadow-subtle hover:shadow-premium transition-all duration-200 flex flex-col justify-between"
            >
              <div>
                <div className="flex items-start gap-3.5">
                  <Link to={`/profile/${p.user_id}`}>
                    <Avatar
                      name={p.full_name}
                      size="md"
                      className="rounded-xl hover:scale-105 transition-transform"
                    />
                  </Link>
                  <div className="min-w-0 flex-1">
                    <Link to={`/profile/${p.user_id}`} className="hover:text-brand-600 transition-colors">
                      <h3 className="font-bold text-slate-900 text-sm truncate flex items-center gap-1">
                        {p.full_name}
                      </h3>
                    </Link>
                    <p className="text-xs text-brand-700 font-semibold truncate">
                      {p.current_job_title || p.headline || 'Member'}
                    </p>
                    <p className="text-[11px] text-slate-500 truncate flex items-center gap-1 mt-0.5">
                      <Building className="w-3 h-3 text-slate-400" />
                      {p.current_company || 'University'}
                    </p>
                  </div>
                </div>

                <div className="mt-3 flex items-center gap-2 text-[11px] text-slate-500">
                  <span className="flex items-center gap-1">
                    <GraduationCap className="w-3 h-3" /> Class of {p.graduation_year || 2022}
                  </span>
                  <span>•</span>
                  <span className="flex items-center gap-1">
                    <MapPin className="w-3 h-3" /> {p.location || 'Remote'}
                  </span>
                </div>

                {/* Skills tags */}
                {p.skills && p.skills.length > 0 && (
                  <div className="mt-3 flex flex-wrap gap-1">
                    {p.skills.slice(0, 3).map((s) => (
                      <span key={s} className="px-2 py-0.5 rounded text-[10px] font-medium bg-slate-100 text-slate-600">
                        {s}
                      </span>
                    ))}
                    {p.skills.length > 3 && (
                      <span className="px-1.5 py-0.5 rounded text-[10px] text-slate-400">
                        +{p.skills.length - 3}
                      </span>
                    )}
                  </div>
                )}
              </div>

              {/* Action buttons */}
              <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between gap-2">
                <Link
                  to={`/profile/${p.user_id}`}
                  className="px-3 py-1.5 text-xs font-semibold rounded-lg border border-slate-200 text-slate-700 hover:bg-slate-50 flex items-center gap-1"
                >
                  <Eye className="w-3.5 h-3.5" />
                  View
                </Link>

                <div className="flex items-center gap-1.5">
                  {p.mentorship_available && (
                    <button
                      onClick={() => setMentorTarget(p)}
                      className="px-2.5 py-1.5 text-xs font-semibold rounded-lg bg-amber-50 text-amber-800 border border-amber-200 hover:bg-amber-100 flex items-center gap-1"
                      title="Request Mentorship"
                    >
                      <Award className="w-3.5 h-3.5" />
                    </button>
                  )}

                  <button
                    onClick={() => setConnectTarget({ profile: p })}
                    disabled={p.connection_status === 'connected' || p.connection_status === 'pending_sent'}
                    className={`px-3 py-1.5 text-xs font-semibold rounded-lg flex items-center gap-1 transition-all ${
                      p.connection_status === 'connected'
                        ? 'bg-emerald-100 text-emerald-800 cursor-default'
                        : p.connection_status === 'pending_sent'
                        ? 'bg-slate-100 text-slate-500 cursor-default'
                        : 'bg-brand-600 hover:bg-brand-700 text-white shadow-sm'
                    }`}
                  >
                    <UserPlus className="w-3.5 h-3.5" />
                    {p.connection_status === 'connected'
                      ? 'Connected'
                      : p.connection_status === 'pending_sent'
                      ? 'Sent'
                      : 'Connect'}
                  </button>
                </div>
              </div>

            </div>
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden divide-y divide-slate-100">
          {profiles.map((p) => (
            <div key={p.user_id} className="p-4 hover:bg-slate-50/80 transition-colors flex items-center justify-between gap-4">
              <div className="flex items-center gap-3.5 min-w-0">
                <Avatar
                  name={p.full_name}
                  size="sm"
                  className="rounded-full flex-shrink-0"
                />
                <div className="min-w-0">
                  <Link to={`/profile/${p.user_id}`} className="font-bold text-slate-900 text-xs hover:text-brand-600 truncate block">
                    {p.full_name}
                  </Link>
                  <p className="text-[11px] text-slate-500 truncate">
                    {p.current_job_title || p.headline} at {p.current_company || 'University'} • Class of {p.graduation_year}
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-2 flex-shrink-0">
                <Link
                  to={`/profile/${p.user_id}`}
                  className="px-3 py-1.5 text-xs font-semibold rounded-lg border border-slate-200 text-slate-700 hover:bg-white"
                >
                  View Profile
                </Link>
                <button
                  onClick={() => setConnectTarget({ profile: p })}
                  disabled={p.connection_status === 'connected' || p.connection_status === 'pending_sent'}
                  className="px-3 py-1.5 text-xs font-semibold rounded-lg bg-brand-600 hover:bg-brand-700 text-white shadow-sm disabled:opacity-50"
                >
                  {p.connection_status === 'connected' ? 'Connected' : 'Connect'}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Pagination Footer */}
      {total > 12 && (
        <div className="flex items-center justify-between bg-white p-4 rounded-2xl border border-slate-200 text-xs text-slate-600">
          <span>Showing {profiles.length} of {total} registered members</span>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setPage(Math.max(1, page - 1))}
              disabled={page === 1}
              className="p-1.5 rounded-lg border border-slate-200 hover:bg-slate-50 disabled:opacity-50"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="font-bold">Page {page}</span>
            <button
              onClick={() => setPage(page + 1)}
              disabled={profiles.length < 12}
              className="p-1.5 rounded-lg border border-slate-200 hover:bg-slate-50 disabled:opacity-50"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* Modals */}
      <ConnectModal
        isOpen={!!connectTarget}
        target={connectTarget}
        onClose={() => setConnectTarget(null)}
        onSuccess={fetchDirectory}
      />

      <MentorshipModal
        isOpen={!!mentorTarget}
        mentor={mentorTarget}
        onClose={() => setMentorTarget(null)}
        onSuccess={fetchDirectory}
      />

    </div>
  );
};
