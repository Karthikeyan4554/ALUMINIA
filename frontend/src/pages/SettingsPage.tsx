import React, { useState } from 'react';
import { Settings, Shield, Lock, Bell, CheckCircle2, AlertCircle } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { api } from '../services/api';

export const SettingsPage: React.FC = () => {
  const { user, profile, refreshProfile } = useAuth();

  const [hideContact, setHideContact] = useState(profile?.hide_contact_info !== false);
  const [isPublic, setIsPublic] = useState(profile?.is_public !== false);
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isSaving, setIsSaving] = useState(false);
  const [success, setSuccess] = useState(false);
  const [pwdSuccess, setPwdSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSavePrivacy = async () => {
    setIsSaving(true);
    setError(null);
    try {
      await api.updateMyProfile({
        hide_contact_info: hideContact,
        is_public: isPublic,
      });
      await refreshProfile();
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
    } catch (err: any) {
      setError(err.message || 'Failed to update privacy');
    } finally {
      setIsSaving(false);
    }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    if (newPassword !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    if (newPassword.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }

    try {
      if (user?.email) {
        await api.resetPassword({ email: user.email, new_password: newPassword });
        setPwdSuccess(true);
        setNewPassword('');
        setConfirmPassword('');
        setTimeout(() => setPwdSuccess(false), 3000);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to change password');
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6 pb-12 animate-fade-in">
      
      {/* Header Banner */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-subtle">
        <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
          <Settings className="w-6 h-6 text-brand-600" />
          Settings & Privacy Controls
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Manage your university profile visibility, notifications, and security credentials
        </p>
      </div>

      {success && (
        <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-800 font-semibold flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          Privacy preferences updated successfully.
        </div>
      )}

      {pwdSuccess && (
        <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-800 font-semibold flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          Password changed successfully.
        </div>
      )}

      {error && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-xs text-rose-800 font-semibold flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-rose-600" />
          {error}
        </div>
      )}

      {/* Privacy Settings */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-subtle space-y-5">
        <div className="flex items-center gap-2 pb-2 border-b border-slate-100">
          <Shield className="w-4 h-4 text-brand-600" />
          <h2 className="text-sm font-bold text-slate-900">Profile Visibility & Privacy</h2>
        </div>

        <div className="space-y-4 text-xs">
          <div className="flex items-center justify-between">
            <div>
              <p className="font-bold text-slate-900">Public Directory Visibility</p>
              <p className="text-slate-500">Allow other university students and alumni to discover your profile in search</p>
            </div>
            <input
              type="checkbox"
              checked={isPublic}
              onChange={(e) => setIsPublic(e.target.checked)}
              className="w-4 h-4 text-brand-600 rounded"
            />
          </div>

          <div className="flex items-center justify-between">
            <div>
              <p className="font-bold text-slate-900">Protect Contact Information</p>
              <p className="text-slate-500">Hide personal email address and phone number from unverified connections</p>
            </div>
            <input
              type="checkbox"
              checked={hideContact}
              onChange={(e) => setHideContact(e.target.checked)}
              className="w-4 h-4 text-brand-600 rounded"
            />
          </div>

          <div className="pt-2 flex justify-end">
            <button
              onClick={handleSavePrivacy}
              disabled={isSaving}
              className="px-4 py-2 rounded-xl text-xs font-bold text-white bg-brand-600 hover:bg-brand-700 shadow-sm transition-all"
            >
              {isSaving ? 'Saving...' : 'Update Privacy Settings'}
            </button>
          </div>
        </div>
      </div>

      {/* Change Password */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-subtle space-y-5">
        <div className="flex items-center gap-2 pb-2 border-b border-slate-100">
          <Lock className="w-4 h-4 text-brand-600" />
          <h2 className="text-sm font-bold text-slate-900">Change Password</h2>
        </div>

        <form onSubmit={handleChangePassword} className="space-y-4 text-xs">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">New Password</label>
              <input
                type="password"
                required
                minLength={6}
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none"
              />
            </div>
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Confirm New Password</label>
              <input
                type="password"
                required
                minLength={6}
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none"
              />
            </div>
          </div>

          <div className="flex justify-end">
            <button
              type="submit"
              className="px-4 py-2 rounded-xl text-xs font-bold text-white bg-slate-900 hover:bg-slate-800 shadow-sm transition-all"
            >
              Update Password
            </button>
          </div>
        </form>
      </div>

      {/* Account Info */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-subtle space-y-3 text-xs text-slate-500">
        <h3 className="font-bold text-slate-900">Platform & Version Information</h3>
        <p>Alumnia Web Application • Version 1.0.0 (Production Release)</p>
        <p>Current Account Role: <span className="font-bold text-brand-700 capitalize">{user?.role}</span></p>
        <p>Registered Email: <span className="font-bold text-slate-700">{user?.email}</span></p>
      </div>

    </div>
  );
};
