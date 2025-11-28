import { Shield } from 'lucide-react';

export default function Header() {
  return (
    <header className="mb-12 flex items-center gap-5">
      <div className="relative group">
        <div className="absolute inset-0 bg-blue-500 blur-xl opacity-20 group-hover:opacity-40 transition-opacity duration-500" />
        <div className="relative p-3.5 bg-linear-to-br from-blue-600 to-blue-700 rounded-2xl shadow-2xl shadow-blue-900/20 border border-blue-500/20">
          <Shield className="w-8 h-8 text-white" />
        </div>
      </div>
      <div>
        <h1 className="text-5xl font-bold text-white mb-1.5 tracking-tight">
          EchoForge <span className="text-transparent bg-clip-text bg-linear-to-r from-blue-400 to-blue-600">Intelligence</span>
        </h1>
        <p className="text-neutral-400 text-lg font-light tracking-wide">Advanced OSINT Deep Search & Analysis Platform</p>
      </div>
    </header>
  );
}
