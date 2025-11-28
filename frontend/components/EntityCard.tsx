import React from 'react';

interface EntityCardProps {
  title: string;
  icon: React.ReactElement;
  items: string[];
  emptyMessage?: string;
}

export default function EntityCard({ title, icon, items, emptyMessage = 'No data found' }: EntityCardProps) {
  return (
    <div className="bg-gradient-to-br from-neutral-900/60 to-neutral-900/40 border border-neutral-800 rounded-2xl p-6 backdrop-blur-sm hover:border-neutral-700 transition-all duration-300">
      <div className="flex items-center gap-3 mb-4">
        <div className="p-2 bg-neutral-800/50 rounded-lg">
          {React.cloneElement(icon as React.ReactElement<any>, { className: 'w-5 h-5' })}
        </div>
        <h3 className="font-semibold text-white">{title}</h3>
        <span className="ml-auto text-xs font-medium text-neutral-500 bg-neutral-800/50 px-2 py-1 rounded">
          {items.length}
        </span>
      </div>
      <div className="space-y-2 max-h-64 overflow-y-auto custom-scrollbar">
        {items.length > 0 ? (
          items.map((item, index) => (
            <div key={`${item}-${index}`} className="flex items-center gap-2 text-sm text-neutral-300 bg-neutral-950/50 p-2.5 rounded-lg border border-neutral-800/50 hover:border-neutral-700 transition-colors">
              <div className="w-1.5 h-1.5 rounded-full bg-neutral-600 flex-shrink-0" />
              <span className="break-all">{item}</span>
            </div>
          ))
        ) : (
          <div className="text-neutral-500 text-sm italic text-center py-4">{emptyMessage}</div>
        )}
      </div>
    </div>
  );
}
