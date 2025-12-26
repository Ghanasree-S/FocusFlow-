/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/
import React from 'react';
import { 
  BarChart3, 
  TrendingUp, 
  Calendar, 
  Clock, 
  Activity,
  Zap,
  Target
} from 'lucide-react';

const Analytics: React.FC = () => {
  // Mock data for heatmap
  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  const hours = ['8am', '10am', '12pm', '2pm', '4pm', '6pm', '8pm', '10pm'];
  
  // Consistency score
  const consistencyScore = 92;

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex items-center gap-3">
        <div className="p-2 bg-indigo-600 rounded-xl text-white shadow-lg shadow-indigo-600/20">
          <BarChart3 className="w-6 h-6" />
        </div>
        <div>
          <h2 className="text-xl font-display font-bold text-slate-900 dark:text-white">Performance Analytics</h2>
          <p className="text-sm text-slate-500">In-depth analysis of your focus and distraction patterns.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Weekly Productivity Line Graph */}
        <div className="lg:col-span-2 bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm">
          <div className="flex justify-between items-center mb-6">
            <h3 className="font-display font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <Activity className="w-4 h-4 text-indigo-500" />
              Weekly Productivity
            </h3>
            <span className="text-xs font-bold text-emerald-500 bg-emerald-50 dark:bg-emerald-500/10 px-2 py-1 rounded-lg">+14% vs last week</span>
          </div>
          
          <div className="h-64 w-full relative pt-4">
            <svg className="w-full h-full overflow-visible" preserveAspectRatio="none" viewBox="0 0 700 200">
              {/* Grid lines */}
              {[0, 50, 100, 150, 200].map(y => (
                <line key={y} x1="0" y1={y} x2="700" y2={y} stroke="currentColor" strokeOpacity="0.05" />
              ))}
              
              {/* Productivity Line Path */}
              <path 
                d="M 0 150 Q 100 80 200 120 T 400 40 T 600 90 T 700 60" 
                fill="none" 
                stroke="#6366f1" 
                strokeWidth="4" 
                strokeLinecap="round"
                className="drop-shadow-[0_4px_10px_rgba(99,102,241,0.3)]"
              />
              
              {/* Area under the path */}
              <path 
                d="M 0 150 Q 100 80 200 120 T 400 40 T 600 90 T 700 60 L 700 200 L 0 200 Z" 
                fill="url(#gradient-prod)" 
                fillOpacity="0.1"
              />
              
              <defs>
                <linearGradient id="gradient-prod" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#6366f1" />
                  <stop offset="100%" stopColor="#6366f1" stopOpacity="0" />
                </linearGradient>
              </defs>
            </svg>
            <div className="flex justify-between mt-4 px-2">
              {days.map(day => (
                <span key={day} className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{day}</span>
              ))}
            </div>
          </div>
        </div>

        {/* Consistency Score Card */}
        <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-6 flex flex-col items-center justify-center text-center shadow-sm relative overflow-hidden">
            <div className="absolute top-0 right-0 p-4 opacity-5">
              <Zap className="w-32 h-32 text-indigo-500" />
            </div>
            
            <div className="relative w-32 h-32 mb-6">
              <svg className="w-full h-full -rotate-90">
                <circle cx="64" cy="64" r="58" fill="none" stroke="currentColor" strokeWidth="8" className="text-slate-100 dark:text-slate-800" />
                <circle 
                  cx="64" cy="64" r="58" fill="none" stroke="#6366f1" strokeWidth="8" 
                  strokeDasharray="364.4" strokeDashoffset={364.4 * (1 - consistencyScore/100)} 
                  strokeLinecap="round"
                />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-3xl font-display font-bold text-slate-900 dark:text-white">{consistencyScore}%</span>
              </div>
            </div>
            
            <h3 className="font-display font-bold text-slate-900 dark:text-white mb-2">Consistency Score</h3>
            <p className="text-xs text-slate-500 dark:text-slate-400 max-w-[200px]">Your performance is extremely stable compared to last month.</p>
            
            <div className="mt-6 w-full pt-6 border-t border-slate-100 dark:border-slate-800">
               <div className="flex justify-between items-center text-xs font-bold text-slate-500 uppercase tracking-widest px-2">
                 <span>Streak</span>
                 <span className="text-indigo-600 dark:text-indigo-400">12 Days</span>
               </div>
            </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Distraction Heatmap */}
        <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm">
          <div className="flex justify-between items-center mb-6">
            <h3 className="font-display font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <Clock className="w-4 h-4 text-rose-500" />
              Distraction Patterns
            </h3>
            <div className="flex gap-1">
              {[1, 2, 3, 4].map(v => <div key={v} className={`w-3 h-3 rounded-sm bg-rose-500 opacity-${v*25}`} />)}
            </div>
          </div>
          
          <div className="grid grid-cols-9 gap-2">
            <div className="col-span-1"></div>
            {hours.map(h => <div key={h} className="text-[9px] font-bold text-slate-400 uppercase text-center">{h}</div>)}
            
            {days.map(day => (
              <React.Fragment key={day}>
                <div className="text-[9px] font-bold text-slate-400 uppercase py-2">{day}</div>
                {hours.map((h, i) => {
                  const intensity = Math.floor(Math.random() * 5);
                  return (
                    <div 
                      key={h} 
                      className={`h-8 rounded-md transition-all duration-500 ${
                        intensity === 0 ? 'bg-slate-50 dark:bg-slate-800/50' : 
                        intensity === 1 ? 'bg-rose-500/10' :
                        intensity === 2 ? 'bg-rose-500/30' :
                        intensity === 3 ? 'bg-rose-500/60' : 'bg-rose-500'
                      }`}
                    />
                  );
                })}
              </React.Fragment>
            ))}
          </div>
        </div>

        {/* Top Productive Hours & Total Focus */}
        <div className="space-y-6">
          <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm">
            <div className="flex items-center gap-4 mb-6">
              <div className="w-12 h-12 bg-emerald-50 dark:bg-emerald-500/10 rounded-2xl flex items-center justify-center text-emerald-500">
                <Clock className="w-6 h-6" />
              </div>
              <div>
                <h4 className="font-display font-bold text-slate-900 dark:text-white">Top Focus Window</h4>
                <p className="text-xs text-slate-500">Peak performance observed between</p>
              </div>
            </div>
            <div className="bg-slate-50 dark:bg-slate-800/50 p-6 rounded-2xl text-center">
              <span className="text-3xl font-display font-bold text-indigo-600 dark:text-indigo-400 tracking-tight">09:00 AM — 11:30 AM</span>
              <div className="flex items-center justify-center gap-2 mt-2 text-[10px] font-bold text-emerald-500 uppercase tracking-widest">
                <TrendingUp className="w-3 h-3" />
                94% Focus Efficiency
              </div>
            </div>
          </div>

          <div className="bg-indigo-600 rounded-3xl p-6 text-white shadow-xl shadow-indigo-600/20 flex items-center justify-between">
            <div className="space-y-1">
              <p className="text-indigo-100 text-xs font-bold uppercase tracking-widest">Total Focus Time</p>
              <h4 className="text-4xl font-display font-bold">42h 15m</h4>
              <p className="text-indigo-200 text-[10px]">+5.4h vs last week</p>
            </div>
            <div className="w-16 h-16 bg-white/10 rounded-2xl flex items-center justify-center backdrop-blur-md">
              <Target className="w-8 h-8 text-white" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
