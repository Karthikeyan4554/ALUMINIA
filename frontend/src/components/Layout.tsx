import React, { useState } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import { Navbar } from './Navbar';
import { Sidebar } from './Sidebar';
import { useAuth } from '../context/AuthContext';

export const Layout: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { isAuthenticated } = useAuth();
  const location = useLocation();

  // Public pages without sidebar
  const publicPaths = ['/', '/features', '/about', '/login', '/register', '/forgot-password', '/onboarding'];
  const isPublicPage = publicPaths.includes(location.pathname);

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      <Navbar onToggleSidebar={() => setSidebarOpen(!sidebarOpen)} />

      <div className="flex-1 flex">
        {isAuthenticated && !isPublicPage && (
          <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
        )}

        <main
          className={`flex-1 transition-all duration-200 ${
            isAuthenticated && !isPublicPage ? 'lg:pl-64' : ''
          }`}
        >
          <div className="p-4 sm:p-6 lg:p-8 max-w-7xl mx-auto w-full animate-fade-in">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};
