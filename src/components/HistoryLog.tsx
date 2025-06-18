"use client";

import { useEffect, useRef } from 'react';
import { Card } from './ui/card';
import { ScrollArea } from './ui/scroll-area';
import { motion, AnimatePresence } from 'framer-motion';

interface HistoryEntry {
  id: string;
  sign: string;
  timestamp: Date;
}

interface HistoryLogProps {
  entries: HistoryEntry[];
  className?: string;
}

export function HistoryLog({ entries, className = '' }: HistoryLogProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new entries are added
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [entries]);

  return (
    <Card className={`p-4 ${className}`}>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-700">History Log</h3>
          <span className="text-sm text-gray-500">
            {entries.length} {entries.length === 1 ? 'entry' : 'entries'}
          </span>
        </div>

        <ScrollArea className="h-[400px] pr-4" ref={scrollRef}>
          <AnimatePresence initial={false}>
            {entries.length > 0 ? (
              <div className="space-y-2">
                {entries.map((entry) => (
                  <motion.div
                    key={entry.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, x: -100 }}
                    transition={{ duration: 0.2 }}
                    className="flex items-start justify-between p-3 bg-gray-50 rounded-lg"
                  >
                    <div className="flex-1">
                      <p className="font-medium text-gray-900">{entry.sign}</p>
                      <p className="text-sm text-gray-500">
                        {entry.timestamp.toLocaleTimeString()}
                      </p>
                    </div>
                  </motion.div>
                ))}
              </div>
            ) : (
              <div className="flex items-center justify-center h-full">
                <p className="text-gray-400">No signs detected yet</p>
              </div>
            )}
          </AnimatePresence>
        </ScrollArea>
      </div>
    </Card>
  );
}
