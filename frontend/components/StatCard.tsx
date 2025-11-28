import React from 'react';

interface StatCardProps {
  icon: React.ReactElement;
  label: string;
  value: string | number;
  color?: string;
}

export default function StatCard({ icon, label, value, color = 'neutral' }: StatCardProps) {
  const colorClasses = {
    neutral: 'bg-neutral-800/50 text-neutral-400 group-hover:text-neutral-200',
    blue: 'bg-blue-500/10 text-blue-400 group-hover:text-blue-300',
    green: 'bg-green-500/10 text-green-400 group-hover:text-green-300',
    purple: 'bg-purple-500/10 text-purple-400 group-hover:text-purple-300',
  };

  const borderClasses = {
    neutral: 'group-hover:border-neutral-600',
    blue: 'group-hover:border-blue-500/50',
    green: 'group-hover:border-green-500/50',
    purple: 'group-hover:border-purple-500/50',
  };

  return (
    <div className={`bg-neutral-900/40 border border-neutral-800 rounded-xl p-5 flex items-center gap-4 transition-all duration-300 hover:scale-[1.02] hover:shadow-xl backdrop-blur-sm group ${borderClasses[color as keyof typeof borderClasses] || borderClasses.neutral}`}>
      <div className={`p-3.5 rounded-xl transition-colors ${colorClasses[color as keyof typeof colorClasses] || colorClasses.neutral}`}>
        {React.cloneElement(icon as React.ReactElement<{ className?: string }>, { className: 'w-6 h-6' })}
      </div>
      <div>
        <div className="text-2xl font-bold text-white tracking-tight">{value}</div>
        <div className="text-xs text-neutral-500 uppercase tracking-wider font-medium group-hover:text-neutral-400 transition-colors">{label}</div>
      </div>
    </div>
  );
}
