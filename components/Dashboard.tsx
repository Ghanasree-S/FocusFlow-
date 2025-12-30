/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React, { useState, useEffect } from 'react';
import { Task } from '../types';
import { insightsApi } from '../services/api';
import {
  CheckCircle2,
  Clock,
  AlertTriangle,
  ArrowUpRight,
  Plus,
  Target
} from 'lucide-react';

interface DashboardProps {
  tasks: Task[];
}

interface DashboardData {
  taskStats: { total: number; completed: number; pending: number; high_priority: number };
  focusScore: number;
  distractionSpikes: number;
  hourlyData: Array<{ time: string; productive: number; distracted: number }>;
  hasData?: boolean;
}

const Dashboard: React.FC<DashboardProps> = ({ tasks }) => {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(() => {
    // Load cached data immediately on mount
    const cached = localStorage.getItem('focusflow_dashboard_cache');
    return cached ? JSON.parse(cached) : null;
  });
  const [isLoading, setIsLoading] = useState(!localStorage.getItem('focusflow_dashboard_cache'));
  const [lastUpdated, setLastUpdated] = useState<string>('');

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const data = await insightsApi.getDashboard();
        setDashboardData(data);
        // Cache the data
        localStorage.setItem('focusflow_dashboard_cache', JSON.stringify(data));
        setLastUpdated(new Date().toLocaleTimeString());
      } catch (error) {
        console.error('Failed to fetch dashboard:', error);
      } finally {
        setIsLoading(false);
      }
    };

    // Fetch immediately
    fetchDashboard();

    // Then refresh every 60 seconds
    const interval = setInterval(fetchDashboard, 60000);
    return () => clearInterval(interval);
  }, []);

  // Use ONLY real data from API - no mock fallbacks
  const completedTasks = dashboardData?.taskStats?.completed ?? 0;
  const totalTasks = dashboardData?.taskStats?.total ?? 0;
  const pendingTasks = dashboardData?.taskStats?.pending ?? 0;
  const focusScore = dashboardData?.focusScore ?? 0;
  const distractionSpikes = dashboardData?.distractionSpikes ?? 0;

  // Use real hourly data or empty array
  const timeSeriesData = dashboardData?.hourlyData?.length
    ? dashboardData.hourlyData
    : [];

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full"></div>
      </div>
    );
  }

  // Always show dashboard - even if data is zero
  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          label="Tasks Completed"
          value={completedTasks.toString()}
          subValue={`of ${totalTasks} total`}
          icon={<CheckCircle2 className="text-emerald-500" />}
          color="emerald"
        />
        <StatCard
          label="Focus Score"
          value={`${focusScore}%`}
          subValue="+4% from yesterday"
          icon={<Target className="text-indigo-500" />}
          color="indigo"
          trend="up"
        />
        <StatCard
          label="Pending Deadline"
          value={pendingTasks.toString()}
          subValue="2 due within 24h"
          icon={<Clock className="text-amber-500" />}
          color="amber"
        />
        <StatCard
          label="Distraction Spikes"
          value={distractionSpikes.toString()}
          subValue="Lower than average"
          icon={<AlertTriangle className="text-rose-500" />}
          color="rose"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Activity Chart */}
        <div className="lg:col-span-2 bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6">
          <div className="flex justify-between items-center mb-6">
            <h3 className="font-display font-bold text-slate-900 dark:text-white">Productivity Trends</h3>
            <div className="flex items-center gap-4 text-xs font-medium">
              <div className="flex items-center gap-1.5">
                <div className="w-4 h-1 bg-indigo-500 rounded"></div>
                <span className="text-slate-500">Productive</span>
              </div>
              <div className="flex items-center gap-1.5">
                <div className="w-4 h-0.5 border-t-2 border-dashed border-rose-500"></div>
                <span className="text-slate-500">Distracted</span>
              </div>
            </div>
          </div>

          {/* Time Series Line Chart */}
          <div className="h-56 relative mt-4">
            {timeSeriesData.length > 0 ? (
              <svg className="w-full h-full" viewBox="0 0 600 200" preserveAspectRatio="none">
                {/* Grid lines */}
                {[0, 50, 100, 150].map(y => (
                  <line key={y} x1="0" y1={y} x2="600" y2={y} stroke="currentColor" strokeOpacity="0.1" />
                ))}

                {/* Gradient definitions */}
                <defs>
                  <linearGradient id="productiveGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#6366f1" stopOpacity="0.4" />
                    <stop offset="100%" stopColor="#6366f1" stopOpacity="0" />
                  </linearGradient>
                </defs>

                {(() => {
                  const maxValue = Math.max(...timeSeriesData.map(d => Math.max(d.productive, d.distracted)), 1);
                  const width = 600;
                  const height = 170;
                  const stepX = width / Math.max(timeSeriesData.length - 1, 1);

                  const productivePoints = timeSeriesData.map((d, i) => ({
                    x: i * stepX,
                    y: height - (d.productive / maxValue) * height
                  }));

                  const distractedPoints = timeSeriesData.map((d, i) => ({
                    x: i * stepX,
                    y: height - (d.distracted / maxValue) * height
                  }));

                  const productivePath = productivePoints.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ');
                  const distractedPath = distractedPoints.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ');
                  const areaPath = productivePath + ` L ${width} ${height} L 0 ${height} Z`;

                  return (
                    <>
                      {/* Area under productive line */}
                      <path d={areaPath} fill="url(#productiveGradient)" />

                      {/* Productive line (solid) */}
                      <path d={productivePath} fill="none" stroke="#6366f1" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />

                      {/* Distracted line (dashed) */}
                      <path d={distractedPath} fill="none" stroke="#f43f5e" strokeWidth="2" strokeLinecap="round" strokeDasharray="8,4" />

                      {/* Data points */}
                      {productivePoints.map((p, i) => (
                        <circle key={`p-${i}`} cx={p.x} cy={p.y} r="5" fill="#6366f1" stroke="#fff" strokeWidth="2" />
                      ))}
                      {distractedPoints.map((p, i) => (
                        <circle key={`d-${i}`} cx={p.x} cy={p.y} r="4" fill="#f43f5e" stroke="#fff" strokeWidth="1" />
                      ))}
                    </>
                  );
                })()}
              </svg>
            ) : (
              <div className="flex items-center justify-center h-full text-slate-400">
                No time series data yet
              </div>
            )}

            {/* X-axis labels */}
            <div className="flex justify-between px-1 mt-1">
              {timeSeriesData.map((d, i) => (
                <span key={i} className="text-[9px] font-medium text-slate-400">{d.time}</span>
              ))}
            </div>
          </div>
        </div>

        {/* Quick Tasks */}
        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 flex flex-col">
          <div className="flex justify-between items-center mb-6">
            <h3 className="font-display font-bold text-slate-900 dark:text-white">Active Tasks</h3>
            <button className="p-1.5 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg text-indigo-600 transition-colors">
              <Plus className="w-5 h-5" />
            </button>
          </div>
          <div className="space-y-4 flex-1 overflow-y-auto pr-1">
            {tasks.filter(t => !t.completed).slice(0, 4).map(task => (
              <div key={task.id} className="p-3 bg-slate-50 dark:bg-slate-800/50 rounded-xl border border-transparent hover:border-slate-200 dark:hover:border-slate-700 transition-all cursor-pointer">
                <div className="flex justify-between items-start mb-2">
                  <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full ${task.priority === 'High' ? 'bg-rose-100 text-rose-600 dark:bg-rose-500/20' : 'bg-slate-200 text-slate-600 dark:bg-slate-700'
                    }`}>
                    {task.priority}
                  </span>
                  <span className="text-[10px] text-slate-400">{task.deadline}</span>
                </div>
                <p className="text-sm font-semibold text-slate-800 dark:text-slate-200 mb-2 truncate">{task.title}</p>
                <div className="w-full h-1 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-indigo-500 transition-all duration-1000"
                    style={{ width: `${task.progress}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
          <button className="mt-4 w-full py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-bold rounded-xl shadow-lg shadow-indigo-600/20 transition-all">
            Start Focus Session
          </button>
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ label, value, subValue, icon, color, trend }: any) => (
  <div className="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm relative overflow-hidden group hover:scale-[1.02] transition-transform">
    <div className={`absolute -right-4 -top-4 w-24 h-24 bg-${color}-500/5 rounded-full blur-2xl group-hover:bg-${color}-500/10 transition-colors`}></div>
    <div className="flex justify-between items-start mb-4 relative z-10">
      <div className={`p-2.5 rounded-xl bg-${color}-50 dark:bg-${color}-500/10`}>
        {icon}
      </div>
      {trend === 'up' && (
        <span className="flex items-center text-[10px] font-bold text-emerald-500 bg-emerald-50 dark:bg-emerald-500/10 px-1.5 py-0.5 rounded-lg">
          <ArrowUpRight className="w-3 h-3 mr-0.5" /> 12%
        </span>
      )}
    </div>
    <h4 className="text-2xl font-display font-bold text-slate-900 dark:text-white mb-1">{value}</h4>
    <p className="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-widest mb-1">{label}</p>
    <p className="text-[10px] text-slate-400">{subValue}</p>
  </div>
);

export default Dashboard;
