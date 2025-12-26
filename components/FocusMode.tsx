/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/
import React, { useState, useEffect } from 'react';
import { Play, Pause, RotateCcw, ShieldCheck, Moon, BellOff, X } from 'lucide-react';

const FocusMode: React.FC = () => {
  const [timeLeft, setTimeLeft] = useState(25 * 60);
  const [isActive, setIsActive] = useState(false);
  const [sessionType, setSessionType] = useState<'Work' | 'Break'>('Work');

  useEffect(() => {
    let interval: any = null;
    if (isActive && timeLeft > 0) {
      interval = setInterval(() => {
        setTimeLeft(timeLeft - 1);
      }, 1000);
    } else if (timeLeft === 0) {
      setIsActive(false);
      // Trigger notification logic here if needed
    }
    return () => clearInterval(interval);
  }, [isActive, timeLeft]);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const progress = ((sessionType === 'Work' ? 25 * 60 : 5 * 60) - timeLeft) / (sessionType === 'Work' ? 25 * 60 : 5 * 60);

  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] animate-in zoom-in duration-500">
      <div className="max-w-xl w-full text-center space-y-12">
        <div className="space-y-2">
          <h2 className="text-3xl font-display font-bold text-slate-900 dark:text-white">Deep Work Protocol</h2>
          <p className="text-slate-500 dark:text-slate-400">Eliminate distractions. Maximize cognitive output.</p>
        </div>

        {/* Timer UI */}
        <div className="relative w-80 h-80 mx-auto flex items-center justify-center">
          {/* Progress Circle SVG */}
          <svg className="absolute inset-0 w-full h-full -rotate-90">
            <circle
              cx="160" cy="160" r="150"
              className="fill-none stroke-slate-200 dark:stroke-slate-800 stroke-[8]"
            />
            <circle
              cx="160" cy="160" r="150"
              className="fill-none stroke-indigo-600 stroke-[8] transition-all duration-1000 ease-linear"
              style={{
                strokeDasharray: '942.48',
                strokeDashoffset: 942.48 * (1 - progress)
              }}
            />
          </svg>

          <div className="relative z-10 flex flex-col items-center">
            <span className="text-6xl font-display font-bold text-slate-900 dark:text-white tabular-nums">
              {formatTime(timeLeft)}
            </span>
            <span className="text-sm font-bold text-indigo-500 uppercase tracking-widest mt-2">
              {sessionType} Mode
            </span>
          </div>

          {/* Particle animations could go here */}
        </div>

        {/* Controls */}
        <div className="flex justify-center items-center gap-6">
          <button 
            onClick={() => {
              setTimeLeft(sessionType === 'Work' ? 25 * 60 : 5 * 60);
              setIsActive(false);
            }}
            className="p-4 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-500 hover:text-indigo-500 transition-all"
          >
            <RotateCcw className="w-6 h-6" />
          </button>

          <button 
            onClick={() => setIsActive(!isActive)}
            className="w-20 h-20 rounded-full bg-indigo-600 flex items-center justify-center text-white shadow-xl shadow-indigo-600/30 hover:scale-105 active:scale-95 transition-all"
          >
            {isActive ? <Pause className="w-8 h-8 fill-current" /> : <Play className="w-8 h-8 fill-current translate-x-0.5" />}
          </button>

          <button className="p-4 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-500 hover:text-rose-500 transition-all">
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Status Indicators */}
        <div className="grid grid-cols-3 gap-4">
          <StatusBadge icon={<ShieldCheck className="w-4 h-4" />} label="Firewall Active" active={isActive} />
          <StatusBadge icon={<BellOff className="w-4 h-4" />} label="DND Mode" active={isActive} />
          <StatusBadge icon={<Moon className="w-4 h-4" />} label="Night Shift" active={true} />
        </div>
      </div>
    </div>
  );
};

const StatusBadge = ({ icon, label, active }: any) => (
  <div className={`flex flex-col items-center gap-2 p-4 rounded-2xl border transition-all ${
    active ? 'border-indigo-500/30 bg-indigo-50/50 dark:bg-indigo-500/10' : 'border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 opacity-50'
  }`}>
    <div className={`p-2 rounded-lg ${active ? 'text-indigo-600 dark:text-indigo-400' : 'text-slate-400'}`}>
      {icon}
    </div>
    <span className="text-[10px] font-bold uppercase tracking-tighter text-slate-500">{label}</span>
  </div>
);

export default FocusMode;
