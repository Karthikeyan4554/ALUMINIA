import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, Sparkles, Users, Bot, MessageSquare, 
  UserCheck, Award, Briefcase, Calendar, User, Settings, 
  ShieldCheck, ArrowUpRight
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { Avatar } from './Avatar';

export const Sidebar: React.FC<{ isOpen: boolean; onClose: () => void }> = ({ isOpen, onClose }) => {
  const { user, profile } = useAuth();

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
    { name: 'AI Connections', href: '/recommendations', icon: Sparkles, badge: 'AI Match' },
    { name: 'Alumni Directory', href: '/directory', icon: Users },
    { name: 'AI Assistant', href: '/assistant', icon: Bot, badge: 'Advisor' },
    { name: 'Messages', href: '/messages', icon: MessageSquare },
    { name: 'My Network', href: '/connections', icon: UserCheck },
    { name: 'Mentorship', href: '/mentorship', icon: Award },
    { name: 'Jobs & Internships', href: '/jobs', icon: Briefcase },
    { name: 'Alumni Events', href: '/events', icon: Calendar },
  ];

  const adminNav = [
    { name: 'Admin Dashboard', href: '/admin', icon: ShieldCheck },
    { name: 'User Management', href: '/admin/users', icon: Users },
    { name: 'Moderation & Reports', href: '/admin/moderation', icon: ShieldCheck },
  ];

  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div
          onClick={onClose}
          className="fixed inset-0 z-40 bg-slate-900/40 backdrop-blur-sm lg:hidden"
        />
      )}

      {/* Sidebar aside container */}
      <aside
        className={`fixed top-16 bottom-0 left-0 z-40 w-64 border-r border-slate-200 bg-white transition-transform duration-200 ease-in-out lg:translate-x-0 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex flex-col h-full justify-between p-4 overflow-y-auto">
          
          <div className="space-y-6">
            {/* Quick Profile Summary Card */}
            {profile && (
              <div className="p-3 rounded-xl bg-slate-50 border border-slate-200/80">
                <div className="flex items-center gap-3">
                  <Avatar name={profile.full_name} size="md" />
                  <div className="min-w-0 flex-1">
                    <p className="text-xs font-bold text-slate-900 truncate">{profile.full_name}</p>
                    <p className="text-[11px] text-slate-500 truncate">{profile.current_job_title || profile.department}</p>
                  </div>
                </div>

                {/* Profile Completion Bar */}
                <div className="mt-3">
                  <div className="flex items-center justify-between text-[11px] mb-1">
                    <span className="text-slate-500 font-medium">Profile Score</span>
                    <span className="font-bold text-brand-700">{profile.profile_completion_percentage}%</span>
                  </div>
                  <div className="w-full h-1.5 bg-slate-200 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-brand-600 to-indigo-600 rounded-full transition-all duration-500"
                      style={{ width: `${profile.profile_completion_percentage}%` }}
                    />
                  </div>
                </div>
              </div>
            )}

            {/* Main Navigation links */}
            <div>
              <p className="px-3 text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-2">
                Platform Navigation
              </p>
              <nav className="space-y-1">
                {navigation.map((item) => (
                  <NavLink
                    key={item.name}
                    to={item.href}
                    onClick={onClose}
                    className={({ isActive }) =>
                      `flex items-center justify-between px-3 py-2 text-xs font-semibold rounded-lg transition-all ${
                        isActive
                          ? 'bg-brand-50 text-brand-700 shadow-sm'
                          : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                      }`
                    }
                  >
                    <div className="flex items-center gap-2.5">
                      <item.icon className="w-4 h-4" />
                      <span>{item.name}</span>
                    </div>
                    {item.badge && (
                      <span className="px-2 py-0.5 text-[10px] font-bold rounded-full bg-brand-100 text-brand-700 border border-brand-200">
                        {item.badge}
                      </span>
                    )}
                  </NavLink>
                ))}
              </nav>
            </div>

            {/* Admin Console links */}
            {user?.role === 'admin' && (
              <div>
                <p className="px-3 text-[11px] font-bold uppercase tracking-wider text-amber-600 mb-2 flex items-center gap-1.5">
                  <ShieldCheck className="w-3.5 h-3.5" />
                  Administrator
                </p>
                <nav className="space-y-1">
                  {adminNav.map((item) => (
                    <NavLink
                      key={item.name}
                      to={item.href}
                      onClick={onClose}
                      className={({ isActive }) =>
                        `flex items-center gap-2.5 px-3 py-2 text-xs font-semibold rounded-lg transition-all ${
                          isActive
                            ? 'bg-amber-100 text-amber-900 font-bold'
                            : 'text-amber-800 hover:bg-amber-50'
                        }`
                      }
                    >
                      <item.icon className="w-4 h-4 text-amber-600" />
                      <span>{item.name}</span>
                    </NavLink>
                  ))}
                </nav>
              </div>
            )}
          </div>

          {/* Bottom Settings & Help */}
          <div className="pt-4 border-t border-slate-200 space-y-1">
            <NavLink
              to="/profile/me"
              onClick={onClose}
              className="flex items-center gap-2.5 px-3 py-2 text-xs font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-50 rounded-lg"
            >
              <User className="w-4 h-4 text-slate-400" />
              <span>My Public Profile</span>
            </NavLink>
            <NavLink
              to="/settings"
              onClick={onClose}
              className="flex items-center gap-2.5 px-3 py-2 text-xs font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-50 rounded-lg"
            >
              <Settings className="w-4 h-4 text-slate-400" />
              <span>Settings & Privacy</span>
            </NavLink>
          </div>

        </div>
      </aside>
    </>
  );
};
