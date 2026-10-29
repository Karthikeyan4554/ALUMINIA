import React, { useState, useEffect, useRef } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { 
  MessageSquare, Send, Search, Check, CheckCheck, 
  User, Circle, Clock, ArrowLeft 
} from 'lucide-react';
import { Conversation, Message } from '../types';
import { api } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { Avatar } from '../components/Avatar';

export const MessagesPage: React.FC = () => {
  const { user: currentUser } = useAuth();
  const [searchParams] = useSearchParams();
  const targetUserId = searchParams.get('start_with');

  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversationId, setActiveConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [messageInput, setMessageInput] = useState('');
  const [searchFilter, setSearchFilter] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [isSending, setIsSending] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const fetchConversations = async () => {
    try {
      const data = await api.getConversations();
      setConversations(data);

      if (targetUserId) {
        // Start or retrieve conversation
        const res = await api.startConversation(targetUserId);
        setActiveConversationId(res.conversation_id);
      } else if (!activeConversationId && data.length > 0) {
        setActiveConversationId(data[0].id);
      }
    } catch (err) {
      console.error('Failed to load conversations', err);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchMessages = async (convId: string) => {
    try {
      const data = await api.getMessages(convId);
      setMessages(data);
    } catch (err) {
      console.error('Failed to load messages', err);
    }
  };

  useEffect(() => {
    fetchConversations();
  }, [targetUserId]);

  useEffect(() => {
    if (activeConversationId) {
      fetchMessages(activeConversationId);
      const interval = setInterval(() => fetchMessages(activeConversationId), 5000); // 5-second polling
      return () => clearInterval(interval);
    }
  }, [activeConversationId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!messageInput.trim() || !activeConversationId || isSending) return;

    const content = messageInput.trim();
    setMessageInput('');
    setIsSending(true);

    try {
      const newMsg = await api.sendMessage(activeConversationId, content);
      setMessages((prev) => [...prev, newMsg]);
      fetchConversations();
    } catch (err) {
      console.error('Failed to send message', err);
    } finally {
      setIsSending(false);
    }
  };

  const activeConv = conversations.find((c) => c.id === activeConversationId);
  const filteredConversations = conversations.filter((c) =>
    c.other_user?.full_name?.toLowerCase().includes(searchFilter.toLowerCase())
  );

  return (
    <div className="h-[calc(100vh-8.5rem)] bg-white rounded-2xl border border-slate-200 shadow-subtle overflow-hidden flex flex-col md:flex-row animate-fade-in">
      
      {/* Left Column: Conversations List */}
      <div className={`w-full md:w-80 border-r border-slate-200 flex flex-col bg-white ${activeConversationId ? 'hidden md:flex' : 'flex'}`}>
        
        {/* Header and Search */}
        <div className="p-4 border-b border-slate-200 space-y-3">
          <h2 className="text-sm font-bold text-slate-900 flex items-center gap-2">
            <MessageSquare className="w-4 h-4 text-brand-600" />
            Messages & Inquiries
          </h2>
          <div className="relative">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              value={searchFilter}
              onChange={(e) => setSearchFilter(e.target.value)}
              placeholder="Search conversations..."
              className="w-full text-xs pl-8 pr-3 py-2 rounded-xl border border-slate-200 bg-slate-50 focus:outline-none focus:ring-2 focus:ring-brand-500/20"
            />
          </div>
        </div>

        {/* Conversation List */}
        <div className="flex-1 overflow-y-auto divide-y divide-slate-100">
          {isLoading ? (
            <div className="p-4 space-y-3">
              {[1, 2, 3].map((i) => (
                <div key={i} className="flex items-center gap-3 animate-pulse">
                  <div className="w-10 h-10 rounded-full bg-slate-200" />
                  <div className="space-y-1.5 flex-1">
                    <div className="h-3 bg-slate-200 rounded w-1/2" />
                    <div className="h-2.5 bg-slate-100 rounded w-3/4" />
                  </div>
                </div>
              ))}
            </div>
          ) : filteredConversations.length === 0 ? (
            <div className="p-8 text-center text-xs text-slate-400 space-y-2">
              <p>No active conversations yet.</p>
              <Link to="/recommendations" className="text-brand-600 font-bold hover:underline block">
                Connect with Alumni →
              </Link>
            </div>
          ) : (
            filteredConversations.map((c) => {
              const isActive = c.id === activeConversationId;
              return (
                <button
                  key={c.id}
                  onClick={() => setActiveConversationId(c.id)}
                  className={`w-full p-3.5 flex items-start gap-3 text-left transition-colors ${
                    isActive ? 'bg-brand-50/70 border-l-4 border-brand-600' : 'hover:bg-slate-50'
                  }`}
                >
                  <Avatar
                    name={c.other_user?.full_name || 'User'}
                    size="sm"
                    className="rounded-full flex-shrink-0"
                  />
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center justify-between">
                      <p className="text-xs font-bold text-slate-900 truncate">
                        {c.other_user?.full_name}
                      </p>
                      {c.last_message && (
                        <span className="text-[10px] text-slate-400">
                          {new Date(c.last_message.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </span>
                      )}
                    </div>
                    <p className="text-[11px] text-slate-500 truncate mt-0.5">
                      {c.last_message?.content || 'No messages yet'}
                    </p>
                  </div>
                  {c.unread_count > 0 && (
                    <span className="w-4 h-4 rounded-full bg-brand-600 text-white text-[10px] font-bold flex items-center justify-center flex-shrink-0">
                      {c.unread_count}
                    </span>
                  )}
                </button>
              );
            })
          )}
        </div>

      </div>

      {/* Right Column: Chat History and Input */}
      <div className={`flex-1 flex flex-col bg-slate-50/40 ${!activeConversationId ? 'hidden md:flex' : 'flex'}`}>
        
        {activeConv ? (
          <>
            {/* Chat Header */}
            <div className="p-3.5 px-6 border-b border-slate-200 bg-white flex items-center justify-between">
              <div className="flex items-center gap-3">
                <button
                  onClick={() => setActiveConversationId(null)}
                  className="p-1.5 text-slate-500 hover:text-slate-900 md:hidden"
                >
                  <ArrowLeft className="w-5 h-5" />
                </button>
                <Link to={`/profile/${activeConv.other_user?.user_id}`}>
                  <Avatar
                    name={activeConv.other_user?.full_name || 'User'}
                    size="sm"
                    className="rounded-full"
                  />
                </Link>
                <div>
                  <Link
                    to={`/profile/${activeConv.other_user?.user_id}`}
                    className="font-bold text-slate-900 text-xs hover:text-brand-600 transition-colors block"
                  >
                    {activeConv.other_user?.full_name}
                  </Link>
                  <p className="text-[11px] text-slate-500">
                    {activeConv.other_user?.current_job_title} at {activeConv.other_user?.current_company || 'University'}
                  </p>
                </div>
              </div>

              <Link
                to={`/profile/${activeConv.other_user?.user_id}`}
                className="px-3 py-1.5 text-xs font-semibold rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-slate-700"
              >
                View Profile
              </Link>
            </div>

            {/* Messages Feed */}
            <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-3.5">
              {messages.length === 0 ? (
                <div className="text-center py-12 space-y-2">
                  <p className="text-xs text-slate-500">Start the conversation by sending a polite introduction.</p>
                  <p className="text-[11px] text-slate-400">Mention common skills or alumni background.</p>
                </div>
              ) : (
                messages.map((m) => {
                  const isMine = m.sender_id === currentUser?.id;
                  return (
                    <div
                      key={m.id}
                      className={`flex flex-col ${isMine ? 'items-end' : 'items-start'}`}
                    >
                      <div
                        className={`max-w-[75%] rounded-2xl p-3 text-xs leading-relaxed ${
                          isMine
                            ? 'bg-brand-600 text-white rounded-tr-none'
                            : 'bg-white border border-slate-200/90 text-slate-800 rounded-tl-none shadow-subtle'
                        }`}
                      >
                        <p className="whitespace-pre-wrap">{m.content}</p>
                      </div>
                      <span className="text-[10px] text-slate-400 mt-1 px-1 flex items-center gap-1">
                        {new Date(m.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        {isMine && <CheckCheck className="w-3 h-3 text-brand-600" />}
                      </span>
                    </div>
                  );
                })
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Input Bar */}
            <div className="p-4 bg-white border-t border-slate-200">
              <form onSubmit={handleSendMessage} className="flex items-center gap-2">
                <input
                  type="text"
                  value={messageInput}
                  onChange={(e) => setMessageInput(e.target.value)}
                  placeholder="Type your message here..."
                  className="flex-1 text-xs p-3 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/30 focus:border-brand-500"
                />
                <button
                  type="submit"
                  disabled={!messageInput.trim() || isSending}
                  className="p-3 rounded-xl bg-brand-600 text-white hover:bg-brand-700 transition-colors shadow-sm disabled:opacity-50"
                >
                  <Send className="w-4 h-4" />
                </button>
              </form>
            </div>
          </>
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center p-8 text-center text-slate-400">
            <MessageSquare className="w-12 h-12 text-slate-300 mb-2" />
            <h3 className="text-sm font-bold text-slate-700">No Conversation Selected</h3>
            <p className="text-xs text-slate-500 max-w-xs mt-1">
              Select an ongoing thread from the sidebar or reach out to alumni from recommendations.
            </p>
          </div>
        )}

      </div>

    </div>
  );
};
