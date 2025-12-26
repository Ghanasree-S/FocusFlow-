/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/
import React, { useState } from 'react';
import { 
  Zap, 
  Target, 
  ShieldCheck, 
  Clock, 
  ArrowRight, 
  CheckCircle2,
  Settings,
  BrainCircuit
} from 'lucide-react';

interface OnboardingProps {
  onComplete: () => void;
}

const Onboarding: React.FC<OnboardingProps> = ({ onComplete }) => {
  const [step, setStep] = useState(1);
  const [style, setStyle] = useState<'Balanced' | 'High-focus' | 'Flexible'>('Balanced');

  const nextStep = () => {
    if (step < 4) setStep(step + 1);
    else onComplete();
  };

  const renderStep = () => {
    switch (step) {
      case 1:
        return (
          <div className="space-y-8 animate-in fade-in slide-in-from-bottom-8 duration-700">
            <div className="text-center">
              <div className="w-20 h-20 bg-indigo-600 rounded-3xl mx-auto flex items-center justify-center text-white shadow-2xl shadow-indigo-600/30 mb-8">
                <Zap className="w-12 h-12 fill-current" />
              </div>
              <h2 className="text-3xl font-display font-bold text-slate-900 dark:text-white mb-4">Welcome to FocusFlow</h2>
              <p className="text-slate-500 dark:text-slate-400 max-w-sm mx-auto">
                The intelligent productivity system that learns your patterns to help you reach peak performance.
              </p>
            </div>
            <div className="grid grid-cols-1 gap-4">
               <FeatureItem icon={<BrainCircuit className="text-indigo-500" />} text="ML-Based Productivity Forecasting" />
               <FeatureItem icon={<Target className="text-emerald-500" />} text="Deep Work Focused Task Manager" />
               <FeatureItem icon={<ShieldCheck className="text-rose-500" />} text="Distraction Blocking Protocols" />
            </div>
          </div>
        );
      case 2:
        return (
          <div className="space-y-8 animate-in fade-in slide-in-from-bottom-8 duration-700">
            <div className="text-center">
              <h2 className="text-3xl font-display font-bold text-slate-900 dark:text-white mb-4">Choose Your Style</h2>
              <p className="text-slate-500 dark:text-slate-400 max-w-sm mx-auto">
                How do you prefer to tackle your daily tasks?
              </p>
            </div>
            <div className="grid grid-cols-1 gap-3">
              {(['Balanced', 'High-focus', 'Flexible'] as const).map(s => (
                <button 
                  key={s}
                  onClick={() => setStyle(s)}
                  className={`flex items-center gap-4 p-5 rounded-2xl border transition-all text-left ${
                    style === s ? 'border-indigo-600 bg-indigo-50 dark:bg-indigo-500/10 ring-4 ring-indigo-500/10' : 'border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-900'
                  }`}
                >
                  <div className={`p-3 rounded-xl ${style === s ? 'bg-indigo-600 text-white' : 'bg-slate-100 dark:bg-slate-800 text-slate-500'}`}>
                    {s === 'Balanced' ? <Clock className="w-5 h-5" /> : s === 'High-focus' ? <Zap className="w-5 h-5" /> : <Settings className="w-5 h-5" />}
                  </div>
                  <div>
                    <h4 className="font-bold text-slate-800 dark:text-white">{s}</h4>
                    <p className="text-xs text-slate-500">Best for {s === 'Balanced' ? 'steady daily progress' : s === 'High-focus' ? 'intense deep work blocks' : 'dynamic schedules'}.</p>
                  </div>
                  {style === s && <CheckCircle2 className="ml-auto w-6 h-6 text-indigo-600" />}
                </button>
              ))}
            </div>
          </div>
        );
      case 3:
        return (
          <div className="space-y-8 animate-in fade-in slide-in-from-bottom-8 duration-700">
            <div className="text-center">
              <h2 className="text-3xl font-display font-bold text-slate-900 dark:text-white mb-4">Tracking Permissions</h2>
              <p className="text-slate-500 dark:text-slate-400 max-w-sm mx-auto">
                FocusFlow needs basic usage data to build your personal productivity model.
              </p>
            </div>
            <div className="bg-slate-50 dark:bg-slate-900 p-6 rounded-3xl border border-slate-200 dark:border-slate-800">
               <ul className="space-y-4">
                 <li className="flex gap-4">
                   <div className="shrink-0 w-8 h-8 rounded-full bg-emerald-100 dark:bg-emerald-500/20 text-emerald-600 flex items-center justify-center">
                     <CheckCircle2 className="w-5 h-5" />
                   </div>
                   <p className="text-sm text-slate-600 dark:text-slate-400"><strong>Screen Time:</strong> Identify peak activity periods.</p>
                 </li>
                 <li className="flex gap-4">
                   <div className="shrink-0 w-8 h-8 rounded-full bg-emerald-100 dark:bg-emerald-500/20 text-emerald-600 flex items-center justify-center">
                     <CheckCircle2 className="w-5 h-5" />
                   </div>
                   <p className="text-sm text-slate-600 dark:text-slate-400"><strong>App Categorization:</strong> Distinguish work from play.</p>
                 </li>
                 <li className="flex gap-4">
                   <div className="shrink-0 w-8 h-8 rounded-full bg-emerald-100 dark:bg-emerald-500/20 text-emerald-600 flex items-center justify-center">
                     <CheckCircle2 className="w-5 h-5" />
                   </div>
                   <p className="text-sm text-slate-600 dark:text-slate-400"><strong>Notifications:</strong> Block distractions during focus mode.</p>
                 </li>
               </ul>
            </div>
          </div>
        );
      case 4:
        return (
          <div className="space-y-8 animate-in fade-in slide-in-from-bottom-8 duration-700">
            <div className="text-center">
              <h2 className="text-3xl font-display font-bold text-slate-900 dark:text-white mb-4">Almost Ready!</h2>
              <p className="text-slate-500 dark:text-slate-400 max-w-sm mx-auto">
                Your workspace is being calibrated to your {style} style.
              </p>
            </div>
            <div className="flex flex-col items-center justify-center py-12">
               <div className="w-24 h-24 border-4 border-slate-200 dark:border-slate-800 border-t-indigo-600 rounded-full animate-spin"></div>
               <p className="mt-6 text-sm font-bold text-slate-400 uppercase tracking-widest animate-pulse">Initializing Neural Engine...</p>
            </div>
          </div>
        );
      default: return null;
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-slate-50 dark:bg-slate-950">
      <div className="max-w-md w-full bg-white dark:bg-slate-900 p-8 rounded-[40px] border border-slate-200 dark:border-slate-800 shadow-xl flex flex-col min-h-[580px]">
        
        <div className="flex-1">
          {renderStep()}
        </div>

        <div className="mt-12 flex flex-col gap-4">
          <div className="flex justify-center gap-1.5 mb-2">
            {[1, 2, 3, 4].map(i => (
              <div key={i} className={`h-1.5 rounded-full transition-all duration-300 ${step === i ? 'w-8 bg-indigo-600' : 'w-1.5 bg-slate-200 dark:bg-slate-800'}`}></div>
            ))}
          </div>
          <button 
            onClick={nextStep}
            className="w-full py-4 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-2xl shadow-lg shadow-indigo-600/20 flex items-center justify-center gap-2 transition-all active:scale-95"
          >
            <span>{step === 4 ? 'Finish Setup' : 'Continue'}</span>
            <ArrowRight className="w-5 h-5" />
          </button>
          {step < 4 && (
            <button onClick={onComplete} className="text-slate-400 text-xs font-bold uppercase tracking-widest hover:text-slate-600 dark:hover:text-slate-200 transition-colors">
              Skip for now
            </button>
          )}
        </div>

      </div>
    </div>
  );
};

const FeatureItem = ({ icon, text }: any) => (
  <div className="flex items-center gap-4 p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/50 border border-transparent">
    <div className="p-2.5 bg-white dark:bg-slate-900 rounded-xl shadow-sm border border-slate-100 dark:border-slate-800">
      {icon}
    </div>
    <span className="text-sm font-semibold text-slate-700 dark:text-slate-300">{text}</span>
  </div>
);

export default Onboarding;
