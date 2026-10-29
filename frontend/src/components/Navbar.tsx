import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  GraduationCap, Bell, MessageSquare, Sparkles, User, 
  LogOut, Shield, Menu, X, ChevronDown, Check, ExternalLink 
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useNotifications } from '../context/NotificationContext';
import { Avatar } from './Avatar';

export const Navbar: React.FC<{ onToggleSidebar?: () => void }> = ({ onToggleSidebar }) => {
  const { user, profile, isAuthenticated, logout } = useAuth();
  const { notifications, unreadCount, markAsRead, markAllAsRead } = useNotifications();
  const [showNotifications, setShowNotifications] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-200 bg-white/95 backdrop-blur-md">
      <div className="flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8">
        
        {/* Left: Brand Logo & Hamburger */}
        <div className="flex items-center gap-4">
          {isAuthenticated && onToggleSidebar && (
            <button
              onClick={onToggleSidebar}
              className="p-2 text-slate-500 hover:text-slate-800 hover:bg-slate-100 rounded-lg lg:hidden"
              aria-label="Toggle Navigation Menu"
            >
              <Menu className="w-5 h-5" />
            </button>
          )}

          <Link to={isAuthenticated ? "/dashboard" : "/"} className="flex items-center gap-2.5 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-700 via-brand-600 to-indigo-500 flex items-center justify-center text-white shadow-md shadow-brand-500/20 group-hover:scale-105 transition-transform duration-200">
              <GraduationCap className="w-5 h-5" />
            </div>
            <div>
              <span className="text-xl font-bold tracking-tight text-slate-900 group-hover:text-brand-700 transition-colors">
                Alumnia
              </span>
              <span className="hidden sm:inline-block ml-2 text-xs font-medium px-2 py-0.5 rounded-full bg-brand-50 text-brand-700 border border-brand-200">
                Connect Beyond Graduation
              </span>
            </div>
          </Link>
        </div>

        {/* Center: Search / Public Nav */}
        <div className="hidden md:flex items-center gap-6">
          {!isAuthenticated ? (
            <nav className="flex items-center gap-6 text-sm font-medium text-slate-600">
              <Link to="/" className="hover:text-brand-600 transition-colors">Home</Link>
              <Link to="/features" className="hover:text-brand-600 transition-colors">Features</Link>
              <Link to="/about" className="hover:text-brand-600 transition-colors">About Platform</Link>
            </nav>
          ) : (
            <div className="flex items-center gap-3">
              <Link
                to="/recommendations"
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold bg-gradient-to-r from-violet-600 to-indigo-600 text-white shadow-sm hover:opacity-95 transition-all"
              >
                <Sparkles className="w-3.5 h-3.5" />
                AI Connections
              </Link>
              <Link
                to="/assistant"
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold bg-slate-100 text-slate-700 hover:bg-slate-200 transition-colors"
              >
                AI Assistant
              </Link>
            </div>
          )}
        </div>

        {/* Right: Actions / Auth buttons / Notification & Profile */}
        <div className="flex items-center gap-3">
          {!isAuthenticated ? (
            <div className="flex items-center gap-3">
              <Link
                to="/login"
                className="text-sm font-semibold text-slate-700 hover:text-brand-600 px-3 py-2 transition-colors"
              >
                Sign In
              </Link>
              <Link
                to="/register"
                className="inline-flex items-center justify-center rounded-lg text-sm font-semibold bg-brand-600 text-white px-4 py-2 hover:bg-brand-700 shadow-sm transition-all"
              >
                Get Started
              </Link>
            </div>
          ) : (
            <div className="flex items-center gap-2 sm:gap-3">
              
              {/* Messages Shortcut */}
              <Link
                to="/messages"
                className="p-2 text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-lg relative transition-colors"
                title="Messages"
              >
                <MessageSquare className="w-5 h-5" />
              </Link>

              {/* Notifications Dropdown */}
              <div className="relative">
                <button
                  onClick={() => setShowNotifications(!showNotifications)}
                  className="p-2 text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-lg relative transition-colors"
                  title="Notifications"
                >
                  <Bell className="w-5 h-5" />
                  {unreadCount > 0 && (
                    <span className="absolute top-1.5 right-1.5 flex h-4 w-4 items-center justify-center rounded-full bg-rose-500 text-[10px] font-bold text-white shadow-sm ring-2 ring-white">
                      {unreadCount > 9 ? '9+' : unreadCount}
                    </span>
                  )}
                </button>

                {showNotifications && (
                  <div className="absolute right-0 mt-2 w-80 sm:w-96 rounded-xl bg-white p-3 shadow-elevated border border-slate-200 z-50">
                    <div className="flex items-center justify-between pb-2 border-b border-slate-100 mb-2">
                      <h4 className="text-sm font-semibold text-slate-900">Notifications</h4>
                      {unreadCount > 0 && (
                        <button
                          onClick={markAllAsRead}
                          className="text-xs text-brand-600 hover:text-brand-700 font-medium"
                        >
                          Mark all read
                        </button>
                      )}
                    </div>
                    <div className="max-h-72 overflow-y-auto space-y-1">
                      {notifications.length === 0 ? (
                        <p className="text-xs text-slate-500 text-center py-6">No notifications yet.</p>
                      ) : (
                        notifications.slice(0, 6).map((n) => (
                          <div
                            key={n.id}
                            onClick={() => {
                              markAsRead(n.id);
                              if (n.link) navigate(n.link);
                              setShowNotifications(false);
                            }}
                            className={`p-2.5 rounded-lg text-xs cursor-pointer transition-colors ${
                              n.is_read ? 'bg-white hover:bg-slate-50' : 'bg-brand-50/60 hover:bg-brand-50'
                            }`}
                          >
                            <div className="flex items-start justify-between gap-1">
                              <p className="font-semibold text-slate-900">{n.title}</p>
                              {!n.is_read && <span className="w-2 h-2 rounded-full bg-brand-600 mt-1 flex-shrink-0" />}
                            </div>
                            <p className="text-slate-600 mt-0.5 line-clamp-2">{n.message}</p>
                          </div>
                        ))
                      )}
                    </div>
                    <div className="pt-2 border-t border-slate-100 text-center mt-2">
                      <Link
                        to="/notifications"
                        onClick={() => setShowNotifications(false)}
                        className="text-xs font-semibold text-brand-600 hover:text-brand-700"
                      >
                        View all notifications
                      </Link>
                    </div>
                  </div>
                )}
              </div>

              {/* User Avatar & Menu */}
              <div className="relative">
                <button
                  onClick={() => setShowUserMenu(!showUserMenu)}
                  className="flex items-center gap-2 p-1.5 rounded-lg hover:bg-slate-100 transition-colors"
                >
                  <Avatar name={profile?.full_name || user?.email || 'User'} size="sm" />
                  <span className="hidden sm:inline-block text-xs font-medium text-slate-800 max-w-[120px] truncate">
                    {profile?.full_name || user?.email}
                  </span>
                  <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
                </button>

                {showUserMenu && (
                  <div className="absolute right-0 mt-2 w-56 rounded-xl bg-white py-2 shadow-elevated border border-slate-200 z-50">
                    <div className="px-4 py-2 border-b border-slate-100">
                      <p className="text-xs font-semibold text-slate-900 truncate">{profile?.full_name}</p>
                      <p className="text-[11px] text-slate-500 truncate">{user?.email}</p>
                      <span className="inline-block mt-1 px-2 py-0.5 text-[10px] font-semibold rounded-full bg-brand-100 text-brand-700 capitalize">
                        {user?.role}
                      </span>
                    </div>

                    <Link
                      to="/profile/me"
                      onClick={() => setShowUserMenu(false)}
                      className="flex items-center gap-2.5 px-4 py-2 text-xs text-slate-700 hover:bg-slate-50"
                    >
                      <User className="w-4 h-4 text-slate-400" />
                      View My Profile
                    </Link>

                    <Link
                      to="/edit-profile"
                      onClick={() => setShowUserMenu(false)}
                      className="flex items-center gap-2.5 px-4 py-2 text-xs text-slate-700 hover:bg-slate-50"
                    >
                      <Sparkles className="w-4 h-4 text-slate-400" />
                      Edit Profile & Goals
                    </Link>

                    {user?.role === 'admin' && (
                      <Link
                        to="/admin"
                        onClick={() => setShowUserMenu(false)}
                        className="flex items-center gap-2.5 px-4 py-2 text-xs text-amber-700 bg-amber-50 hover:bg-amber-100"
                      >
                        <Shield className="w-4 h-4 text-amber-600" />
                        Admin Portal
                      </Link>
                    )}

                    <div className="border-t border-slate-100 my-1" />

                    <button
                      onClick={handleLogout}
                      className="w-full flex items-center gap-2.5 px-4 py-2 text-xs text-rose-600 hover:bg-rose-50 text-left"
                    >
                      <LogOut className="w-4 h-4" />
                      Sign Out
                    </button>
                  </div>
                )}
              </div>

            </div>
          )}
        </div>

      </div>
    </header>
  );
};
