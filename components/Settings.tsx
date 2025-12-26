/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/
import React from 'react';
import { 
  Sun, 
  Moon, 
  Bell, 
  Shield, 
  Trash2, 
  Cloud,
  ChevronRight,
  Monitor
} from 'lucide-react';

interface SettingsProps {
  isDarkMode: boolean;
  setIsDarkMode: (val: boolean) => void;
}

const Settings: React.FC<SettingsProps> = ({ isDarkMode, setIsDarkMode }) => {
  return (
    <div className="max-w-4xl space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 divide-y divide-slate-100 dark:divide-slate-800">
        <SectionHeader title="Appearance" />
        
        <div className="p-6 flex items-center justify-between group">
          <div className="flex items-center gap-4">
            <div className="p-2.5 bg-indigo-50 dark:bg-indigo-500/10 rounded-xl text-indigo-600">
              <Monitor className="w-5 h-5" />
            </div>
            <div>
              <h4 className="font-bold text-slate-800 dark:text-white">Dark Mode</h4>
              <p className="text-xs text-slate-500">Adjust the visual environment of the workspace.</p>
            </div>
          </div>
          <button 
            onClick={() => setIsDarkMode(!isDarkMode)}
            className={`w-14 h-8 rounded-full p-1 transition-all duration-300 ${isDarkMode ? 'bg-indigo-600' : 'bg-slate-200'}`}
          >
            <div className={`w-6 h-6 rounded-full bg-white shadow-sm flex items-center justify-center transition-all ${isDarkMode ? 'translate-x-6' : 'translate-x-0'}`}>
              {isDarkMode ? <Moon className="w-3.5 h-3.5 text-indigo-600" /> : <Sun className="w-3.5 h-3.5 text-amber-500" />}
            </div>
          </button>
        </div>

        <SectionHeader title="System & Sync" />

        <SettingsRow 
          icon={<Bell className="text-slate-400" />} 
          title="Notifications" 
          description="Control how and when you receive distraction alerts." 
        />
        <SettingsRow 
          icon={<Cloud className="text-slate-400" />} 
          title="Cloud Backup" 
          description="Last synced 12 minutes ago." 
          value="Enabled" 
        />
        <SettingsRow 
          icon={<Shield className="text-slate-400" />} 
          title="Privacy Settings" 
          description="Manage tracking permissions and data history." 
        />

        <div className="p-6">
          <button className="flex items-center gap-3 text-rose-500 font-bold text-sm hover:underline">
            <Trash2 className="w-5 h-5" />
            <span>Delete Account and Data</span>
          </button>
        </div>
      </div>

      <div className="p-8 bg-indigo-600 rounded-3xl text-white relative overflow-hidden">
        <div className="absolute top-0 right-0 p-4 opacity-10">
          <Zap className="w-40 h-40 fill-current" />
        </div>
        <div className="relative z-10 space-y-4">
          <h3 className="text-xl font-display font-bold">FocusFlow Pro</h3>
          <p className="text-indigo-100 text-sm max-w-sm">Unlock advanced time-series modeling, unlimited focus projects, and team collaboration tools.</p>
          <button className="bg-white text-indigo-600 px-6 py-2.5 rounded-xl font-bold text-sm shadow-xl shadow-black/10 hover:bg-indigo-50 transition-colors">
            Upgrade Now
          </button>
        </div>
      </div>
    </div>
  );
};

const SectionHeader = ({ title }: { title: string }) => (
  <div className="px-6 py-4 bg-slate-50 dark:bg-slate-800/30">
    <h3 className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">{title}</h3>
  </div>
);

const SettingsRow = ({ icon, title, description, value }: any) => (
  <div className="p-6 flex items-center justify-between hover:bg-slate-50 dark:hover:bg-slate-800 transition-all cursor-pointer group">
    <div className="flex items-center gap-4">
      <div className="p-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-400 group-hover:text-indigo-500 transition-colors">
        {icon}
      </div>
      <div>
        <h4 className="font-bold text-slate-800 dark:text-white">{title}</h4>
        <p className="text-xs text-slate-500">{description}</p>
      </div>
    </div>
    <div className="flex items-center gap-3">
      {value && <span className="text-xs font-bold text-slate-400">{value}</span>}
      <ChevronRight className="w-5 h-5 text-slate-300 group-hover:text-indigo-500" />
    </div>
  </div>
);

const Zap = ({ className }: { className: string }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M13 2L3 14H12V22L22 10H13V2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

export default Settings;
