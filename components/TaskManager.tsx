/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/
import React, { useState } from 'react';
import { Task } from '../types';
import { 
  Search, 
  Filter, 
  Plus, 
  MoreVertical, 
  Clock, 
  CheckCircle2, 
  Circle,
  Calendar,
  Layers
} from 'lucide-react';

interface TaskManagerProps {
  tasks: Task[];
  setTasks: (tasks: Task[]) => void;
}

const TaskManager: React.FC<TaskManagerProps> = ({ tasks, setTasks }) => {
  const [filter, setFilter] = useState<'All' | 'Today' | 'Upcoming' | 'Completed'>('All');
  const [searchQuery, setSearchQuery] = useState('');

  const toggleTask = (id: string) => {
    setTasks(tasks.map(t => t.id === id ? { ...t, completed: !t.completed, progress: !t.completed ? 100 : 0 } : t));
  };

  const filteredTasks = tasks.filter(t => {
    const matchesSearch = t.title.toLowerCase().includes(searchQuery.toLowerCase());
    if (filter === 'Completed') return t.completed && matchesSearch;
    if (filter === 'All') return matchesSearch;
    return !t.completed && matchesSearch;
  });

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
      {/* Search & Actions Bar */}
      <div className="flex flex-col md:flex-row gap-4 items-center">
        <div className="relative flex-1 w-full">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input 
            type="text" 
            placeholder="Search tasks, categories..." 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-11 pr-4 py-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all outline-none"
          />
        </div>
        <div className="flex gap-2 w-full md:w-auto">
          <button className="flex items-center gap-2 px-4 py-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl hover:bg-slate-50 dark:hover:bg-slate-800 transition-all text-sm font-medium">
            <Filter className="w-4 h-4" />
            <span>Filter</span>
          </button>
          <button className="flex-1 md:flex-none flex items-center justify-center gap-2 px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl shadow-lg shadow-indigo-600/20 transition-all font-bold">
            <Plus className="w-5 h-5" />
            <span>Add Task</span>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Left: Filter Sidebar */}
        <div className="lg:col-span-1 space-y-2">
          <h3 className="px-4 text-[10px] font-bold text-slate-500 uppercase tracking-[0.2em] mb-4">View</h3>
          {(['All', 'Today', 'Upcoming', 'Completed'] as const).map((item) => (
            <button
              key={item}
              onClick={() => setFilter(item)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
                filter === item 
                ? 'bg-indigo-50 dark:bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 font-bold' 
                : 'text-slate-600 dark:text-slate-400 hover:bg-white dark:hover:bg-slate-900'
              }`}
            >
              {item === 'All' && <Layers className="w-4 h-4" />}
              {item === 'Today' && <Clock className="w-4 h-4" />}
              {item === 'Upcoming' && <Calendar className="w-4 h-4" />}
              {item === 'Completed' && <CheckCircle2 className="w-4 h-4" />}
              <span className="text-sm">{item}</span>
              <span className="ml-auto text-[10px] opacity-60">
                {tasks.filter(t => {
                  if (item === 'All') return true;
                  if (item === 'Completed') return t.completed;
                  return !t.completed;
                }).length}
              </span>
            </button>
          ))}
          
          <div className="pt-8 px-4">
            <h3 className="text-[10px] font-bold text-slate-500 uppercase tracking-[0.2em] mb-4">Focus Projects</h3>
            <div className="space-y-4">
              <ProjectTag color="indigo" label="Work Automation" count={4} />
              <ProjectTag color="emerald" label="Personal Growth" count={2} />
              <ProjectTag color="amber" label="University Prep" count={12} />
            </div>
          </div>
        </div>

        {/* Right: Task List */}
        <div className="lg:col-span-3 space-y-4">
          <div className="flex justify-between items-center mb-2 px-2">
            <h2 className="font-display font-bold text-slate-900 dark:text-white">Active Tasks</h2>
            <span className="text-xs text-slate-400">{filteredTasks.length} tasks matching view</span>
          </div>
          
          <div className="space-y-3">
            {filteredTasks.map((task) => (
              <div 
                key={task.id} 
                className={`p-4 bg-white dark:bg-slate-900 rounded-2xl border transition-all group ${
                  task.completed ? 'opacity-60 border-transparent bg-slate-100 dark:bg-slate-800/30' : 'border-slate-200 dark:border-slate-800 hover:border-indigo-500/30 shadow-sm'
                }`}
              >
                <div className="flex items-center gap-4">
                  <button 
                    onClick={() => toggleTask(task.id)}
                    className={`shrink-0 transition-colors ${task.completed ? 'text-emerald-500' : 'text-slate-300 hover:text-indigo-500'}`}
                  >
                    {task.completed ? <CheckCircle2 className="w-6 h-6" /> : <Circle className="w-6 h-6" />}
                  </button>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <h4 className={`font-bold truncate text-slate-800 dark:text-slate-100 ${task.completed ? 'line-through' : ''}`}>
                        {task.title}
                      </h4>
                      <span className={`text-[9px] font-bold uppercase tracking-widest px-1.5 py-0.5 rounded ${
                        task.priority === 'High' ? 'bg-rose-100 text-rose-600' : 'bg-slate-100 text-slate-600'
                      }`}>
                        {task.priority}
                      </span>
                    </div>
                    <div className="flex items-center gap-4 text-[10px] text-slate-400">
                      <div className="flex items-center gap-1"><Layers className="w-3 h-3" /> {task.category}</div>
                      <div className="flex items-center gap-1"><Clock className="w-3 h-3" /> {task.deadline}</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="hidden md:flex flex-col items-end gap-1 w-24">
                      <span className="text-[10px] font-bold text-slate-500 uppercase">{task.progress}%</span>
                      <div className="w-full h-1 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                        <div className="h-full bg-indigo-500" style={{ width: `${task.progress}%` }}></div>
                      </div>
                    </div>
                    <button className="p-2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors">
                      <MoreVertical className="w-5 h-5" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
            
            {filteredTasks.length === 0 && (
              <div className="py-20 text-center space-y-4">
                <div className="w-20 h-20 bg-slate-100 dark:bg-slate-800 rounded-full mx-auto flex items-center justify-center text-slate-300">
                  <CheckCircle2 className="w-10 h-10" />
                </div>
                <div>
                  <h4 className="font-bold text-slate-600 dark:text-slate-400">All caught up!</h4>
                  <p className="text-sm text-slate-400">No tasks match your current filters.</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

const ProjectTag = ({ color, label, count }: any) => (
  <div className="flex items-center justify-between group cursor-pointer">
    <div className="flex items-center gap-2">
      <div className={`w-2.5 h-2.5 rounded-full bg-${color}-500 shadow-[0_0_8px_rgba(0,0,0,0.1)] group-hover:scale-125 transition-transform`}></div>
      <span className="text-sm font-medium text-slate-600 dark:text-slate-400 group-hover:text-slate-900 dark:group-hover:text-white transition-colors">{label}</span>
    </div>
    <span className="text-[10px] text-slate-400 font-mono">{count}</span>
  </div>
);

export default TaskManager;
