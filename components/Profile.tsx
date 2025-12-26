/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/
import React from 'react';
import { UserProfile } from '../types';
import { 
  User, 
  Mail, 
  Settings, 
  Shield, 
  Zap, 
  TrendingUp,
  Award,
  Edit2,
  ExternalLink
} from 'lucide-react';

interface ProfileProps {
  user: UserProfile | null;
}

const Profile: React.FC<ProfileProps> = ({ user }) => {
  if (!user) return null;

  return (
    <div className="max-w-4xl space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      
      {/* Profile Header */}
      <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-8 shadow-sm relative overflow-hidden">
        <div className="absolute top-0 right-0 p-8 opacity-5">
          <User className="w-48 h-48" />
        </div>
        
        <div className="relative z-10 flex flex-col md:flex-row items-center gap-8">
          <div className="w-32 h-32 rounded-[2rem] bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white text-4xl font-display font-bold shadow-2xl shadow-indigo-500/30 ring-4 ring-white dark:ring-slate-800">
            {user.name[0]}
          </div>
          <div className="flex-1 text-center md:text-left">
            <h2 className="text-3xl font-display font-bold text-slate-900 dark:text-white mb-2">{user.name}</h2>
            <div className="flex flex-wrap items-center justify-center md:justify-start gap-4">
              <div className="flex items-center gap-2 text-sm text-slate-500">
                <Mail className="w-4 h-4" />
                {user.email}
              </div>
              <div className="flex items-center gap-2 text-sm text-indigo-500 font-bold bg-indigo-50 dark:bg-indigo-500/10 px-3 py-1 rounded-full uppercase tracking-widest">
                <Zap className="w-3 h-3" />
                {user.style} Style
              </div>
            </div>
          </div>
          <button className="flex items-center gap-2 px-6 py-3 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl text-sm font-bold hover:bg-slate-50 transition-all shadow-sm">
            <Edit2 className="w-4 h-4" />
            Edit Profile
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Achievement Card */}
        <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-8 shadow-sm">
          <div className="flex items-center gap-4 mb-6">
             <div className="p-3 bg-amber-50 dark:bg-amber-500/10 rounded-2xl text-amber-500">
               <Award className="w-6 h-6" />
             </div>
             <h3 className="font-display font-bold text-slate-900 dark:text-white">Productivity Achievements</h3>
          </div>
          <div className="space-y-4">
            <AchievementItem title="Deep Work Legend" description="Completed 10 focus sessions over 90 mins" status="Unlocked" />
            <AchievementItem title="Deadline Master" description="20 tasks completed before their deadline" status="90%" />
            <AchievementItem title="Early Bird" description="Most productive before 10:00 AM" status="Unlocked" />
          </div>
        </div>

        {/* Security & Access */}
        <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-8 shadow-sm">
           <div className="flex items-center gap-4 mb-6">
             <div className="p-3 bg-emerald-50 dark:bg-emerald-500/10 rounded-2xl text-emerald-500">
               <Shield className="w-6 h-6" />
             </div>
             <h3 className="font-display font-bold text-slate-900 dark:text-white">Privacy & Security</h3>
          </div>
          <div className="space-y-4">
            <SecurityItem title="Two-Factor Auth" status="Disabled" />
            <SecurityItem title="Session History" status="View logs" icon={<ExternalLink className="w-4 h-4" />} />
            <SecurityItem title="Data Portability" status="Export Data" icon={<TrendingUp className="w-4 h-4" />} />
          </div>
        </div>
      </div>

      {/* Stats Summary */}
      <div className="bg-slate-900 rounded-[2.5rem] p-10 text-white relative overflow-hidden shadow-2xl">
         <div className="absolute inset-0 bg-gradient-to-br from-indigo-900/40 via-transparent to-transparent"></div>
         <div className="relative z-10">
            <h3 className="text-xl font-display font-bold mb-10 flex items-center gap-3">
              <TrendingUp className="text-indigo-400" />
              Usage Intelligence Summary
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              <StatItem label="Total Tasks" value="142" />
              <StatItem label="Focus Hours" value="328h" />
              <StatItem label="Avg Efficiency" value="88%" />
              <StatItem label="Current Rank" value="Elite" />
            </div>
         </div>
      </div>
    </div>
  );
};

const AchievementItem = ({ title, description, status }: any) => (
  <div className="flex items-center justify-between p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/50">
    <div>
      <h5 className="font-bold text-slate-800 dark:text-slate-200 text-sm">{title}</h5>
      <p className="text-[10px] text-slate-500">{description}</p>
    </div>
    <span className={`text-[10px] font-bold uppercase tracking-widest px-2 py-1 rounded-lg ${
      status === 'Unlocked' ? 'bg-emerald-50 dark:bg-emerald-500/10 text-emerald-600' : 'bg-slate-200 dark:bg-slate-700 text-slate-500'
    }`}>
      {status}
    </span>
  </div>
);

const SecurityItem = ({ title, status, icon }: any) => (
  <button className="w-full flex items-center justify-between p-4 rounded-2xl hover:bg-slate-50 dark:hover:bg-slate-800 transition-all border border-transparent hover:border-slate-100 dark:hover:border-slate-800">
    <span className="font-bold text-slate-700 dark:text-slate-300 text-sm">{title}</span>
    <div className="flex items-center gap-2 text-xs font-bold text-slate-400">
      {status}
      {icon}
    </div>
  </button>
);

const StatItem = ({ label, value }: any) => (
  <div className="space-y-1">
    <p className="text-[10px] font-bold text-indigo-400 uppercase tracking-widest">{label}</p>
    <p className="text-3xl font-display font-bold">{value}</p>
  </div>
);

export default Profile;
