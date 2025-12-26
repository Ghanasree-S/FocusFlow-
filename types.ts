
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

export type View = 'LOGIN' | 'SIGNUP' | 'ONBOARDING' | 'DASHBOARD' | 'TASKS' | 'ANALYTICS' | 'INSIGHTS' | 'FOCUS' | 'REPORTS' | 'SETTINGS' | 'PROFILE';

export type ProductivityLevel = 'Low' | 'Medium' | 'High';
export type TaskPriority = 'Low' | 'Medium' | 'High';
export type TaskCategory = 'Work' | 'Personal' | 'Study' | 'Health' | 'Urgent';

export interface Task {
  id: string;
  title: string;
  deadline: string;
  category: TaskCategory;
  priority: TaskPriority;
  completed: boolean;
  progress: number;
}

export interface ActivityData {
  time: string;
  productive: number;
  distracted: number;
}

export interface MLForecast {
  nextDayWorkload: number; // 0-100
  completionProbability: number; // 0-100
  bestFocusWindow: string;
  distractionTrigger: string;
  trend: 'Up' | 'Down' | 'Stable';
}

export interface UserProfile {
  id?: string;
  name: string;
  email: string;
  style: 'Balanced' | 'High-focus' | 'Flexible';
  goals: string[];
}

/**
 * Visual generation and research types
 */

export type ComplexityLevel = 'Elementary' | 'High School' | 'College' | 'Expert';

export type VisualStyle = 'Minimalist' | 'Realistic' | 'Cartoon' | 'Vintage' | 'Futuristic' | '3D Render' | 'Sketch';

export type AspectRatio = '1:1' | '3:4' | '4:3' | '9:16' | '16:9';

export type Language = string;

export interface SearchResultItem {
  title: string;
  url: string;
}

export interface ResearchResult {
  imagePrompt: string;
  facts: string[];
  searchResults: SearchResultItem[];
}

export interface GeneratedImage {
  id: string;
  data: string;
  prompt: string;
}
