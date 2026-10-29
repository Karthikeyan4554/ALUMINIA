import React, { useState } from 'react';
import { X, Send, Sparkles, AlertCircle } from 'lucide-react';
import { Recommendation, Profile } from '../types';
import { api } from '../services/api';
import { useToast } from '../context/ToastContext';
import { Avatar } from './Avatar';

interface ConnectModalProps {
  target: { profile: Profile; starter?: string } | null;
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export const ConnectModal: React.FC<ConnectModalProps> = ({
  target,
  isOpen,
  onClose,
  onSuccess,
}) => {
  if (!isOpen || !target) return null;

  const toast = useToast();
  const [message, setMessage] = useState(target.starter || '');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);
    try {
      await api.sendConnectionRequest({
        receiver_id: target.profile.user_id,
        message: message.trim() || undefined,
      });
      toast.success(`Connection request sent to ${target.profile.full_name}!`);
      onSuccess();
      onClose();
    } catch (err: any) {
      setError(err.message || 'Failed to send connection request');
      toast.error(err.message || 'Failed to send connection request');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
      <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-elevated border border-slate-200">
        
        <div className="flex items-center justify-between pb-3 border-b border-slate-100">
          <h3 className="text-base font-bold text-slate-900">
            Connect with {target.profile.full_name}
          </h3>
          <button
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {error && (
          <div className="mt-3 p-3 rounded-xl bg-rose-50 border border-rose-200 text-xs text-rose-700 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <div className="flex items-center gap-3 my-4 p-3 bg-slate-50 rounded-xl border border-slate-200">
          <Avatar name={target.profile.full_name} size="lg" />
          <div>
            <p className="text-xs font-bold text-slate-900">{target.profile.full_name}</p>
            <p className="text-xs text-slate-600">{target.profile.current_job_title} at {target.profile.current_company}</p>
            <p className="text-[11px] text-slate-400">{target.profile.department} • Class of {target.profile.graduation_year}</p>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <div className="flex items-center justify-between mb-1">
              <label className="text-xs font-semibold text-slate-700">
                Personalized Note (Optional)
              </label>
              {target.starter && (
                <button
                  type="button"
                  onClick={() => setMessage(target.starter || '')}
                  className="text-[11px] text-brand-600 hover:text-brand-700 font-semibold flex items-center gap-1"
                >
                  <Sparkles className="w-3 h-3" /> Insert AI Icebreaker
                </button>
              )}
            </div>
            <textarea
              rows={4}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Hi Deepa, I'm a final-year CS student interested in ML careers at Google and would love to connect..."
              className="w-full text-xs p-3 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/30 focus:border-brand-500 resize-none"
            />
            <p className="text-[11px] text-slate-400 mt-1">
              Adding a friendly intro note helps alumni understand your background and goals.
            </p>
          </div>

          <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded-lg transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="px-4 py-2 text-xs font-semibold text-white bg-brand-600 hover:bg-brand-700 rounded-lg shadow-sm flex items-center gap-1.5 transition-all disabled:opacity-60"
            >
              <Send className="w-3.5 h-3.5" />
              {isSubmitting ? 'Sending Request...' : 'Send Invitation'}
            </button>
          </div>
        </form>

      </div>
    </div>
  );
};
