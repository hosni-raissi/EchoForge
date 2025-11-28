"use client";

import React, { useState } from 'react';
import { Database, Clock, Layers, Hash } from 'lucide-react';
import { AnimatePresence } from 'framer-motion';

import Header from '@/components/Header';
import SearchForm from '@/components/SearchForm';
import InfoBlocks from '@/components/InfoBlocks';
import StatCard from '@/components/StatCard';
import ErrorAlert from '@/components/ErrorAlert';

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

export default function Dashboard() {
  const [target, setTarget] = useState('');
  const [type, setType] = useState('person');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<SearchResponse | null>(null);
  const [error, setError] = useState('');

  const [options, setOptions] = useState({
    deepSearch: true,
    darkWeb: true,
    socialMedia: true,
  });

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!target) return;

    setLoading(true);
    setError('');
    setData(null);

    try {
      const res = await fetch('http://localhost:8000/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          target, 
          target_type: type, 
          max_results: 20,
          deep_search: options.deepSearch,
          dark_web: options.darkWeb,
          social_media: options.socialMedia
        }),
      });

      if (!res.ok) throw new Error('Search failed');
      
      const result = await res.json();
      setData(result);
    } catch (err) {
      setError('Failed to fetch results. Ensure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const stats = {
    totalResults: data?.metadata.total_results || 0,
    executionTime: data ? `${data.metadata.execution_time}s` : '0s',
    dorksExecuted: data?.metadata.dorks_executed || 0,
    entitiesFound: data ? (
      data.aggregated_entities.emails.length + 
      data.aggregated_entities.phones.length + 
      Object.values(data.aggregated_entities.social_handles).flat().length
    ) : 0
  };

  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-200 font-sans selection:bg-blue-500/30 relative overflow-hidden">
      <div className="fixed inset-0 bg-[radial-gradient(ellipse_at_top,var(--tw-gradient-stops))] from-blue-900/20 via-neutral-950/80 to-neutral-950 pointer-events-none" />
      <div className="fixed inset-0 bg-[url('/grid.svg')] bg-center mask-[linear-gradient(180deg,white,rgba(255,255,255,0))] pointer-events-none opacity-20" />
      
      <main className="w-full relative z-10">
        <div className="max-w-[1600px] mx-auto p-8">
          <Header />
          
          <div className="flex flex-col lg:flex-row gap-8">
            {/* Left Column: Stats - Always visible */}
            <div className="w-full lg:w-72 shrink-0 space-y-4">
              <StatCard 
                icon={<Database className="text-neutral-400" />} 
                label="Total Results" 
                value={stats.totalResults}
                color="neutral" 
              />
              <StatCard 
                icon={<Clock className="text-blue-400" />} 
                label="Execution Time" 
                value={stats.executionTime}
                color="blue" 
              />
              <StatCard 
                icon={<Layers className="text-green-400" />} 
                label="Dorks Executed" 
                value={stats.dorksExecuted}
                color="green" 
              />
              <StatCard 
                icon={<Hash className="text-purple-400" />} 
                label="Entities Found" 
                value={stats.entitiesFound}
                color="purple" 
              />
            </div>

            {/* Right Column: Search & Results */}
            <div className="flex-1 min-w-0">
              <SearchForm
                target={target}
                type={type}
                loading={loading}
                options={options}
                onTargetChange={setTarget}
                onTypeChange={setType}
                onOptionsChange={setOptions}
                onSubmit={handleSearch}
              />

              <AnimatePresence>
                {error && <ErrorAlert message={error} />}
              </AnimatePresence>

              <InfoBlocks data={data} loading={loading} />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
