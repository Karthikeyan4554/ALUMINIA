import React, { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Bot, Send, Sparkles, User, Copy, Check, 
  ArrowRight, Building, Award, MessageSquare, Compass, RefreshCw, 
  MapPin, ExternalLink, UserPlus, GraduationCap
} from 'lucide-react';
import { api } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { ConnectModal } from '../components/ConnectModal';
import { MentorshipModal } from '../components/MentorshipModal';

interface ChatMessage {
  id: string;
  sender: 'user' | 'assistant';
  content: string;
  suggested_actions?: string[];
  recommended_alumni?: any[];
  is_llm_generated?: boolean;
}

export const AssistantPage: React.FC = () => {
  const { user, profile } = useAuth();
  const isAlumni = user?.role === 'alumni';

  const defaultStudentPrompts = [
    'Find alumni in Aerospace & Defense (ISRO, DRDO)',
    'Find alumni working in artificial intelligence',
    'Show alumni in Robotics & Industrial Automation',
    'Find mentors in VLSI & Semiconductor Design',
    'Recommend alumni in Automotive & Electric Vehicles',
    'Find alumni in Biomedical & Medical Electronics',
    'Which alumni can guide me in cloud computing?',
    'Recommend three alumni for my Generative AI project',
    'Find alumni in Chennai who work in software development',
    'Which skills should I learn for Embedded Systems & IoT?',
    'Help me write a message requesting mentorship',
    'Find alumni with experience in cybersecurity',
  ];

  const defaultAlumniPrompts = [
    'Show students interested in Aerospace & Robotics who need mentorship',
    'Find students interested in Artificial Intelligence and VLSI',
    'Review student career interests and engineering skill gaps',
    'Show students from Bannari Amman Institute of Technology seeking guidance',
  ];

  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      sender: 'assistant',
      content: isAlumni
        ? `Vanakkam ${profile?.full_name?.split(' ')[0] || 'Alumnus'}! I am your AI Networking Assistant on Alumnia.\n\nI can help you discover ambitious students looking for guidance in your engineering industry, review student skill interests, and prepare structured mentorship discussion outlines. What can I help you explore today?`
        : `Vanakkam ${profile?.full_name?.split(' ')[0] || 'there'}! I am your AI Networking Assistant on Alumnia.\n\nI am connected directly to our verified alumni database of 70+ industry professionals across 20+ engineering disciplines from Bannari Amman Institute of Technology and leading organizations across Tamil Nadu.\n\nI can help you discover mentors, analyze skill gaps for your dream job, recommend alumni for your college project, and draft tailored connection notes. What would you like to explore today?`,
      suggested_actions: isAlumni ? defaultAlumniPrompts.slice(0, 4) : defaultStudentPrompts.slice(0, 4),
      is_llm_generated: false,
    },
  ]);

  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  // Modals for direct connect / mentorship from chat cards
  const [connectTarget, setConnectTarget] = useState<any | null>(null);
  const [mentorTarget, setMentorTarget] = useState<any | null>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (textToSend: string) => {
    const text = textToSend.trim();
    if (!text || isLoading) return;

    const userMsg: ChatMessage = {
      id: String(Date.now()),
      sender: 'user',
      content: text,
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const res = await api.chatWithAssistant({
        message: text,
        history: messages.slice(-4).map((m) => ({
          role: m.sender === 'user' ? 'user' : 'assistant',
          content: m.content,
        })),
      });

      const assistantMsg: ChatMessage = {
        id: String(Date.now() + 1),
        sender: 'assistant',
        content: res.response,
        suggested_actions: res.suggested_actions,
        recommended_alumni: res.recommended_alumni,
        is_llm_generated: res.is_llm_generated,
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          id: String(Date.now() + 1),
          sender: 'assistant',
          content: 'Sorry, I encountered an issue retrieving verified database records. Please try again with a specific skill, industry, or role query.',
          is_llm_generated: false,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopy = (id: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(input);
    }
  };

  return (
    <div className="max-w-4xl mx-auto h-[calc(100vh-8.5rem)] flex flex-col bg-white rounded-2xl border border-slate-200 shadow-subtle overflow-hidden animate-fade-in">
      
      {/* Header */}
      <div className="p-4 border-b border-slate-200 bg-white flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 to-indigo-600 text-white flex items-center justify-center shadow-sm">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              AI Career &amp; Networking Assistant
              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                Database Grounded
              </span>
            </h2>
            <p className="text-[11px] text-slate-500">
              Personalized career guidance grounded in verified student &amp; alumni profiles from Bannari Amman Institute of Technology
            </p>
          </div>
        </div>

        <button
          onClick={() => setMessages(messages.slice(0, 1))}
          className="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors"
          title="Reset Conversation"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>New Chat</span>
        </button>
      </div>

      {/* Suggested Quick Prompts Bar */}
      <div className="px-4 py-2.5 bg-slate-50 border-b border-slate-200 flex items-center gap-2 overflow-x-auto text-xs">
        <span className="text-slate-400 font-bold whitespace-nowrap text-[11px]">Suggested Queries:</span>
        {(isAlumni ? defaultAlumniPrompts : defaultStudentPrompts).map((prompt) => (
          <button
            key={prompt}
            onClick={() => sendMessage(prompt)}
            className="px-2.5 py-1 rounded-lg bg-white border border-slate-200 text-slate-700 hover:bg-brand-50 hover:border-brand-200 hover:text-brand-700 font-medium whitespace-nowrap transition-colors flex-shrink-0 shadow-2xs"
          >
            {prompt}
          </button>
        ))}
      </div>

      {/* Message History Thread */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-5">
        {messages.map((m) => (
          <div
            key={m.id}
            className={`flex items-start gap-3 ${m.sender === 'user' ? 'flex-row-reverse' : ''}`}
          >
            <div
              className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 text-white shadow-sm ${
                m.sender === 'user'
                  ? 'bg-slate-800'
                  : 'bg-gradient-to-tr from-brand-600 to-indigo-600'
              }`}
            >
              {m.sender === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
            </div>

            <div
              className={`max-w-[85%] rounded-2xl p-4 text-xs leading-relaxed space-y-3 shadow-subtle ${
                m.sender === 'user'
                  ? 'bg-brand-600 text-white rounded-tr-none'
                  : 'bg-slate-50 text-slate-800 border border-slate-200/80 rounded-tl-none'
              }`}
            >
              <div className="whitespace-pre-wrap font-sans text-xs leading-relaxed">{m.content}</div>

              {/* Embedded Alumni Recommendation Mini-Cards */}
              {m.recommended_alumni && m.recommended_alumni.length > 0 && (
                <div className="pt-3 border-t border-slate-200/80 space-y-2">
                  <p className="text-[11px] font-bold text-slate-500 uppercase tracking-wider">
                    Matching Profiles Retrieved:
                  </p>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                    {m.recommended_alumni.map((a: any) => (
                      <div
                        key={a.id || a.user_id || a.name}
                        className="p-3 rounded-xl bg-white border border-slate-200 text-[11px] space-y-2 shadow-2xs hover:border-brand-300 transition-all flex flex-col justify-between"
                      >
                        <div>
                          <div className="flex items-start justify-between gap-1">
                            <Link
                              to={`/profile/${a.user_id}`}
                              className="font-bold text-slate-900 hover:text-brand-600 transition-colors flex items-center gap-1"
                            >
                              {a.name}
                              <ExternalLink className="w-3 h-3 text-slate-400" />
                            </Link>
                            {a.mentorship && (
                              <span className="inline-block px-1.5 py-0.5 rounded bg-amber-50 text-amber-700 font-bold text-[10px] border border-amber-200 whitespace-nowrap">
                                ★ Mentor
                              </span>
                            )}
                          </div>

                          <p className="text-slate-600 flex items-center gap-1 mt-0.5 font-medium">
                            <Building className="w-3 h-3 text-slate-400 flex-shrink-0" />
                            <span className="truncate">{a.title} {a.company ? `• ${a.company}` : ''}</span>
                          </p>

                          {a.location && (
                            <p className="text-slate-500 flex items-center gap-1 text-[10px]">
                              <MapPin className="w-3 h-3 text-slate-400 flex-shrink-0" />
                              <span className="truncate">{a.location}</span>
                            </p>
                          )}

                          {a.skills && a.skills.length > 0 && (
                            <div className="flex flex-wrap gap-1 mt-1.5">
                              {a.skills.slice(0, 3).map((sk: string) => (
                                <span
                                  key={sk}
                                  className="px-1.5 py-0.5 rounded text-[10px] bg-slate-100 text-slate-600 font-medium"
                                >
                                  {sk}
                                </span>
                              ))}
                            </div>
                          )}
                        </div>

                        {/* Interactive In-App Profile Actions */}
                        <div className="pt-2 border-t border-slate-100 flex items-center justify-between gap-2">
                          <Link
                            to={`/profile/${a.user_id}`}
                            className="text-brand-600 hover:text-brand-700 font-semibold text-[10px] flex items-center gap-0.5"
                          >
                            View Profile →
                          </Link>

                          {a.user_id && (
                            <button
                              onClick={() => setConnectTarget({
                                profile: {
                                  id: a.id,
                                  user_id: a.user_id,
                                  full_name: a.name,
                                  current_job_title: a.title,
                                  current_company: a.company
                                },
                                starter: `Hi ${a.name.split(' ')[0]}, I discovered your profile through Alumnia's AI assistant and would love to connect!`
                              })}
                              className="px-2 py-1 rounded bg-brand-50 hover:bg-brand-100 text-brand-700 font-bold text-[10px] border border-brand-200 transition-colors"
                            >
                              Connect
                            </button>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Action Buttons / Copy */}
              {m.sender === 'assistant' && (
                <div className="flex items-center justify-between pt-2 border-t border-slate-200 text-[10px] text-slate-400">
                  <span className="flex items-center gap-1">
                    <Sparkles className="w-3 h-3 text-brand-500" />
                    Verified from Platform Database
                  </span>
                  <button
                    onClick={() => handleCopy(m.id, m.content)}
                    className="flex items-center gap-1 font-semibold text-brand-600 hover:text-brand-700 transition-colors"
                  >
                    {copiedId === m.id ? <Check className="w-3 h-3 text-emerald-600" /> : <Copy className="w-3 h-3" />}
                    {copiedId === m.id ? 'Copied' : 'Copy Response'}
                  </button>
                </div>
              )}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-brand-600 text-white flex items-center justify-center shadow-sm">
              <Bot className="w-4 h-4 animate-spin" />
            </div>
            <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200 text-xs text-slate-500 rounded-tl-none flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-brand-600 animate-ping"></span>
              Querying database and computing recommendations...
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Chat Input Bar */}
      <div className="p-3.5 border-t border-slate-200 bg-white">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            sendMessage(input);
          }}
          className="flex items-end gap-2"
        >
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
            placeholder={
              isAlumni
                ? "Ask anything: 'Show students interested in web development', 'Review student career interests'..."
                : "Ask anything: 'Find alumni in AI', 'Which skills should I learn for Data Science?', 'Recommend mentors for cloud in Chennai'..."
            }
            className="flex-1 text-xs p-3 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/30 focus:border-brand-500 resize-none max-h-32"
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="p-3 rounded-xl bg-brand-600 text-white hover:bg-brand-700 transition-colors shadow-sm disabled:opacity-50 flex-shrink-0 font-semibold"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
        <p className="text-[10px] text-slate-400 mt-1.5 text-center">
          Press <kbd className="px-1 py-0.5 rounded bg-slate-100 font-mono text-[9px] text-slate-600">Enter</kbd> to send, <kbd className="px-1 py-0.5 rounded bg-slate-100 font-mono text-[9px] text-slate-600">Shift + Enter</kbd> for a new line
        </p>
      </div>

      {/* Interactive Connect Modal */}
      <ConnectModal
        isOpen={!!connectTarget}
        target={connectTarget}
        onClose={() => setConnectTarget(null)}
        onSuccess={() => {
          if (connectTarget) {
            const name = connectTarget.profile.full_name;
            setConnectTarget(null);
            setMessages((prev) => [
              ...prev,
              {
                id: String(Date.now()),
                sender: 'assistant',
                content: `Success! Your connection request has been sent to ${name}. You can track the status in the Connections tab.`,
                is_llm_generated: false,
              }
            ]);
          }
        }}
      />

      {/* Interactive Mentorship Modal */}
      <MentorshipModal
        isOpen={!!mentorTarget}
        mentor={mentorTarget}
        onClose={() => setMentorTarget(null)}
        onSuccess={() => {
          if (mentorTarget) {
            const name = mentorTarget.full_name;
            setMentorTarget(null);
            setMessages((prev) => [
              ...prev,
              {
                id: String(Date.now()),
                sender: 'assistant',
                content: `Success! Your mentorship application has been submitted to ${name}.`,
                is_llm_generated: false,
              }
            ]);
          }
        }}
      />

    </div>
  );
};
