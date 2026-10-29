import React, { useState } from 'react';
import { X, Award, Send, AlertCircle, Clock } from 'lucide-react';
import { Profile } from '../types';
import { api } from '../services/api';
import { useToast } from '../context/ToastContext';
import { Avatar } from './Avatar';

interface MentorshipModalProps {
  mentor: Profile | null;
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export const MentorshipModal: React.FC<MentorshipModalProps> = ({
  mentor,
  isOpen,
  onClose,
  onSuccess,
}) => {
  if (!isOpen || !mentor) return null;

  const toast = useToast();
  const [goalsDescription, setGoalsDescription] = useState('');
  const [frequency, setFrequency] = useState('Bi-weekly');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!goalsDescription.trim()) {
      setError('Please provide a brief statement of your mentorship goals.');
      return;
    }

    setIsSubmitting(true);
    setError(null);
    try {
      await api.requestMentorship({
        mentor_id: mentor.user_id,
        goals_description: goalsDescription.trim(),
        preferred_frequency: frequency,
      });
      toast.success(`Mentorship request submitted to ${mentor.full_name}!`);
      onSuccess();
      onClose();
    } catch (err: any) {
      setError(err.message || 'Failed to submit mentorship application');
      toast.error(err.message || 'Failed to submit mentorship application');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
      <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-elevated border border-slate-200">
        
        <div className="flex items-center justify-between pb-3 border-b border-slate-100">
          <div className="flex items-center gap-2">
            <div className="p-1.5 rounded-lg bg-amber-50 text-amber-600 border border-amber-200">
              <Award className="w-4 h-4" />
            </div>
            <h3 className="text-base font-bold text-slate-900">
              Apply for Mentorship
            </h3>
          </div>
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

        {/* Mentor Mini Card */}
        <div className="flex items-center gap-3 my-4 p-3 bg-slate-50 rounded-xl border border-slate-200">
          <Avatar name={mentor.full_name} size="lg" />
          <div>
            <p className="text-xs font-bold text-slate-900">{mentor.full_name}</p>
            <p className="text-xs text-slate-600">{mentor.current_job_title} at {mentor.current_company}</p>
            {mentor.mentorship_topics && mentor.mentorship_topics.length > 0 && (
              <div className="flex flex-wrap gap-1 mt-1">
                {mentor.mentorship_topics.map(t => (
                  <span key={t} className="text-[10px] font-medium px-1.5 py-0.5 rounded bg-amber-50 text-amber-700 border border-amber-200">
                    {t}
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              What are your key learning and career goals for this mentorship? *
            </label>
            <textarea
              required
              rows={4}
              value={goalsDescription}
              onChange={(e) => setGoalsDescription(e.target.value)}
              placeholder="e.g., I would love guidance on preparing for technical interviews, transitioning into AI systems, and feedback on my portfolio projects."
              className="w-full text-xs p-3 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-amber-500/30 focus:border-amber-500 resize-none"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Preferred Meeting Cadence
            </label>
            <select
              value={frequency}
              onChange={(e) => setFrequency(e.target.value)}
              className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-amber-500/30 focus:border-amber-500 bg-white"
            >
              <option value="Weekly">Weekly (45 mins)</option>
              <option value="Bi-weekly">Bi-weekly (45 mins) - Recommended</option>
              <option value="Monthly">Monthly Strategy Check-in</option>
              <option value="Ad-hoc">As-needed Questions & Mock Reviews</option>
            </select>
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
              className="px-4 py-2 text-xs font-semibold text-white bg-amber-600 hover:bg-amber-700 rounded-lg shadow-sm flex items-center gap-1.5 transition-all disabled:opacity-60"
            >
              <Send className="w-3.5 h-3.5" />
              {isSubmitting ? 'Submitting Application...' : 'Submit Mentorship Request'}
            </button>
          </div>
        </form>

      </div>
    </div>
  );
};
