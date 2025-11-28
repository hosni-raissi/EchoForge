import { AlertCircle } from 'lucide-react';
import { motion } from 'framer-motion';

interface ErrorAlertProps {
  message: string;
}

export default function ErrorAlert({ message }: ErrorAlertProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      className="bg-red-500/10 border border-red-500/30 text-red-400 p-4 rounded-xl mb-8 flex items-center gap-3 backdrop-blur-sm"
    >
      <AlertCircle className="w-5 h-5 flex-shrink-0" />
      <span>{message}</span>
    </motion.div>
  );
}
