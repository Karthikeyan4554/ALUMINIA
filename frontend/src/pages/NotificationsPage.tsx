import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Bell, Check, UserPlus, MessageSquare, Award, 
  Briefcase, Calendar, CheckCheck, Clock 
} from 'lucide-react';
import { useNotifications } from '../context/NotificationContext';

export const NotificationsPage: React.FC = () => {
  const { notifications, unreadCount, markAsRead, markAllAsRead } = useNotifications();
  const navigate = useNavigate();

  const getIcon = (type: string) => {
    switch (type) {
      case 'connection_request':
      case 'connection_accepted':
        return <UserPlus className="w-4 h-4 text-brand-600" />;
      case 'message':
        return <MessageSquare className="w-4 h-4 text-indigo-600" />;
      case 'mentorship_request':
      case 'mentorship_accepted':
      case 'mentorship_session':
        return <Award className="w-4 h-4 text-amber-600" />;
      case 'job_alert':
        return <Briefcase className="w-4 h-4 text-emerald-600" />;
      case 'event_reminder':
        return <Calendar className="w-4 h-4 text-purple-600" />;
      default:
        return <Bell className="w-4 h-4 text-slate-500" />;
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6 pb-12 animate-fade-in">
      
      {/* Top Banner */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-subtle flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <Bell className="w-6 h-6 text-brand-600" />
            Notifications Center
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Real-time updates on connections, mentorship requests, and system alerts
          </p>
        </div>

        {unreadCount > 0 && (
          <button
            onClick={markAllAsRead}
            className="px-3.5 py-2 rounded-xl text-xs font-bold bg-brand-50 hover:bg-brand-100 text-brand-700 border border-brand-200 transition-colors flex items-center gap-1.5"
          >
            <CheckCheck className="w-4 h-4" />
            Mark all read
          </button>
        )}
      </div>

      {/* Notifications List */}
      <div className="bg-white rounded-2xl border border-slate-200 divide-y divide-slate-100 overflow-hidden shadow-subtle">
        {notifications.length === 0 ? (
          <div className="p-12 text-center text-xs text-slate-400 space-y-2">
            <Bell className="w-8 h-8 text-slate-300 mx-auto" />
            <p>You're completely caught up. No notifications right now.</p>
          </div>
        ) : (
          notifications.map((n) => (
            <div
              key={n.id}
              onClick={() => {
                markAsRead(n.id);
                if (n.link) navigate(n.link);
              }}
              className={`p-4 flex items-start gap-3.5 cursor-pointer transition-colors ${
                n.is_read ? 'hover:bg-slate-50' : 'bg-brand-50/50 hover:bg-brand-50'
              }`}
            >
              <div className="p-2 rounded-xl bg-white border border-slate-200 shadow-sm flex-shrink-0 mt-0.5">
                {getIcon(n.type)}
              </div>

              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between gap-2">
                  <p className="text-xs font-bold text-slate-900">{n.title}</p>
                  <span className="text-[10px] text-slate-400 flex items-center gap-1 flex-shrink-0">
                    <Clock className="w-3 h-3" />
                    {new Date(n.created_at).toLocaleDateString()}
                  </span>
                </div>
                <p className="text-xs text-slate-600 mt-0.5 leading-relaxed">{n.message}</p>
              </div>

              {!n.is_read && (
                <span className="w-2.5 h-2.5 rounded-full bg-brand-600 mt-2 flex-shrink-0" />
              )}
            </div>
          ))
        )}
      </div>

    </div>
  );
};
