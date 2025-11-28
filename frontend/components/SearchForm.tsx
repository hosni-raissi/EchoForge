import { Search, ChevronRight, Activity, Globe, ShieldAlert, Zap } from 'lucide-react';

export interface SearchOptions {
  deepSearch: boolean;
  darkWeb: boolean;
  socialMedia: boolean;
}

interface SearchFormProps {
  target: string;
  type: string;
  loading: boolean;
  options: SearchOptions;
  onTargetChange: (value: string) => void;
  onTypeChange: (value: string) => void;
  onOptionsChange: (options: SearchOptions) => void;
  onSubmit: (e: React.FormEvent) => void;
}

export default function SearchForm({ 
  target, 
  type, 
  loading, 
  options,
  onTargetChange, 
  onTypeChange, 
  onOptionsChange,
  onSubmit 
}: SearchFormProps) {
  const toggleOption = (key: keyof SearchOptions) => {
    onOptionsChange({ ...options, [key]: !options[key] });
  };

  return (
    <div className="bg-neutral-900/40 border border-neutral-800 rounded-2xl p-5 mb-6 backdrop-blur-md shadow-2xl relative overflow-hidden group">
      <div className="absolute inset-0 bg-linear-to-br from-blue-500/5 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />
      
      <form onSubmit={onSubmit} className="flex flex-col gap-4 relative z-10">
        <div className="flex flex-col md:flex-row gap-4 items-end">
          <div className="flex-1 w-full">
            <label htmlFor="target-input" className="block text-xs font-semibold text-neutral-400 mb-1.5 uppercase tracking-widest pl-1">
              Target Identifier
            </label>
            <div className="relative group/input">
              <div className="absolute inset-0 bg-blue-500/20 rounded-xl blur-md opacity-0 group-focus-within/input:opacity-100 transition-opacity duration-300" />
              <Search className="absolute left-4 top-3 w-5 h-5 text-neutral-500 group-focus-within/input:text-blue-400 transition-colors" />
              <input
                id="target-input"
                type="text"
                value={target}
                onChange={(e) => onTargetChange(e.target.value)}
                placeholder="e.g. John Doe, username, email..."
                className="w-full bg-neutral-950/80 border border-neutral-800 rounded-xl py-2.5 pl-12 pr-4 text-white placeholder:text-neutral-600 focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20 transition-all relative"
              />
            </div>
          </div>
          
          <div className="w-full md:w-64">
            <label htmlFor="type-select" className="block text-xs font-semibold text-neutral-400 mb-1.5 uppercase tracking-widest pl-1">
              Target Type
            </label>
            <div className="relative group/select">
              <div className="absolute inset-0 bg-blue-500/20 rounded-xl blur-md opacity-0 group-focus-within/select:opacity-100 transition-opacity duration-300" />
              <select
                id="type-select"
                value={type}
                onChange={(e) => onTypeChange(e.target.value)}
                className="w-full bg-neutral-950/80 border border-neutral-800 rounded-xl py-2.5 px-5 text-white appearance-none focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20 transition-all cursor-pointer relative"
              >
                <option value="person">Person</option>
                <option value="email">Email</option>
                <option value="phone">Phone</option>
              </select>
              <ChevronRight className="absolute right-5 top-3 w-5 h-5 text-neutral-500 rotate-90 pointer-events-none group-focus-within/select:text-blue-400 transition-colors" />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full md:w-auto bg-linear-to-r from-blue-600 to-blue-700 hover:from-blue-500 hover:to-blue-600 text-white px-10 py-2.5 rounded-xl font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2.5 shadow-lg shadow-blue-900/20 hover:shadow-blue-500/30 hover:-translate-y-0.5 active:translate-y-0"
          >
            {loading ? <Activity className="animate-spin w-5 h-5" /> : <Search className="w-5 h-5" />}
            {loading ? 'Scanning...' : 'Initialize Scan'}
          </button>
        </div>

        <div className="flex flex-wrap gap-4 pt-4 border-t border-neutral-800/50">
          <button
            type="button"
            onClick={() => toggleOption('deepSearch')}
            className={`flex items-center gap-3 px-4 py-2 rounded-xl border transition-all duration-300 ${
              options.deepSearch 
                ? 'bg-blue-500/10 border-blue-500/40 text-blue-400 shadow-[0_0_15px_rgba(59,130,246,0.15)]' 
                : 'bg-neutral-950/50 border-neutral-800 text-neutral-500 hover:border-neutral-700 hover:text-neutral-400'
            }`}
          >
            <Zap className={`w-4 h-4 ${options.deepSearch ? 'fill-blue-500/20' : ''}`} />
            <span className="text-sm font-medium">Deep Search</span>
            <div className={`w-2 h-2 rounded-full ${options.deepSearch ? 'bg-blue-500 shadow-[0_0_8px_rgba(59,130,246,0.8)]' : 'bg-neutral-700'}`} />
          </button>

          <button
            type="button"
            onClick={() => toggleOption('darkWeb')}
            className={`flex items-center gap-3 px-4 py-2 rounded-xl border transition-all duration-300 ${
              options.darkWeb 
                ? 'bg-purple-500/10 border-purple-500/40 text-purple-400 shadow-[0_0_15px_rgba(168,85,247,0.15)]' 
                : 'bg-neutral-950/50 border-neutral-800 text-neutral-500 hover:border-neutral-700 hover:text-neutral-400'
            }`}
          >
            <ShieldAlert className={`w-4 h-4 ${options.darkWeb ? 'fill-purple-500/20' : ''}`} />
            <span className="text-sm font-medium">Dark Web Scan</span>
            <div className={`w-2 h-2 rounded-full ${options.darkWeb ? 'bg-purple-500 shadow-[0_0_8px_rgba(168,85,247,0.8)]' : 'bg-neutral-700'}`} />
          </button>

          <button
            type="button"
            onClick={() => toggleOption('socialMedia')}
            className={`flex items-center gap-3 px-4 py-2 rounded-xl border transition-all duration-300 ${
              options.socialMedia 
                ? 'bg-green-500/10 border-green-500/40 text-green-400 shadow-[0_0_15px_rgba(34,197,94,0.15)]' 
                : 'bg-neutral-950/50 border-neutral-800 text-neutral-500 hover:border-neutral-700 hover:text-neutral-400'
            }`}
          >
            <Globe className={`w-4 h-4 ${options.socialMedia ? 'fill-green-500/20' : ''}`} />
            <span className="text-sm font-medium">Social Media</span>
            <div className={`w-2 h-2 rounded-full ${options.socialMedia ? 'bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.8)]' : 'bg-neutral-700'}`} />
          </button>
        </div>
      </form>
    </div>
  );
}
