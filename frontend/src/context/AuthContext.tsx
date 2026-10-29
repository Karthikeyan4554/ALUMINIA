import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User, Profile } from '../types';
import { api } from '../services/api';

interface AuthContextType {
  user: User | null;
  profile: Profile | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: any) => Promise<void>;
  register: (data: any) => Promise<void>;
  logout: () => void;
  refreshProfile: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [profile, setProfile] = useState<Profile | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('alumnia_token'));
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const refreshProfile = async () => {
    try {
      const data = await api.getMyProfile();
      setProfile(data);
      if (user) {
        setUser({
          ...user,
          full_name: data.full_name,
          avatar_url: data.avatar_url,
          role: data.role,
        });
      }
    } catch (err) {
      console.error('[Auth] Failed to refresh profile:', err);
    }
  };

  useEffect(() => {
    const initializeAuth = async () => {
      const savedToken = localStorage.getItem('alumnia_token');
      if (savedToken) {
        try {
          const meData = await api.getMe();
          setUser({
            id: meData.id,
            email: meData.email,
            role: meData.role,
            full_name: meData.profile?.full_name,
            avatar_url: meData.profile?.avatar_url,
          });
          const fullProfile = await api.getMyProfile();
          setProfile(fullProfile);
        } catch (err) {
          console.warn('[Auth] Token invalid or expired, clearing session.');
          localStorage.removeItem('alumnia_token');
          setToken(null);
          setUser(null);
          setProfile(null);
        }
      }
      setIsLoading(false);
    };

    initializeAuth();
  }, []);

  const login = async (credentials: any) => {
    setIsLoading(true);
    try {
      const res = await api.login(credentials);
      localStorage.setItem('alumnia_token', res.access_token);
      setToken(res.access_token);
      setUser(res.user);
      const fullProfile = await api.getMyProfile();
      setProfile(fullProfile);
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (data: any) => {
    setIsLoading(true);
    try {
      const res = await api.register(data);
      localStorage.setItem('alumnia_token', res.access_token);
      setToken(res.access_token);
      setUser(res.user);
      const fullProfile = await api.getMyProfile();
      setProfile(fullProfile);
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('alumnia_token');
    setToken(null);
    setUser(null);
    setProfile(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        profile,
        token,
        isAuthenticated: !!token && !!user,
        isLoading,
        login,
        register,
        logout,
        refreshProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
