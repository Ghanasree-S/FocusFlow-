/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/
import { Task, ActivityData, MLForecast } from './types';

export const INITIAL_TASKS: Task[] = [
  { id: '1', title: 'Q1 Revenue Analysis', deadline: '2023-12-01', category: 'Work', priority: 'High', completed: false, progress: 45 },
  { id: '2', title: 'Morning Workout', deadline: '2023-11-20', category: 'Health', priority: 'Medium', completed: true, progress: 100 },
  { id: '3', title: 'ML Model Fine-tuning', deadline: '2023-11-25', category: 'Study', priority: 'High', completed: false, progress: 12 },
  { id: '4', title: 'Weekly Groceries', deadline: '2023-11-21', category: 'Personal', priority: 'Low', completed: false, progress: 0 },
];

export const TIME_SERIES_DATA: ActivityData[] = [
  { time: '08:00', productive: 20, distracted: 5 },
  { time: '10:00', productive: 85, distracted: 10 },
  { time: '12:00', productive: 40, distracted: 30 },
  { time: '14:00', productive: 95, distracted: 5 },
  { time: '16:00', productive: 70, distracted: 20 },
  { time: '18:00', productive: 30, distracted: 45 },
  { time: '20:00', productive: 15, distracted: 60 },
];

export const FORECAST_DATA: MLForecast = {
  nextDayWorkload: 78,
  completionProbability: 82,
  bestFocusWindow: '09:00 AM - 11:30 AM',
  distractionTrigger: 'Social Media / Morning Emails',
  trend: 'Up',
};
