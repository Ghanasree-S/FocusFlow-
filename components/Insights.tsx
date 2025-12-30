/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React, { useState, useEffect } from 'react';
import { insightsApi } from '../services/api';
import {
  Sparkles,
  BrainCircuit,
  TrendingUp,
  TrendingDown,
  Zap,
  Lightbulb,
  Timer,
  ChevronRight,
  ShieldAlert,
  Minus
} from 'lucide-react';

interface ForecastData {
  productivityLevel: string;
  nextDayWorkload: number;
  completionProbability: number;
  bestFocusWindow: string;
  distractionTrigger: string;
  trend: 'Up' | 'Down' | 'Stable';
  expectedLoadLevel: string;
  stressRisk: string;
}

interface Pattern {
  type: string;
  title: string;
  description: string;
  icon: string;
}

const Insights: React.FC = () => {
  const [forecast, setForecast] = useState<ForecastData | null>(null);
  const [patterns, setPatterns] = useState<Pattern[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchInsights = async () => {
      try {
        const [forecastData, patternsData] = await Promise.all([
          insightsApi.getForecast(),
          insightsApi.getBehavioralPatterns()
        ]);

        setForecast(forecastData);
        setPatterns(patternsData.patterns || []);
      } catch (error) {
        console.error('Failed to fetch insights:', error);
        // No fallback - show empty state
        setForecast(null);
        setPatterns([]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchInsights();
  }, []);

  const getIconComponent = (iconName: string) => {
    switch (iconName) {
      case 'Lightbulb': return <Lightbulb className="text-yellow-500" />;
      case 'Timer': return <Timer className="text-indigo-500" />;
      case 'ShieldAlert': return <ShieldAlert className="text-rose-500" />;
      default: return <Lightbulb className="text-yellow-500" />;
    }
  };

  const getTrendIcon = () => {
    if (forecast?.trend === 'Up') return <TrendingUp className="w-5 h-5" />;
    if (forecast?.trend === 'Down') return <TrendingDown className="w-5 h-5" />;
    return <Minus className="w-5 h-5" />;
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full"></div>
      </div>
    );
  }

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
              <h3 className="text-5xl font-display font-bold mb-4">{forecast?.productivityLevel} Output</h3>
              <div className="flex items-center gap-2 text-indigo-100 font-semibold">
                {getTrendIcon()}
                <span>{forecast?.completionProbability}% Prob. Task Completion</span>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 mt-12 pt-6 border-t border-white/10">
              <div>
                <p className="text-white/60 text-[10px] uppercase font-bold tracking-widest mb-1">Expected Load</p>
                <div className="flex items-center gap-2">
                  <div className="h-2 w-16 bg-white/20 rounded-full overflow-hidden">
                    <div className="h-full bg-white" style={{ width: `${forecast?.nextDayWorkload}%` }}></div>
                  </div>
                  <span className="text-xs font-bold">{forecast?.expectedLoadLevel}</span>
                </div>
              </div>
              <div>
                <p className="text-white/60 text-[10px] uppercase font-bold tracking-widest mb-1">Stress Risk</p>
                <div className="flex items-center gap-2">
                  <div className="h-2 w-16 bg-white/20 rounded-full overflow-hidden">
                    <div className={`h-full ${forecast?.stressRisk === 'Low' ? 'bg-emerald-400 w-1/4' : forecast?.stressRisk === 'Medium' ? 'bg-amber-400 w-1/2' : 'bg-rose-400 w-3/4'}`}></div>
                  </div>
                  <span className="text-xs font-bold">{forecast?.stressRisk}</span>
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
              {forecast?.bestFocusWindow}
            </p>
            <p className="text-xs font-bold text-amber-600 uppercase tracking-widest">Optimal Cognitive state</p>
          </div>

          <div className="mt-8 space-y-4">
            <div className="flex items-center gap-3">
              <Zap className="w-5 h-5 text-indigo-500" />
              <p className="text-sm text-slate-600 dark:text-slate-400">Next 7 days show a <span className="text-indigo-600 dark:text-indigo-400 font-bold">{forecast?.trend?.toLowerCase()} trend</span> in focus duration.</p>
            </div>
            <div className="flex items-center gap-3">
              <ShieldAlert className="w-5 h-5 text-rose-500" />
              <p className="text-sm text-slate-600 dark:text-slate-400">Main distraction: <span className="font-bold">{forecast?.distractionTrigger}</span>.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Behavioral Insights List */}
      <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-8">
        <h3 className="font-display font-bold text-slate-900 dark:text-white mb-6">Behavioral Patterns</h3>
        <div className="space-y-4">
          {patterns.map((pattern, index) => (
            <InsightItem
              key={index}
              icon={getIconComponent(pattern.icon)}
              title={pattern.title}
              description={pattern.description}
              tag={pattern.type}
            />
          ))}
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
        <span className={`text-[10px] font-bold uppercase tracking-widest px-1.5 py-0.5 rounded-md ${tag === 'Warning' ? 'bg-rose-100 text-rose-600' : 'bg-indigo-100 text-indigo-600'
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
