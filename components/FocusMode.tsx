/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React, { useState, useEffect, useRef } from 'react';
import { focusApi } from '../services/api';
import { Play, Pause, RotateCcw, ShieldCheck, Moon, BellOff, X, CheckCircle2 } from 'lucide-react';

const FocusMode: React.FC = () => {
  const [timeLeft, setTimeLeft] = useState(25 * 60);
  const [isActive, setIsActive] = useState(false);
  const [sessionType, setSessionType] = useState<'Work' | 'Break'>('Work');
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null);
  const [sessionCompleted, setSessionCompleted] = useState(false);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    // Check for active session on mount
    const checkActiveSession = async () => {
      try {
        const { active, session } = await focusApi.getActiveSession();
        if (active && session) {
          setCurrentSessionId(session.id);
          setIsActive(true);
          // Calculate remaining time
          const elapsed = (Date.now() - new Date(session.start_time).getTime()) / 1000;
          const remaining = Math.max(0, session.planned_duration * 60 - elapsed);
          setTimeLeft(Math.floor(remaining));
        }
      } catch (error) {
        console.error('Failed to check active session:', error);
      }
    };

    checkActiveSession();
  }, []);

  useEffect(() => {
    if (isActive && timeLeft > 0) {
      timerRef.current = setInterval(() => {
        setTimeLeft(prev => {
          if (prev <= 1) {
            handleSessionComplete();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    } else if (timerRef.current) {
      clearInterval(timerRef.current);
    }

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [isActive]);

  const handleSessionComplete = async () => {
    setIsActive(false);
    setSessionCompleted(true);

    if (currentSessionId) {
      try {
        await focusApi.endSession(true);
        setCurrentSessionId(null);
      } catch (error) {
        console.error('Failed to end session:', error);
      }
    }

    // Auto-hide completion message
    setTimeout(() => setSessionCompleted(false), 3000);
  };

  const handleStart = async () => {
    try {
      const duration = sessionType === 'Work' ? 25 : 5;
      const { session } = await focusApi.startSession(duration);
      setCurrentSessionId(session.id);
      setIsActive(true);
      setTimeLeft(duration * 60);
      setSessionCompleted(false);
    } catch (error: any) {
      console.error('Failed to start session:', error);
      // If there's already an active session, just resume the timer
      if (error.message.includes('already have an active')) {
        setIsActive(true);
      }
    }
  };

  const handlePause = async () => {
    setIsActive(false);
  };

  const handleStop = async () => {
    setIsActive(false);
    setTimeLeft(sessionType === 'Work' ? 25 * 60 : 5 * 60);

    if (currentSessionId) {
      try {
        await focusApi.endSession(false);
        setCurrentSessionId(null);
      } catch (error) {
        console.error('Failed to end session:', error);
      }
    }
  };

  const handleReset = () => {
    setIsActive(false);
    setTimeLeft(sessionType === 'Work' ? 25 * 60 : 5 * 60);
    setCurrentSessionId(null);
    setSessionCompleted(false);
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const totalSeconds = sessionType === 'Work' ? 25 * 60 : 5 * 60;
  const progress = (totalSeconds - timeLeft) / totalSeconds;

  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] animate-in zoom-in duration-500">
      {sessionCompleted && (
        <div className="fixed top-4 right-4 bg-emerald-500 text-white px-6 py-3 rounded-2xl shadow-lg flex items-center gap-2 animate-in slide-in-from-right duration-300">
          <CheckCircle2 className="w-5 h-5" />
          <span className="font-bold">Focus session completed!</span>
        </div>
      )}

      <div className="max-w-xl w-full text-center space-y-12">
        <div className="space-y-2">
          <h2 className="text-3xl font-display font-bold text-slate-900 dark:text-white">Deep Work Protocol</h2>
          <p className="text-slate-500 dark:text-slate-400">Eliminate distractions. Maximize cognitive output.</p>
        </div>

        {/* Session Type Toggle */}
        <div className="flex justify-center gap-2">
          <button
            onClick={() => { if (!isActive) { setSessionType('Work'); setTimeLeft(25 * 60); } }}
            className={`px-6 py-2 rounded-xl font-bold transition-all ${sessionType === 'Work'
              ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/20'
              : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400'
              }`}
          >
            Work (25m)
          </button>
          <button
            onClick={() => { if (!isActive) { setSessionType('Break'); setTimeLeft(5 * 60); } }}
            className={`px-6 py-2 rounded-xl font-bold transition-all ${sessionType === 'Break'
              ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-600/20'
              : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400'
              }`}
          >
            Break (5m)
          </button>
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
              className={`fill-none stroke-[8] transition-all duration-1000 ease-linear ${sessionType === 'Work' ? 'stroke-indigo-600' : 'stroke-emerald-600'
                }`}
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
            <span className={`text-sm font-bold uppercase tracking-widest mt-2 ${sessionType === 'Work' ? 'text-indigo-500' : 'text-emerald-500'
              }`}>
              {sessionType} Mode
            </span>
          </div>
        </div>

        {/* Controls */}
        <div className="flex justify-center items-center gap-6">
          <button
            onClick={handleReset}
            className="p-4 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-500 hover:text-indigo-500 transition-all"
          >
            <RotateCcw className="w-6 h-6" />
          </button>

          <button
            onClick={isActive ? handlePause : handleStart}
            className={`w-20 h-20 rounded-full flex items-center justify-center text-white shadow-xl hover:scale-105 active:scale-95 transition-all ${sessionType === 'Work'
              ? 'bg-indigo-600 shadow-indigo-600/30'
              : 'bg-emerald-600 shadow-emerald-600/30'
              }`}
          >
            {isActive ? <Pause className="w-8 h-8 fill-current" /> : <Play className="w-8 h-8 fill-current translate-x-0.5" />}
          </button>

          <button
            onClick={handleStop}
            className="p-4 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-500 hover:text-rose-500 transition-all"
          >
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
  <div className={`flex flex-col items-center gap-2 p-4 rounded-2xl border transition-all ${active ? 'border-indigo-500/30 bg-indigo-50/50 dark:bg-indigo-500/10' : 'border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 opacity-50'
    }`}>
    <div className={`p-2 rounded-lg ${active ? 'text-indigo-600 dark:text-indigo-400' : 'text-slate-400'}`}>
      {icon}
    </div>
    <span className="text-[10px] font-bold uppercase tracking-tighter text-slate-500">{label}</span>
  </div>
);

export default FocusMode;
