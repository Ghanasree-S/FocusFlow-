/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/
import React from 'react';
import { 
  FileText, 
  Download, 
  Share2, 
  Calendar,
  CheckCircle2,
  TrendingUp,
  AlertCircle
} from 'lucide-react';

const Reports: React.FC = () => {
  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-xl font-display font-bold text-slate-900 dark:text-white">Performance Reports</h2>
          <p className="text-sm text-slate-500">Historical review and long-term trend analysis.</p>
        </div>
        <div className="flex gap-2">
          <button className="flex items-center gap-2 px-4 py-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm font-bold shadow-sm hover:bg-slate-50">
            <Calendar className="w-4 h-4" />
            <span>This Month</span>
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-xl text-sm font-bold shadow-lg shadow-indigo-600/20 hover:bg-indigo-700">
            <Download className="w-4 h-4" />
            <span>Export to CSV</span>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <ReportCard 
          title="Completion Velocity" 
          value="4.2 tasks/day" 
          description="Average throughput this month" 
          icon={<TrendingUp className="text-emerald-500" />} 
          trend="+0.8 from Oct"
        />
        <ReportCard 
          title="Deep Work Volume" 
          value="28h 12m" 
          description="Total focus time in sessions" 
          icon={<CheckCircle2 className="text-indigo-500" />} 
          trend="Consistent"
        />
        <ReportCard 
          title="Distraction Cost" 
          value="12h 05m" 
          description="Estimated productivity lost" 
          icon={<AlertCircle className="text-rose-500" />} 
          trend="-15% reduction"
        />
      </div>

      <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-8">
        <h3 className="font-display font-bold text-slate-900 dark:text-white mb-8">Generated Summaries</h3>
        <div className="space-y-4">
          <ReportListItem title="Weekly Productivity Summary - Nov 13-19" date="Nov 20, 2023" type="Weekly" />
          <ReportListItem title="Monthly Behavior Analysis - October 2023" date="Oct 31, 2023" type="Monthly" />
          <ReportListItem title="Yearly Target Forecasting Q4" date="Sep 15, 2023" type="Custom" />
        </div>
      </div>
    </div>
  );
};

const ReportCard = ({ title, value, description, icon, trend }: any) => (
  <div className="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm">
    <div className="flex justify-between items-start mb-4">
      <div className="p-2.5 bg-slate-50 dark:bg-slate-800 rounded-xl">{icon}</div>
      <span className="text-[10px] font-bold text-indigo-500 bg-indigo-50 dark:bg-indigo-500/10 px-2 py-0.5 rounded-full">{trend}</span>
    </div>
    <h4 className="text-2xl font-display font-bold text-slate-900 dark:text-white mb-1">{value}</h4>
    <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">{title}</p>
    <p className="text-[10px] text-slate-400 mt-2">{description}</p>
  </div>
);

const ReportListItem = ({ title, date, type }: any) => (
  <div className="group flex items-center justify-between p-4 rounded-2xl border border-slate-100 dark:border-slate-800 hover:border-indigo-500/30 hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-all cursor-pointer">
    <div className="flex items-center gap-4">
      <div className="p-3 bg-white dark:bg-slate-900 rounded-xl border border-slate-100 dark:border-slate-800 shadow-sm">
        <FileText className="w-5 h-5 text-indigo-500" />
      </div>
      <div>
        <h5 className="font-bold text-slate-800 dark:text-slate-200">{title}</h5>
        <div className="flex items-center gap-3 text-xs text-slate-400">
          <span>{date}</span>
          <span className="w-1 h-1 rounded-full bg-slate-300"></span>
          <span>{type} Report</span>
        </div>
      </div>
    </div>
    <div className="flex items-center gap-2">
      <button className="p-2 text-slate-400 hover:text-indigo-500 transition-colors">
        <Share2 className="w-5 h-5" />
      </button>
      <button className="p-2 text-slate-400 hover:text-indigo-500 transition-colors">
        <Download className="w-5 h-5" />
      </button>
    </div>
  </div>
);

export default Reports;
