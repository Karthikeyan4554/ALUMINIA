import React, { useState, useEffect } from 'react';
import { 
  Calendar, MapPin, Clock, Users, ExternalLink, 
  Plus, CheckCircle2, Video, X 
} from 'lucide-react';
import { AlumniEvent } from '../types';
import { api } from '../services/api';
import { useAuth } from '../context/AuthContext';

export const EventsPage: React.FC = () => {
  const { user } = useAuth();
  const [events, setEvents] = useState<AlumniEvent[]>([]);
  const [eventTypeFilter, setEventTypeFilter] = useState('All');
  const [isLoading, setIsLoading] = useState(true);

  // Create Event Modal
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newEvent, setNewEvent] = useState({
    title: '',
    event_type: 'Webinar',
    description: '',
    location: 'Virtual / Zoom',
    is_virtual: true,
    virtual_meeting_link: 'https://meet.google.com/alm-evt-2026',
    start_time: new Date(Date.now() + 86400000 * 3).toISOString().slice(0, 16),
    end_time: new Date(Date.now() + 86400000 * 3 + 7200000).toISOString().slice(0, 16),
    capacity: 200,
  });

  const fetchEvents = async () => {
    setIsLoading(true);
    try {
      const data = await api.getEvents({
        event_type: eventTypeFilter !== 'All' ? eventTypeFilter : undefined,
      });
      setEvents(data);
    } catch (err) {
      console.error('Failed to load events', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchEvents();
  }, [eventTypeFilter]);

  const handleRegister = async (eventId: string) => {
    try {
      await api.registerForEvent(eventId);
      fetchEvents();
    } catch (err) {
      console.error('Failed to register for event', err);
    }
  };

  const handleCancelRegistration = async (eventId: string) => {
    try {
      await api.cancelEventRegistration(eventId);
      fetchEvents();
    } catch (err) {
      console.error('Failed to cancel event registration', err);
    }
  };

  const handleCreateSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.createEvent({
        ...newEvent,
        start_time: new Date(newEvent.start_time).toISOString(),
        end_time: new Date(newEvent.end_time).toISOString(),
      });
      setShowCreateModal(false);
      fetchEvents();
    } catch (err) {
      console.error('Failed to create event', err);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      
      {/* Header Banner */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-subtle flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-50 border border-indigo-200 text-indigo-800 text-xs font-bold mb-2">
            <Calendar className="w-3.5 h-3.5 text-indigo-600" />
            University Events & Tech Talks
          </div>
          <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">
            Alumni Events & Technical Workshops
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Participate in interactive alumni panels, coding bootcamps, and career preparation masterclasses
          </p>
        </div>

        {(user?.role === 'alumni' || user?.role === 'admin') && (
          <button
            onClick={() => setShowCreateModal(true)}
            className="px-4 py-2 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-bold text-xs shadow-sm flex items-center gap-1.5 transition-all"
          >
            <Plus className="w-4 h-4" />
            Host Event
          </button>
        )}
      </div>

      {/* Filter Tabs */}
      <div className="p-3.5 bg-white rounded-2xl border border-slate-200 shadow-subtle flex items-center gap-2 text-xs">
        {['All', 'Webinar', 'Technical Workshop', 'Alumni Meetup', 'Career Session'].map((type) => (
          <button
            key={type}
            onClick={() => setEventTypeFilter(type)}
            className={`px-3 py-1.5 rounded-xl font-bold transition-colors ${
              eventTypeFilter === type ? 'bg-brand-600 text-white' : 'text-slate-600 hover:bg-slate-100'
            }`}
          >
            {type}
          </button>
        ))}
      </div>

      {/* Events Grid */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 py-6">
          {[1, 2].map((i) => (
            <div key={i} className="h-64 rounded-2xl bg-white border border-slate-200 animate-pulse p-6" />
          ))}
        </div>
      ) : events.length === 0 ? (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center text-xs text-slate-500">
          No alumni events found under selected category.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {events.map((ev) => (
            <div
              key={ev.id}
              className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-subtle hover:shadow-premium transition-all flex flex-col justify-between"
            >
              <div>
                {/* Banner image */}
                <div className="h-40 w-full relative overflow-hidden bg-slate-900">
                  <img
                    src={ev.banner_url || "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800"}
                    alt={ev.title}
                    className="w-full h-full object-cover opacity-80"
                  />
                  <span className="absolute top-3 left-3 px-2.5 py-1 rounded-lg bg-black/60 backdrop-blur-sm text-white text-[11px] font-bold">
                    {ev.event_type}
                  </span>
                </div>

                <div className="p-5 space-y-3">
                  <h3 className="text-base font-bold text-slate-900 leading-snug">{ev.title}</h3>
                  <p className="text-xs text-slate-600 leading-relaxed line-clamp-3">{ev.description}</p>

                  <div className="space-y-1.5 pt-2 border-t border-slate-100 text-xs text-slate-500">
                    <div className="flex items-center gap-2 text-brand-700 font-semibold">
                      <Clock className="w-3.5 h-3.5 text-brand-600" />
                      {new Date(ev.start_time).toLocaleDateString()} • {new Date(ev.start_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </div>
                    <div className="flex items-center gap-2">
                      <MapPin className="w-3.5 h-3.5 text-slate-400" />
                      {ev.location}
                    </div>
                    <div className="flex items-center gap-2">
                      <Users className="w-3.5 h-3.5 text-slate-400" />
                      {ev.registered_count} / {ev.capacity} spots filled
                    </div>
                  </div>
                </div>
              </div>

              {/* Action buttons */}
              <div className="p-5 pt-3 border-t border-slate-100 bg-slate-50/50 flex items-center justify-between gap-2">
                {ev.is_registered && ev.virtual_meeting_link && (
                  <a
                    href={ev.virtual_meeting_link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-xs font-bold text-brand-700 hover:underline flex items-center gap-1"
                  >
                    Meeting Link <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                )}

                <div className="ml-auto">
                  {ev.is_registered ? (
                    <button
                      onClick={() => handleCancelRegistration(ev.id)}
                      className="px-4 py-2 rounded-xl text-xs font-bold bg-slate-200 hover:bg-slate-300 text-slate-700 transition-colors"
                    >
                      Cancel RSVP
                    </button>
                  ) : (
                    <button
                      onClick={() => handleRegister(ev.id)}
                      disabled={ev.registered_count >= ev.capacity}
                      className="px-4 py-2 rounded-xl text-xs font-bold bg-brand-600 hover:bg-brand-700 text-white shadow-sm transition-all disabled:opacity-50"
                    >
                      {ev.registered_count >= ev.capacity ? 'Full Capacity' : 'RSVP Free'}
                    </button>
                  )}
                </div>
              </div>

            </div>
          ))}
        </div>
      )}

      {/* Host Event Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-elevated border border-slate-200 max-h-[90vh] overflow-y-auto">
            <h3 className="text-base font-bold text-slate-900 mb-1">Host an Alumni Event</h3>
            <p className="text-xs text-slate-500 mb-4">Organize a session for students and fellow graduates</p>

            <form onSubmit={handleCreateSubmit} className="space-y-3.5 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Event Title *</label>
                <input
                  type="text"
                  required
                  value={newEvent.title}
                  onChange={(e) => setNewEvent({ ...newEvent, title: e.target.value })}
                  placeholder="e.g. Navigating AI System Design Loops"
                  className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Event Type</label>
                  <select
                    value={newEvent.event_type}
                    onChange={(e) => setNewEvent({ ...newEvent, event_type: e.target.value })}
                    className="w-full p-2.5 rounded-xl border border-slate-200 bg-white focus:outline-none"
                  >
                    <option value="Webinar">Webinar</option>
                    <option value="Technical Workshop">Technical Workshop</option>
                    <option value="Alumni Meetup">Alumni Meetup</option>
                    <option value="Career Session">Career Session</option>
                  </select>
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Capacity</label>
                  <input
                    type="number"
                    value={newEvent.capacity}
                    onChange={(e) => setNewEvent({ ...newEvent, capacity: Number(e.target.value) })}
                    className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Start Date & Time</label>
                  <input
                    type="datetime-local"
                    value={newEvent.start_time}
                    onChange={(e) => setNewEvent({ ...newEvent, start_time: e.target.value })}
                    className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">End Date & Time</label>
                  <input
                    type="datetime-local"
                    value={newEvent.end_time}
                    onChange={(e) => setNewEvent({ ...newEvent, end_time: e.target.value })}
                    className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Virtual Meeting Link</label>
                <input
                  type="url"
                  value={newEvent.virtual_meeting_link}
                  onChange={(e) => setNewEvent({ ...newEvent, virtual_meeting_link: e.target.value })}
                  placeholder="https://meet.google.com/..."
                  className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none"
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Description *</label>
                <textarea
                  rows={3}
                  required
                  value={newEvent.description}
                  onChange={(e) => setNewEvent({ ...newEvent, description: e.target.value })}
                  placeholder="Outline topics covered and target audience..."
                  className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none resize-none"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="px-4 py-2 font-semibold text-slate-600 hover:bg-slate-100 rounded-xl"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 font-bold text-white bg-brand-600 hover:bg-brand-700 rounded-xl shadow-sm"
                >
                  Publish Event
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
};
