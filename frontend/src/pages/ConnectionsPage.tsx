import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  UserCheck, UserPlus, Clock, MessageSquare, 
  Trash2, Check, X, Shield, Users, Building, MapPin 
} from 'lucide-react';
import { Profile } from '../types';
import { api } from '../services/api';
import { Avatar } from '../components/Avatar';

export const ConnectionsPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'connected' | 'incoming' | 'outgoing'>('connected');
  const [connections, setConnections] = useState<Profile[]>([]);
  const [incomingRequests, setIncomingRequests] = useState<any[]>([]);
  const [outgoingRequests, setOutgoingRequests] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchData = async () => {
    setIsLoading(true);
    try {
      const [conns, reqs] = await Promise.all([
        api.getConnections(),
        api.getConnectionRequests(),
      ]);
      setConnections(conns);
      setIncomingRequests(reqs.incoming || []);
      setOutgoingRequests(reqs.outgoing || []);
    } catch (err) {
      console.error('Failed to load connections', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleAccept = async (reqId: string) => {
    try {
      await api.acceptConnectionRequest(reqId);
      fetchData();
    } catch (err) {
      console.error('Failed to accept request', err);
    }
  };

  const handleReject = async (reqId: string) => {
    try {
      await api.rejectConnectionRequest(reqId);
      fetchData();
    } catch (err) {
      console.error('Failed to reject request', err);
    }
  };

  const handleCancel = async (reqId: string) => {
    try {
      await api.cancelConnectionRequest(reqId);
      fetchData();
    } catch (err) {
      console.error('Failed to cancel request', err);
    }
  };

  const handleRemoveConnection = async (userId: string) => {
    if (!window.confirm('Are you sure you want to remove this connection?')) return;
    try {
      await api.removeConnection(userId);
      fetchData();
    } catch (err) {
      console.error('Failed to remove connection', err);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      
      {/* Top Banner */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-subtle flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <UserCheck className="w-6 h-6 text-brand-600" />
            My Alumni Network
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Manage your university relationships, pending invitations, and active contacts
          </p>
        </div>

        <Link
          to="/recommendations"
          className="px-4 py-2 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-bold text-xs shadow-sm flex items-center gap-1.5 transition-all"
        >
          <UserPlus className="w-4 h-4" />
          Find New Connections
        </Link>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-200 pb-2 text-xs font-bold">
        <button
          onClick={() => setActiveTab('connected')}
          className={`px-4 py-2 rounded-xl transition-all ${
            activeTab === 'connected'
              ? 'bg-brand-600 text-white shadow-sm'
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          Active Connections ({connections.length})
        </button>
        <button
          onClick={() => setActiveTab('incoming')}
          className={`px-4 py-2 rounded-xl transition-all flex items-center gap-1.5 ${
            activeTab === 'incoming'
              ? 'bg-brand-600 text-white shadow-sm'
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          Incoming Requests
          {incomingRequests.length > 0 && (
            <span className={`w-5 h-5 rounded-full text-[10px] flex items-center justify-center font-bold ${
              activeTab === 'incoming' ? 'bg-white text-brand-700' : 'bg-brand-100 text-brand-700'
            }`}>
              {incomingRequests.length}
            </span>
          )}
        </button>
        <button
          onClick={() => setActiveTab('outgoing')}
          className={`px-4 py-2 rounded-xl transition-all ${
            activeTab === 'outgoing'
              ? 'bg-brand-600 text-white shadow-sm'
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          Sent Invitations ({outgoingRequests.length})
        </button>
      </div>

      {/* Content */}
      {isLoading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 py-6">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-40 rounded-2xl bg-white border border-slate-200 animate-pulse p-4" />
          ))}
        </div>
      ) : activeTab === 'connected' ? (
        connections.length === 0 ? (
          <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center space-y-3">
            <Users className="w-10 h-10 text-slate-300 mx-auto" />
            <h3 className="text-base font-bold text-slate-900">No Connections Yet</h3>
            <p className="text-xs text-slate-500 max-w-sm mx-auto">
              Start building your university network by connecting with recommended alumni.
            </p>
            <Link to="/recommendations" className="inline-block mt-2 px-4 py-2 text-xs font-bold text-white bg-brand-600 rounded-xl">
              Browse AI Recommendations
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {connections.map((p) => (
              <div
                key={p.user_id}
                className="bg-white rounded-2xl border border-slate-200 p-5 shadow-subtle hover:shadow-premium transition-all flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-start gap-3">
                    <Link to={`/profile/${p.user_id}`}>
                      <Avatar
                        name={p.full_name}
                        size="md"
                        className="rounded-xl"
                      />
                    </Link>
                    <div className="min-w-0 flex-1">
                      <Link to={`/profile/${p.user_id}`} className="font-bold text-slate-900 text-xs hover:text-brand-600 truncate block">
                        {p.full_name}
                      </Link>
                      <p className="text-[11px] text-brand-700 font-semibold truncate">
                        {p.current_job_title || p.department}
                      </p>
                      <p className="text-[11px] text-slate-400 truncate">
                        {p.current_company || 'Apex University'}
                      </p>
                    </div>
                  </div>
                </div>

                <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between gap-2">
                  <Link
                    to={`/messages?start_with=${p.user_id}`}
                    className="flex-1 py-1.5 rounded-lg bg-brand-50 hover:bg-brand-100 text-brand-700 font-bold text-xs flex items-center justify-center gap-1 transition-colors"
                  >
                    <MessageSquare className="w-3.5 h-3.5" /> Message
                  </Link>
                  <button
                    onClick={() => handleRemoveConnection(p.user_id)}
                    className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
                    title="Remove connection"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )
      ) : activeTab === 'incoming' ? (
        incomingRequests.length === 0 ? (
          <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center text-xs text-slate-500">
            No incoming connection invitations.
          </div>
        ) : (
          <div className="space-y-3">
            {incomingRequests.map((req) => (
              <div
                key={req.id}
                className="bg-white rounded-2xl border border-slate-200 p-4 shadow-subtle flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4"
              >
                <div className="flex items-center gap-3 min-w-0">
                  <Avatar
                    name={req.sender_profile?.full_name || 'User'}
                    size="md"
                    className="rounded-full flex-shrink-0"
                  />
                  <div className="min-w-0">
                    <p className="font-bold text-slate-900 text-xs">{req.sender_profile?.full_name}</p>
                    <p className="text-[11px] text-slate-600">{req.sender_profile?.current_job_title} at {req.sender_profile?.current_company}</p>
                    {req.message && (
                      <p className="text-[11px] text-slate-500 italic mt-0.5">"{req.message}"</p>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-2 w-full sm:w-auto">
                  <button
                    onClick={() => handleAccept(req.id)}
                    className="flex-1 sm:flex-none px-4 py-2 rounded-xl bg-brand-600 text-white font-bold text-xs hover:bg-brand-700 transition-colors flex items-center justify-center gap-1"
                  >
                    <Check className="w-3.5 h-3.5" /> Accept
                  </button>
                  <button
                    onClick={() => handleReject(req.id)}
                    className="flex-1 sm:flex-none px-4 py-2 rounded-xl border border-slate-200 text-slate-700 font-semibold text-xs hover:bg-slate-50 transition-colors"
                  >
                    Decline
                  </button>
                </div>
              </div>
            ))}
          </div>
        )
      ) : (
        outgoingRequests.length === 0 ? (
          <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center text-xs text-slate-500">
            No outgoing connection invitations pending.
          </div>
        ) : (
          <div className="space-y-3">
            {outgoingRequests.map((req) => (
              <div
                key={req.id}
                className="bg-white rounded-2xl border border-slate-200 p-4 shadow-subtle flex items-center justify-between gap-4"
              >
                <div className="flex items-center gap-3 min-w-0">
                  <Avatar
                    name={req.receiver_profile?.full_name || 'User'}
                    size="sm"
                    className="rounded-full flex-shrink-0"
                  />
                  <div className="min-w-0">
                    <p className="font-bold text-slate-900 text-xs">{req.receiver_profile?.full_name}</p>
                    <p className="text-[11px] text-slate-500">
                      {req.receiver_profile?.current_job_title} at {req.receiver_profile?.current_company}
                    </p>
                  </div>
                </div>

                <button
                  onClick={() => handleCancel(req.id)}
                  className="px-3 py-1.5 rounded-lg border border-slate-200 text-slate-600 hover:bg-slate-50 font-semibold text-xs transition-colors"
                >
                  Withdraw Request
                </button>
              </div>
            ))}
          </div>
        )
      )}

    </div>
  );
};
