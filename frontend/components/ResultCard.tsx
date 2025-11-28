import { ExternalLink } from 'lucide-react';
import { motion } from 'framer-motion';

interface ResultCardProps {
  result: {
    title: string;
    link: string;
    snippet: string;
    displayLink: string;
    relevance_score?: number;
  };
  index: number;
}

export default function ResultCard({ result, index }: ResultCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.05 }}
      className="bg-gradient-to-br from-neutral-900/60 to-neutral-900/40 border border-neutral-800 rounded-xl p-5 hover:border-blue-500/40 transition-all duration-300 group hover:shadow-lg hover:shadow-blue-500/5"
    >
      <div className="flex justify-between items-start mb-2">
        <a 
          href={result.link} 
          target="_blank" 
          rel="noopener noreferrer" 
          className="text-lg font-medium text-blue-400 hover:text-blue-300 transition-colors flex items-center gap-2 flex-1"
        >
          <span className="line-clamp-2">{result.title}</span>
          <ExternalLink className="w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0" />
        </a>
        {result.relevance_score && (
          <span className="text-xs font-mono bg-blue-500/10 text-blue-400 px-2.5 py-1 rounded-md border border-blue-500/20 ml-3 flex-shrink-0">
            {result.relevance_score.toFixed(1)}
          </span>
        )}
      </div>
      <div className="text-xs text-neutral-500 mb-3 font-mono">{result.displayLink}</div>
      <p className="text-neutral-300 text-sm leading-relaxed line-clamp-3">{result.snippet}</p>
    </motion.div>
  );
}
