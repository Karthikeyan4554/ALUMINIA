const API_BASE = '/api';

export class ApiError extends Error {
  status: number;
  data: any;

  constructor(status: number, message: string, data?: any) {
    super(message);
    this.status = status;
    this.data = data;
  }
}

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem('alumnia_token');
  const headers = new Headers(options.headers || {});

  if (!headers.has('Content-Type') && !(options.body instanceof FormData)) {
    headers.set('Content-Type', 'application/json');
  }

  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let errorDetail = 'Request failed';
    try {
      const errJson = await response.json();
      errorDetail = errJson.detail || errJson.message || errorDetail;
    } catch {
      errorDetail = response.statusText || errorDetail;
    }
    throw new ApiError(response.status, errorDetail);
  }

  return response.json();
}

export const api = {
  // Auth
  login: (data: any) => request<any>('/auth/login', { method: 'POST', body: JSON.stringify(data) }),
  register: (data: any) => request<any>('/auth/register', { method: 'POST', body: JSON.stringify(data) }),
  getMe: () => request<any>('/auth/me'),
  forgotPassword: (email: string) => request<any>('/auth/forgot-password', { method: 'POST', body: JSON.stringify({ email }) }),
  resetPassword: (data: any) => request<any>('/auth/reset-password', { method: 'POST', body: JSON.stringify(data) }),

  // Profiles
  getMyProfile: () => request<any>('/profiles/me'),
  getDashboardStats: () => request<any>('/profiles/dashboard/stats'),
  updateMyProfile: (data: any) => request<any>('/profiles/me', { method: 'PUT', body: JSON.stringify(data) }),
  getProfile: (userId: string) => request<any>(`/profiles/${userId}`),
  getDirectory: (params: Record<string, any>) => {
    const qs = new URLSearchParams(
      Object.entries(params).filter(([_, v]) => v !== undefined && v !== null && v !== '')
    ).toString();
    return request<any>(`/profiles/directory?${qs}`);
  },
  getDirectoryFilters: () => request<{ departments: string[]; industries: string[] }>('/profiles/filters/meta'),

  // Recommendations
  getRecommendations: (params: Record<string, any> = {}) => {
    const qs = new URLSearchParams(
      Object.entries(params).filter(([_, v]) => v !== undefined && v !== null && v !== '')
    ).toString();
    return request<any[]>(`/recommendations${qs ? `?${qs}` : ''}`);
  },
  submitRecommendationFeedback: (data: any) => request<any>('/recommendations/feedback', { method: 'POST', body: JSON.stringify(data) }),
  getRecommendationWeights: () => request<any>('/recommendations/weights'),
  updateRecommendationWeights: (data: any) => request<any>('/recommendations/weights', { method: 'PUT', body: JSON.stringify(data) }),

  // Connections
  sendConnectionRequest: (data: { receiver_id: string; message?: string }) => 
    request<any>('/connections/request', { method: 'POST', body: JSON.stringify(data) }),
  getConnectionRequests: () => request<{ incoming: any[]; outgoing: any[] }>('/connections/requests'),
  acceptConnectionRequest: (id: string) => request<any>(`/connections/requests/${id}/accept`, { method: 'POST' }),
  rejectConnectionRequest: (id: string) => request<any>(`/connections/requests/${id}/reject`, { method: 'POST' }),
  cancelConnectionRequest: (id: string) => request<any>(`/connections/requests/${id}/cancel`, { method: 'POST' }),
  getConnections: () => request<any[]>('/connections'),
  removeConnection: (targetUserId: string) => request<any>(`/connections/${targetUserId}`, { method: 'DELETE' }),

  // Messaging
  getConversations: () => request<any[]>('/messages/conversations'),
  startConversation: (targetUserId: string) => request<{ conversation_id: string }>(`/messages/start/${targetUserId}`, { method: 'POST' }),
  getMessages: (conversationId: string) => request<any[]>(`/messages/conversations/${conversationId}/messages`),
  sendMessage: (conversationId: string, content: string) => 
    request<any>(`/messages/conversations/${conversationId}/messages`, { method: 'POST', body: JSON.stringify({ content }) }),

  // Mentorship
  getMentors: (params: Record<string, any> = {}) => {
    const qs = new URLSearchParams(
      Object.entries(params).filter(([_, v]) => v !== undefined && v !== null && v !== '')
    ).toString();
    return request<any[]>(`/mentorship/mentors${qs ? `?${qs}` : ''}`);
  },
  requestMentorship: (data: { mentor_id: string; goals_description: string; preferred_frequency?: string }) =>
    request<any>('/mentorship/request', { method: 'POST', body: JSON.stringify(data) }),
  getMentorshipRequests: () => request<any[]>('/mentorship/requests'),
  updateMentorshipStatus: (requestId: string, status: string, response_note?: string) =>
    request<any>(`/mentorship/requests/${requestId}/status`, { method: 'POST', body: JSON.stringify({ status, response_note }) }),
  scheduleSession: (data: any) => request<any>('/mentorship/sessions', { method: 'POST', body: JSON.stringify(data) }),
  getMentorshipSessions: () => request<any[]>('/mentorship/sessions'),

  // Jobs
  getJobs: (params: Record<string, any> = {}) => {
    const qs = new URLSearchParams(
      Object.entries(params).filter(([_, v]) => v !== undefined && v !== null && v !== '')
    ).toString();
    return request<any[]>(`/jobs${qs ? `?${qs}` : ''}`);
  },
  createJob: (data: any) => request<any>('/jobs', { method: 'POST', body: JSON.stringify(data) }),
  toggleSaveJob: (jobId: string) => request<any>(`/jobs/${jobId}/save`, { method: 'POST' }),
  getSavedJobs: () => request<any[]>('/jobs/saved'),
  applyToJob: (jobId: string, data: any) => request<any>(`/jobs/${jobId}/apply`, { method: 'POST', body: JSON.stringify(data) }),

  // Events
  getEvents: (params: Record<string, any> = {}) => {
    const qs = new URLSearchParams(
      Object.entries(params).filter(([_, v]) => v !== undefined && v !== null && v !== '')
    ).toString();
    return request<any[]>(`/events${qs ? `?${qs}` : ''}`);
  },
  createEvent: (data: any) => request<any>('/events', { method: 'POST', body: JSON.stringify(data) }),
  registerForEvent: (eventId: string) => request<any>(`/events/${eventId}/register`, { method: 'POST' }),
  cancelEventRegistration: (eventId: string) => request<any>(`/events/${eventId}/cancel`, { method: 'POST' }),

  // Notifications
  getNotifications: () => request<any[]>('/notifications'),
  getUnreadNotificationCount: () => request<{ unread_count: number }>('/notifications/unread-count'),
  markNotificationAsRead: (id: string) => request<any>(`/notifications/${id}/read`, { method: 'POST' }),
  markAllNotificationsAsRead: () => request<any>('/notifications/read-all', { method: 'POST' }),

  // AI Assistant
  chatWithAssistant: (data: { message: string; task?: string; target_user_id?: string; history?: any[] }) =>
    request<any>('/ai/assistant', { method: 'POST', body: JSON.stringify(data) }),

  // Admin
  getAdminMetrics: () => request<any>('/admin/metrics'),
  getAdminUsers: (params: Record<string, any> = {}) => {
    const qs = new URLSearchParams(
      Object.entries(params).filter(([_, v]) => v !== undefined && v !== null && v !== '')
    ).toString();
    return request<any[]>(`/admin/users${qs ? `?${qs}` : ''}`);
  },
  toggleUserStatus: (userId: string) => request<any>(`/admin/users/${userId}/status`, { method: 'PUT' }),
  updateUserRole: (userId: string, role: string) => request<any>(`/admin/users/${userId}/role?new_role=${role}`, { method: 'PUT' }),
  getAdminReports: () => request<any[]>('/admin/reports'),
  resolveAdminReport: (reportId: string, action: string) => request<any>(`/admin/reports/${reportId}/resolve?action=${action}`, { method: 'PUT' }),
  submitReport: (data: any) => request<any>('/admin/reports', { method: 'POST', body: JSON.stringify(data) }),
};
