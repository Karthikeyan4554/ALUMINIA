import React from 'react';
import { GraduationCap, Award, CheckCircle, Code2, Database, Cpu } from 'lucide-react';

export const AboutPage: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto py-10 px-4 space-y-10">
      <div className="text-center max-w-2xl mx-auto space-y-3">
        <div className="w-12 h-12 rounded-2xl bg-brand-600 text-white flex items-center justify-center mx-auto shadow-md">
          <GraduationCap className="w-6 h-6" />
        </div>
        <h1 className="text-3xl font-extrabold text-slate-900">
          About Alumnia
        </h1>
        <p className="text-sm text-slate-600">
          College Final-Year Project: Generative AI Based Alumni Networking Platform with Personalized Connection Recommendations.
        </p>
      </div>

      <div className="bg-white rounded-2xl border border-slate-200 p-8 shadow-subtle space-y-6 text-xs text-slate-600 leading-relaxed">
        <div>
          <h2 className="text-sm font-bold text-slate-900 mb-2">Project Mission</h2>
          <p>
            Alumnia was created to address a critical disconnect in higher education: while universities have thousands of successful alumni across leading industries, current undergraduates often struggle to discover relevant mentors, understand target career requirements, or initiate professional conversations without friction.
          </p>
        </div>

        <div>
          <h2 className="text-sm font-bold text-slate-900 mb-2">Technical Innovation</h2>
          <p>
            By combining multi-factor scoring with TF-IDF and cosine vector similarity, Alumnia identifies high-compatibility student-alumni pairs and provides transparent, natural-language explanations for every match. The integrated AI assistant assists students in articulating professional objectives and preparing for industry interviews.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t border-slate-100">
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
            <div className="flex items-center gap-1.5 font-bold text-slate-900">
              <Code2 className="w-4 h-4 text-brand-600" /> Frontend
            </div>
            <p className="text-[11px] text-slate-500">React 18, TypeScript, Vite, Tailwind CSS, Lucide Icons, Recharts, React Router.</p>
          </div>
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
            <div className="flex items-center gap-1.5 font-bold text-slate-900">
              <Cpu className="w-4 h-4 text-brand-600" /> Backend
            </div>
            <p className="text-[11px] text-slate-500">Python FastAPI, Pydantic, Scikit-learn Vectorizer, PyJWT, Bcrypt.</p>
          </div>
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
            <div className="flex items-center gap-1.5 font-bold text-slate-900">
              <Database className="w-4 h-4 text-brand-600" /> Database & Security
            </div>
            <p className="text-[11px] text-slate-500">PostgreSQL / SQLite Dual Engine, Row-Level Security, Normalized Schema.</p>
          </div>
        </div>
      </div>
    </div>
  );
};
