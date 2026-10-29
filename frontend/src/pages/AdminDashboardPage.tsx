import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  ShieldCheck, Users, Award, Briefcase, Calendar, 
  TrendingUp, Sparkles, AlertCircle, BarChart3, ChevronRight 
} from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, 
  ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line 
} from 'recharts';
import { AdminMetrics } from '../types';
import { api } from '../services/api';

export const AdminDashboardPage: React.FC = () => {
  const [metrics, setMetrics] = useState<AdminMetrics | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const data = await api.getAdminMetrics();
        setMetrics(data);
      } catch (err) {
        console.error('Failed to load admin metrics', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchMetrics();
  }, []);

  const COLORS = ['#6366f1', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6'];

  if (isLoading || !metrics) {
    return (
      <div className="space-y-6 py-8 animate-pulse">
        <div className="h-32 bg-white rounded-2xl border border-slate-200" />
        <div className="grid grid-cols-4 gap-4 h-24" />
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-fade-in pb-12">
      
      {/* Top Banner */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-subtle flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-50 border border-amber-200 text-amber-800 text-xs font-bold mb-2">
            <ShieldCheck className="w-3.5 h-3.5 text-amber-600" />
            Institutional Administration & Analytics
          </div>
          <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">
            Executive Platform Dashboard
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Real-time telemetry, student engagement, algorithmic feedback, and moderation queues
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Link
            to="/admin/users"
            className="px-3.5 py-2 rounded-xl text-xs font-bold bg-slate-900 text-white hover:bg-slate-800 transition-colors"
          >
            Manage Users
          </Link>
          <Link
            to="/admin/moderation"
            className="px-3.5 py-2 rounded-xl text-xs font-bold border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 transition-colors"
          >
            Review Reports
          </Link>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        
        <div className="p-5 bg-white rounded-2xl border border-slate-200 shadow-subtle">
          <div className="flex items-center justify-between">
            <p className="text-xs font-medium text-slate-500">Total Registered</p>
            <Users className="w-4 h-4 text-brand-600" />
          </div>
          <p className="text-2xl font-extrabold text-slate-900 mt-1">{metrics.total_users}</p>
          <p className="text-[11px] text-slate-400 mt-0.5">
            {metrics.total_students} Students • {metrics.total_alumni} Alumni
          </p>
        </div>

        <div className="p-5 bg-white rounded-2xl border border-slate-200 shadow-subtle">
          <div className="flex items-center justify-between">
            <p className="text-xs font-medium text-slate-500">Established Connections</p>
            <TrendingUp className="w-4 h-4 text-emerald-600" />
          </div>
          <p className="text-2xl font-extrabold text-slate-900 mt-1">{metrics.total_connections}</p>
          <p className="text-[11px] text-emerald-600 mt-0.5 font-medium">Verified relationships</p>
        </div>

        <div className="p-5 bg-white rounded-2xl border border-slate-200 shadow-subtle">
          <div className="flex items-center justify-between">
            <p className="text-xs font-medium text-slate-500">Mentorship Pipelines</p>
            <Award className="w-4 h-4 text-amber-600" />
          </div>
          <p className="text-2xl font-extrabold text-slate-900 mt-1">{metrics.total_mentorship_requests}</p>
          <p className="text-[11px] text-amber-700 mt-0.5 font-medium">
            {metrics.active_mentorship_sessions} active sessions
          </p>
        </div>

        <div className="p-5 bg-white rounded-2xl border border-slate-200 shadow-subtle">
          <div className="flex items-center justify-between">
            <p className="text-xs font-medium text-slate-500">AI Recommendation Accuracy</p>
            <Sparkles className="w-4 h-4 text-brand-600" />
          </div>
          <p className="text-2xl font-extrabold text-brand-700 mt-1">{metrics.recommendation_feedback_positive_rate}%</p>
          <p className="text-[11px] text-slate-400 mt-0.5">Student positive evaluation rate</p>
        </div>

      </div>

      {/* Recharts Analytics Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Chart 1: Weekly Activity */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-subtle space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Weekly Interaction Volumes</h3>
              <p className="text-xs text-slate-500">Platform connection requests and message volume</p>
            </div>
            <BarChart3 className="w-4 h-4 text-slate-400" />
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={metrics.weekly_activity} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="day" tick={{ fontSize: 11, fill: '#64748b' }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 11, fill: '#64748b' }} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderRadius: '12px', border: '1px solid #e2e8f0', fontSize: '12px' }} />
                <Bar dataKey="messages" fill="#6366f1" radius={[4, 4, 0, 0]} name="Messages" />
                <Bar dataKey="connections" fill="#10b981" radius={[4, 4, 0, 0]} name="Connections" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 2: Industry Distribution */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-subtle space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Alumni Industry Representation</h3>
              <p className="text-xs text-slate-500">Concentration of verified graduates across market sectors</p>
            </div>
            <Briefcase className="w-4 h-4 text-slate-400" />
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={metrics.industry_distribution} layout="vertical" margin={{ top: 10, right: 20, left: 40, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis type="number" tick={{ fontSize: 11, fill: '#64748b' }} axisLine={false} tickLine={false} />
                <YAxis type="category" dataKey="name" tick={{ fontSize: 11, fill: '#64748b' }} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderRadius: '12px', border: '1px solid #e2e8f0', fontSize: '12px' }} />
                <Bar dataKey="value" fill="#4f46e5" radius={[0, 4, 4, 0]} name="Alumni Count" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>

    </div>
  );
};
