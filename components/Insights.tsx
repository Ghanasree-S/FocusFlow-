/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/
import React from 'react';
import { FORECAST_DATA } from '../mockData';
import { 
  Sparkles, 
  BrainCircuit, 
  TrendingUp, 
  Zap, 
  Lightbulb,
  Timer,
  ChevronRight,
  ShieldAlert
} from 'lucide-react';

const Insights: React.FC = () => {
  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex items-center gap-3">
        <div className="p-2 bg-indigo-600 rounded-xl text-white shadow-lg shadow-indigo-600/20">
          <BrainCircuit className="w-6 h-6" />
        </div>
        <div>
          <h2 className="text-xl font-display font-bold text-slate-900 dark:text-white">Predictive Analytics</h2>
          <p className="text-sm text-slate-500">ML models trained on your behavioral history.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Core Prediction Card */}
        <div className="bg-gradient-to-br from-indigo-600 to-purple-700 rounded-3xl p-8 text-white relative overflow-hidden shadow-2xl shadow-indigo-600/30">
          <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>
          <div className="relative z-10 flex flex-col h-full">
            <div className="flex justify-between items-start mb-12">
              <span className="text-xs font-bold uppercase tracking-[0.2em] bg-white/20 px-3 py-1 rounded-full backdrop-blur-md">
                24H Forecasting
              </span>
              <Sparkles className="w-6 h-6 text-yellow-300 animate-pulse" />
            </div>
            
            <div className="mb-auto">
              <p className="text-white/70 text-sm font-medium mb-1">Tomorrow's Productivity Forecast</p>
              <h3 className="text-5xl font-display font-bold mb-4">High Output</h3>
              <div className="flex items-center gap-2 text-indigo-100 font-semibold">
                <TrendingUp className="w-5 h-5" />
                <span>82% Prob. Task Completion</span>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 mt-12 pt-6 border-t border-white/10">
              <div>
                <p className="text-white/60 text-[10px] uppercase font-bold tracking-widest mb-1">Expected Load</p>
                <div className="flex items-center gap-2">
                  <div className="h-2 w-16 bg-white/20 rounded-full overflow-hidden">
                    <div className="h-full bg-white w-3/4"></div>
                  </div>
                  <span className="text-xs font-bold">Medium</span>
                </div>
              </div>
              <div>
                <p className="text-white/60 text-[10px] uppercase font-bold tracking-widest mb-1">Stress Risk</p>
                <div className="flex items-center gap-2">
                  <div className="h-2 w-16 bg-white/20 rounded-full overflow-hidden">
                    <div className="h-full bg-emerald-400 w-1/4"></div>
                  </div>
                  <span className="text-xs font-bold">Low</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Focus Window Card */}
        <div className="bg-white dark:bg-slate-900 rounded-3xl p-8 border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col">
          <div className="flex items-center gap-4 mb-8">
            <div className="w-12 h-12 bg-amber-50 dark:bg-amber-500/10 rounded-2xl flex items-center justify-center text-amber-500">
              <Timer className="w-6 h-6" />
            </div>
            <div>
              <h4 className="font-display font-bold text-slate-900 dark:text-white">Peak Focus Window</h4>
              <p className="text-xs text-slate-500">Based on Time-Series analysis</p>
            </div>
          </div>

          <div className="flex-1 flex flex-col justify-center text-center py-6 bg-slate-50 dark:bg-slate-800/50 rounded-2xl border border-dashed border-slate-300 dark:border-slate-700">
            <p className="text-3xl font-display font-bold text-slate-800 dark:text-slate-100 mb-2">
              {FORECAST_DATA.bestFocusWindow}
            </p>
            <p className="text-xs font-bold text-amber-600 uppercase tracking-widest">Optimal Cognitive state</p>
          </div>

          <div className="mt-8 space-y-4">
            <div className="flex items-center gap-3">
              <Zap className="w-5 h-5 text-indigo-500" />
              <p className="text-sm text-slate-600 dark:text-slate-400">Next 7 days show a <span className="text-indigo-600 dark:text-indigo-400 font-bold">positive trend</span> in focus duration.</p>
            </div>
            <div className="flex items-center gap-3">
              <ShieldAlert className="w-5 h-5 text-rose-500" />
              <p className="text-sm text-slate-600 dark:text-slate-400">High distraction probability detected at <span className="font-bold">1:45 PM</span>.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Behavioral Insights List */}
      <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-8">
        <h3 className="font-display font-bold text-slate-900 dark:text-white mb-6">Behavioral Patterns</h3>
        <div className="space-y-4">
          <InsightItem 
            icon={<Lightbulb className="text-yellow-500" />}
            title="Consistency Streak"
            description="You are most productive after morning physical activity. Your streak is currently at 5 days."
            tag="Optimization"
          />
          <InsightItem 
            icon={<Timer className="text-indigo-500" />}
            title="Deep Work Capacity"
            description="Average focus duration has increased from 42m to 58m this week (+38%)."
            tag="Growth"
          />
          <InsightItem 
            icon={<ShieldAlert className="text-rose-500" />}
            title="Context Switching"
            description="Switching between Email and Work apps before 11 AM reduces output by ~15%."
            tag="Warning"
          />
        </div>
      </div>
    </div>
  );
};

const InsightItem = ({ icon, title, description, tag }: any) => (
  <div className="group flex items-center gap-6 p-4 rounded-2xl hover:bg-slate-50 dark:hover:bg-slate-800 transition-all cursor-default border border-transparent hover:border-slate-200 dark:hover:border-slate-700">
    <div className="p-3 bg-white dark:bg-slate-900 rounded-xl shadow-sm border border-slate-100 dark:border-slate-800">
      {icon}
    </div>
    <div className="flex-1">
      <div className="flex items-center gap-2 mb-1">
        <h5 className="font-bold text-slate-800 dark:text-slate-200">{title}</h5>
        <span className={`text-[10px] font-bold uppercase tracking-widest px-1.5 py-0.5 rounded-md ${
          tag === 'Warning' ? 'bg-rose-100 text-rose-600' : 'bg-indigo-100 text-indigo-600'
        }`}>
          {tag}
        </span>
      </div>
      <p className="text-sm text-slate-500 dark:text-slate-400">{description}</p>
    </div>
    <ChevronRight className="w-5 h-5 text-slate-300 group-hover:text-indigo-500 transition-colors" />
  </div>
);

export default Insights;
