/**
 * FocusFlow API Service
 * Handles all backend API calls with JWT authentication
 */

const API_BASE_URL = 'http://localhost:5000/api';

// Token management - uses sessionStorage so token clears when browser closes
let authToken: string | null = sessionStorage.getItem('focusflow_token');

export const setAuthToken = (token: string | null) => {
    authToken = token;
    if (token) {
        sessionStorage.setItem('focusflow_token', token);
    } else {
        sessionStorage.removeItem('focusflow_token');
    }
};

export const getAuthToken = () => authToken;

// API request helper
const apiRequest = async (
    endpoint: string,
    options: RequestInit = {}
): Promise<any> => {
    const headers: Record<string, string> = {
        'Content-Type': 'application/json',
        ...((options.headers as Record<string, string>) || {}),
    };

    if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`;
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers,
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || 'API request failed');
    }

    return data;
};

// ============ AUTH API ============
export const authApi = {
    register: async (name: string, email: string, password: string, style?: string, goals?: string[]) => {
        const data = await apiRequest('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ name, email, password, style, goals }),
        });
        if (data.token) {
            setAuthToken(data.token);
        }
        return data;
    },

    login: async (email: string, password: string) => {
        const data = await apiRequest('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password }),
        });
        if (data.token) {
            setAuthToken(data.token);
        }
        return data;
    },

    getProfile: async () => {
        return await apiRequest('/auth/profile');
    },

    updateProfile: async (updates: { name?: string; style?: string; goals?: string[] }) => {
        return await apiRequest('/auth/profile', {
            method: 'PUT',
            body: JSON.stringify(updates),
        });
    },

    logout: () => {
        setAuthToken(null);
    },
};

// ============ TASKS API ============
export const tasksApi = {
    getAll: async (completed?: boolean) => {
        const query = completed !== undefined ? `?completed=${completed}` : '';
        return await apiRequest(`/tasks${query}`);
    },

    create: async (task: {
        title: string;
        deadline?: string;
        category?: string;
        priority?: string;
    }) => {
        return await apiRequest('/tasks', {
            method: 'POST',
            body: JSON.stringify(task),
        });
    },

    update: async (taskId: string, updates: {
        title?: string;
        deadline?: string;
        category?: string;
        priority?: string;
        completed?: boolean;
        progress?: number;
    }) => {
        return await apiRequest(`/tasks/${taskId}`, {
            method: 'PUT',
            body: JSON.stringify(updates),
        });
    },

    delete: async (taskId: string) => {
        return await apiRequest(`/tasks/${taskId}`, {
            method: 'DELETE',
        });
    },

    getStats: async () => {
        return await apiRequest('/tasks/stats');
    },
};

// ============ ACTIVITIES API ============
export const activitiesApi = {
    log: async (appName: string, durationMinutes: number, category?: string) => {
        return await apiRequest('/activities', {
            method: 'POST',
            body: JSON.stringify({
                app_name: appName,
                duration_minutes: durationMinutes,
                category,
            }),
        });
    },

    logBatch: async (activities: Array<{
        app_name: string;
        duration_minutes: number;
        category?: string;
        timestamp?: string;
    }>) => {
        return await apiRequest('/activities/batch', {
            method: 'POST',
            body: JSON.stringify({ activities }),
        });
    },

    getHistory: async (days: number = 7) => {
        return await apiRequest(`/activities?days=${days}`);
    },

    getDailySummary: async (date?: string) => {
        const query = date ? `?date=${date}` : '';
        return await apiRequest(`/activities/summary${query}`);
    },

    getWeeklyTrends: async () => {
        return await apiRequest('/activities/weekly');
    },

    getHourlyBreakdown: async (days: number = 7) => {
        return await apiRequest(`/activities/hourly?days=${days}`);
    },
};

// ============ FOCUS API ============
export const focusApi = {
    startSession: async (durationMinutes: number = 25) => {
        return await apiRequest('/focus/start', {
            method: 'POST',
            body: JSON.stringify({ duration: durationMinutes }),
        });
    },

    endSession: async (completed: boolean = true) => {
        return await apiRequest('/focus/end', {
            method: 'POST',
            body: JSON.stringify({ completed }),
        });
    },

    getActiveSession: async () => {
        return await apiRequest('/focus/active');
    },

    getHistory: async (days: number = 30) => {
        return await apiRequest(`/focus/history?days=${days}`);
    },

    getStats: async (days: number = 7) => {
        return await apiRequest(`/focus/stats?days=${days}`);
    },
};

// ============ INSIGHTS API ============
export const insightsApi = {
    getDashboard: async () => {
        return await apiRequest('/insights/dashboard');
    },

    getForecast: async () => {
        return await apiRequest('/insights/forecast');
    },

    getTrends: async (days: number = 7) => {
        return await apiRequest(`/insights/trends?days=${days}`);
    },

    getBehavioralPatterns: async () => {
        return await apiRequest('/insights/behavioral-patterns');
    },

    getWeeklyReport: async () => {
        return await apiRequest('/insights/reports/weekly');
    },

    // ML Model APIs
    getMLStatus: async () => {
        return await apiRequest('/insights/ml/status');
    },

    trainModels: async () => {
        return await apiRequest('/insights/ml/train', {
            method: 'POST',
        });
    },

    compareModels: async () => {
        return await apiRequest('/insights/ml/compare');
    },

    getModelForecast: async (model: 'lstm' | 'arima' | 'prophet' | 'ensemble', periods: number = 7) => {
        return await apiRequest(`/insights/ml/forecast/${model}?periods=${periods}`);
    },
};

// ============ HEALTH CHECK ============
export const healthCheck = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        return response.ok;
    } catch {
        return false;
    }
};

// Export all APIs
export default {
    auth: authApi,
    tasks: tasksApi,
    activities: activitiesApi,
    focus: focusApi,
    insights: insightsApi,
    healthCheck,
};
