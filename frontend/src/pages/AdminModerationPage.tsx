import React, { useState, useEffect } from 'react';
import { Shield, AlertTriangle, CheckCircle, XCircle, Search } from 'lucide-react';
import { ContentReport } from '../types';
import { api } from '../services/api';

export const AdminModerationPage: React.FC = () => {
  const [reports, setReports] = useState<ContentReport[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchReports = async () => {
    setIsLoading(true);
    try {
      const data = await api.getAdminReports();
      setReports(data);
    } catch (err) {
      console.error('Failed to load reports', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  const handleResolve = async (reportId: string, action: 'resolved' | 'dismissed') => {
    try {
      await api.resolveAdminReport(reportId, action);
      fetchReports();
    } catch (err) {
      console.error('Failed to resolve report', err);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in pb-12">
      
      {/* Header Banner */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-subtle flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <Shield className="w-6 h-6 text-brand-600" />
            Moderation & Content Safety
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Review reported accounts, flagged messages, and inappropriate listings
          </p>
        </div>
        <span className="text-xs font-bold px-3 py-1 bg-amber-50 text-amber-800 rounded-xl border border-amber-200">
          {reports.filter(r => r.status === 'pending').length} Action Items Pending
        </span>
      </div>

      {/* Reports List */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-subtle divide-y divide-slate-100 overflow-hidden">
        {reports.length === 0 ? (
          <div className="p-12 text-center text-xs text-slate-500 space-y-2">
            <CheckCircle className="w-8 h-8 text-emerald-500 mx-auto" />
            <p className="font-bold text-slate-700">All Clear!</p>
            <p>No active reports or moderation violations on file.</p>
          </div>
        ) : (
          reports.map((r) => (
            <div key={r.id} className="p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 text-xs">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-slate-100 text-slate-700">
                    {r.content_type}
                  </span>
                  <span
                    className={`px-2 py-0.5 rounded text-[10px] font-bold capitalize ${
                      r.status === 'pending'
                        ? 'bg-amber-100 text-amber-800'
                        : r.status === 'resolved'
                        ? 'bg-emerald-100 text-emerald-800'
                        : 'bg-slate-200 text-slate-600'
                    }`}
                  >
                    {r.status}
                  </span>
                </div>
                <p className="font-bold text-slate-900 pt-1">Reason: {r.reason}</p>
                <p className="text-[11px] text-slate-400">Reported on {new Date(r.created_at).toLocaleString()}</p>
              </div>

              {r.status === 'pending' && (
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => handleResolve(r.id, 'resolved')}
                    className="px-3.5 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold transition-colors"
                  >
                    Resolve & Warn
                  </button>
                  <button
                    onClick={() => handleResolve(r.id, 'dismissed')}
                    className="px-3.5 py-1.5 rounded-xl border border-slate-200 hover:bg-slate-50 text-slate-700 font-semibold transition-colors"
                  >
                    Dismiss
                  </button>
                </div>
              )}
            </div>
          ))
        )}
      </div>

    </div>
  );
};
