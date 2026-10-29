import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { GraduationCap, Lock, Mail, ArrowRight, AlertCircle, Sparkles } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const LoginPage: React.FC = () => {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    try {
      await login({ email, password });
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Invalid email or password');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDemoFill = async (demoEmail: string, role: string) => {
    setEmail(demoEmail);
    setPassword('Password123!');
    setIsLoading(true);
    setError(null);
    try {
      await login({ email: demoEmail, password: 'Password123!' });
      navigate(role === 'admin' ? '/admin' : '/dashboard');
    } catch (err: any) {
      setError(err.message || 'Demo login failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center py-12 px-4">
      <div className="max-w-md w-full bg-white p-8 rounded-2xl border border-slate-200/90 shadow-elevated">
        
        <div className="text-center mb-6">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-brand-700 to-indigo-500 text-white flex items-center justify-center mx-auto shadow-md shadow-brand-500/20 mb-3">
            <GraduationCap className="w-6 h-6" />
          </div>
          <h2 className="text-2xl font-extrabold text-slate-900 tracking-tight">
            Sign In to Alumnia
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Access your personalized alumni recommendation feed
          </p>
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-xl bg-rose-50 border border-rose-200 text-xs text-rose-700 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Email Address
            </label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="student@alumnia.edu"
                className="w-full text-xs pl-9 pr-3 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/30 focus:border-brand-500"
              />
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-1">
              <label className="block text-xs font-semibold text-slate-700">
                Password
              </label>
              <Link to="/forgot-password" className="text-[11px] font-semibold text-brand-600 hover:text-brand-700">
                Forgot password?
              </Link>
            </div>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••••••"
                className="w-full text-xs pl-9 pr-3 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/30 focus:border-brand-500"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-2.5 px-4 rounded-xl text-xs font-bold text-white bg-brand-600 hover:bg-brand-700 shadow-sm flex items-center justify-center gap-2 transition-all disabled:opacity-60"
          >
            {isLoading ? 'Signing In...' : 'Sign In'}
            <ArrowRight className="w-4 h-4" />
          </button>
        </form>

        {/* Demo Fast-Login Pill Tray */}
        <div className="mt-6 pt-5 border-t border-slate-100 text-center">
          <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-2.5">
            Instant Demo Logins
          </p>
          <div className="grid grid-cols-3 gap-2">
            <button
              type="button"
              onClick={() => handleDemoFill('student@alumnia.edu', 'student')}
              className="p-2 rounded-lg bg-slate-50 hover:bg-brand-50 text-[11px] font-semibold text-slate-700 hover:text-brand-700 border border-slate-200 transition-colors"
            >
              🎓 Student
            </button>
            <button
              type="button"
              onClick={() => handleDemoFill('deepa.subramanian@alumni.edu', 'alumni')}
              className="p-2 rounded-lg bg-slate-50 hover:bg-indigo-50 text-[11px] font-semibold text-slate-700 hover:text-indigo-700 border border-slate-200 transition-colors"
            >
              💼 Alumni
            </button>
            <button
              type="button"
              onClick={() => handleDemoFill('admin@alumnia.edu', 'admin')}
              className="p-2 rounded-lg bg-slate-50 hover:bg-amber-50 text-[11px] font-semibold text-slate-700 hover:text-amber-700 border border-slate-200 transition-colors"
            >
              🛡️ Admin
            </button>
          </div>
        </div>

        <div className="mt-6 text-center text-xs text-slate-500">
          Don't have an account yet?{' '}
          <Link to="/register" className="font-bold text-brand-600 hover:text-brand-700">
            Create an Account
          </Link>
        </div>

      </div>
    </div>
  );
};
