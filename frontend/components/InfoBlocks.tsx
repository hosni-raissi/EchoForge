'use client';

import { Layers, Database, Mail, Phone, Globe, Loader2, Scan } from 'lucide-react';
import { useState } from 'react';
import EntityCard from './EntityCard';
import SocialProfiles from './SocialProfiles';
import ResultCard from './ResultCard';

interface SearchResult {
  title: string;
  link: string;
  snippet: string;
  displayLink: string;
  relevance_score?: number;
  source?: string;
}

interface Entities {
  emails: string[];
  phones: string[];
  urls: string[];
  social_handles: Record<string, string[]>;
  dates: string[];
}

interface SearchResponse {
  metadata: {
    target: string;
    target_type: string;
    execution_time: number;
    total_results: number;
    dorks_executed: number;
  };
  aggregated_entities: Entities;
  top_results: SearchResult[];
}

interface InfoBlocksProps {
  data: SearchResponse | null;
  loading: boolean;
}

const capabilities = [
  {
    title: 'Deep Search Engine',
    description: 'Advanced dork generation & multi-source scanning',
  },
  {
    title: 'Entity Extraction',
    description: 'Automated parsing of emails, phones, and profiles',
  },
  {
    title: 'Real-time Analysis',
    description: 'Live data processing with relevance scoring',
  },
];

const outputs = [
  {
    title: 'Contact Information',
    description: 'Verified email addresses and phone numbers',
  },
  {
    title: 'Digital Footprint',
    description: 'Social media profiles and web presence',
  },
  {
    title: 'Source Metadata',
    description: 'Origin links, timestamps, and context snippets',
  },
];

export default function InfoBlocks({ data, loading }: InfoBlocksProps) {
  const [leftMousePosition, setLeftMousePosition] = useState({ x: 0, y: 0 });
  const [rightMousePosition, setRightMousePosition] = useState({ x: 0, y: 0 });

  const handleLeftMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    setLeftMousePosition({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    });
  };

  const handleRightMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    setRightMousePosition({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    });
  };

  const LoadingState = ({ color }: { color: 'blue' | 'green' }) => (
    <div className="h-full flex flex-col items-center justify-center relative overflow-hidden">
      <div className={`absolute inset-0 bg-${color}-500/5 animate-pulse`} />
      <div className="absolute inset-0 bg-[linear-gradient(to_bottom,transparent,rgba(255,255,255,0.05),transparent)] -translate-y-full animate-[scan_2s_ease-in-out_infinite]" />
      
      <div className="relative z-10 flex flex-col items-center gap-6">
        <div className="relative">
          <div className={`absolute inset-0 bg-${color}-500 blur-xl opacity-20 animate-pulse`} />
          <div className={`p-4 bg-${color}-500/10 rounded-2xl border border-${color}-500/20 shadow-lg shadow-${color}-500/10`}>
            <Loader2 className={`w-8 h-8 text-${color}-400 animate-spin`} />
          </div>
        </div>
        <div className="text-center space-y-2">
          <h3 className="text-xl font-bold text-white tracking-tight">
            {color === 'blue' ? 'Analyzing Sources' : 'Aggregating Data'}
          </h3>
          <div className="flex items-center gap-2 text-sm text-neutral-500">
            <Scan className="w-4 h-4" />
            <span className="animate-pulse">Scanning target footprint...</span>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
      {/* Left Block: System Capabilities or Entities */}
      <div 
        className="relative bg-neutral-900/40 border border-neutral-800 rounded-3xl p-8 backdrop-blur-md hover:border-blue-500/30 transition-all duration-500 group overflow-hidden h-[600px] flex flex-col shadow-2xl"
        onMouseMove={handleLeftMouseMove}
        style={{
          background: `radial-gradient(800px circle at ${leftMousePosition.x}px ${leftMousePosition.y}px, rgba(59, 130, 246, 0.08), transparent 40%)`,
        }}
      >
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808008_1px,transparent_1px),linear-gradient(to_bottom,#80808008_1px,transparent_1px)] bg-size-[32px_32px] -z-10" />
        <div className="absolute inset-0 bg-neutral-950/20 -z-20" />
        
        {loading ? (
          <LoadingState color="blue" />
        ) : data ? (
          <div className="h-full overflow-y-auto pr-2 space-y-6 scrollbar-thin scrollbar-thumb-neutral-700 scrollbar-track-transparent scrollbar-thumb-rounded-full hover:scrollbar-thumb-neutral-600">
            <div className="flex items-center gap-4 mb-6 sticky top-0 bg-neutral-900/90 backdrop-blur-xl p-3 rounded-2xl z-10 border border-neutral-800/50 shadow-lg">
              <div className="p-2.5 bg-blue-500/10 rounded-xl border border-blue-500/20">
                <Layers className="w-5 h-5 text-blue-400" />
              </div>
              <h3 className="font-bold text-white text-lg tracking-tight">Discovered Entities</h3>
              <span className="ml-auto text-xs font-bold text-blue-400 bg-blue-500/10 border border-blue-500/20 px-3 py-1.5 rounded-full">
                {data.aggregated_entities.emails.length + data.aggregated_entities.phones.length + Object.values(data.aggregated_entities.social_handles).flat().length} FOUND
              </span>
            </div>
            
            <div className="space-y-6 px-1">
              <EntityCard 
                title="Email Addresses" 
                icon={<Mail className="text-blue-400" />} 
                items={data.aggregated_entities.emails}
                emptyMessage="No emails discovered"
              />
              <EntityCard 
                title="Phone Numbers" 
                icon={<Phone className="text-green-400" />} 
                items={data.aggregated_entities.phones}
                emptyMessage="No phones discovered"
              />
              <SocialProfiles socialHandles={data.aggregated_entities.social_handles} />
            </div>
          </div>
        ) : (
          <>
            <div className="flex items-center gap-4 mb-10">
              <div className="p-3.5 bg-blue-500/10 rounded-2xl border border-blue-500/20 group-hover:border-blue-500/40 transition-colors shadow-lg shadow-blue-900/10">
                <Layers className="w-7 h-7 text-blue-400" />
              </div>
              <div>
                <h3 className="font-bold text-white text-2xl tracking-tight">System Capabilities</h3>
                <p className="text-neutral-500 text-sm mt-1">Core processing engine features</p>
              </div>
            </div>
            
            <div className="space-y-6 flex-1">
              {capabilities.map((item, index) => (
                <div key={item.title} className="flex items-start gap-5 group/item p-4 rounded-2xl hover:bg-white/5 transition-colors border border-transparent hover:border-white/5">
                  <div className="mt-2 w-2.5 h-2.5 rounded-full bg-blue-500 shrink-0 group-hover/item:scale-125 transition-transform shadow-[0_0_12px_rgba(59,130,246,0.6)]" />
                  <div>
                    <div className="text-xl font-medium text-neutral-200 group-hover/item:text-blue-300 transition-colors">{item.title}</div>
                    <div className="text-base text-neutral-500 mt-1.5 leading-relaxed">{item.description}</div>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </div>

      {/* Right Block: Intelligence Output or Feed */}
      <div 
        className="relative bg-neutral-900/40 border border-neutral-800 rounded-3xl p-8 backdrop-blur-md hover:border-green-500/30 transition-all duration-500 group overflow-hidden h-[600px] flex flex-col shadow-2xl"
        onMouseMove={handleRightMouseMove}
        style={{
          background: `radial-gradient(800px circle at ${rightMousePosition.x}px ${rightMousePosition.y}px, rgba(34, 197, 94, 0.08), transparent 40%)`,
        }}
      >
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808008_1px,transparent_1px),linear-gradient(to_bottom,#80808008_1px,transparent_1px)] bg-size-[32px_32px] -z-10" />
        <div className="absolute inset-0 bg-neutral-950/20 -z-20" />
        
        {loading ? (
          <LoadingState color="green" />
        ) : data ? (
          <div className="h-full overflow-y-auto pr-2 space-y-4 scrollbar-thin scrollbar-thumb-neutral-700 scrollbar-track-transparent scrollbar-thumb-rounded-full hover:scrollbar-thumb-neutral-600">
            <div className="flex items-center gap-4 mb-6 sticky top-0 bg-neutral-900/90 backdrop-blur-xl p-3 rounded-2xl z-10 border border-neutral-800/50 shadow-lg">
              <div className="p-2.5 bg-green-500/10 rounded-xl border border-green-500/20">
                <Globe className="w-5 h-5 text-green-400" />
              </div>
              <h3 className="font-bold text-white text-lg tracking-tight">Intelligence Feed</h3>
              <span className="ml-auto text-xs font-bold text-green-400 bg-green-500/10 border border-green-500/20 px-3 py-1.5 rounded-full">
                {data.top_results.length} RESULTS
              </span>
            </div>

            <div className="space-y-4 px-1">
              {data.top_results.map((result, idx) => (
                <ResultCard key={result.link || idx} result={result} index={idx} />
              ))}
            </div>
          </div>
        ) : (
          <>
            <div className="flex items-center gap-4 mb-10">
              <div className="p-3.5 bg-green-500/10 rounded-2xl border border-green-500/20 group-hover:border-green-500/40 transition-colors shadow-lg shadow-green-900/10">
                <Database className="w-7 h-7 text-green-400" />
              </div>
              <div>
                <h3 className="font-bold text-white text-2xl tracking-tight">Intelligence Output</h3>
                <p className="text-neutral-500 text-sm mt-1">Live data aggregation stream</p>
              </div>
            </div>
            
            <div className="space-y-6 flex-1">
              {outputs.map((item, index) => (
                <div key={item.title} className="flex items-start gap-5 group/item p-4 rounded-2xl hover:bg-white/5 transition-colors border border-transparent hover:border-white/5">
                  <div className="mt-2 w-2.5 h-2.5 rounded-full bg-green-500 shrink-0 group-hover/item:scale-125 transition-transform shadow-[0_0_12px_rgba(34,197,94,0.6)]" />
                  <div>
                    <div className="text-xl font-medium text-neutral-200 group-hover/item:text-green-300 transition-colors">{item.title}</div>
                    <div className="text-base text-neutral-500 mt-1.5 leading-relaxed">{item.description}</div>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
