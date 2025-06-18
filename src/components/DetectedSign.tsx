"use client";

import { useEffect, useState } from 'react';
import { Card } from './ui/card';
import { Badge } from './ui/badge';
import { motion, AnimatePresence } from 'framer-motion';

interface DetectedSignProps {
  sign: string | null;
  confidence?: number;
  className?: string;
}

export function DetectedSign({ sign, confidence, className = '' }: DetectedSignProps) {
  const [prevSign, setPrevSign] = useState<string | null>(null);

  useEffect(() => {
    if (sign !== prevSign) {
      setPrevSign(sign);
    }
  }, [sign, prevSign]);

  return (
    <Card className={`p-6 ${className}`}>
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-gray-700">
          Detected Sign
        </h3>
        
        <div className="h-32 flex items-center justify-center bg-gray-50 rounded-lg relative overflow-hidden">
          <AnimatePresence mode="wait">
            {sign ? (
              <motion.div
                key={sign}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
                className="text-center"
              >
                <span className="text-4xl font-bold text-gray-900">
                  {sign}
                </span>
                
                {confidence !== undefined && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.2 }}
                    className="mt-2"
                  >
                    <Badge variant="secondary" className="text-sm">
                      {`${(confidence * 100).toFixed(1)}% confident`}
                    </Badge>
                  </motion.div>
                )}
              </motion.div>
            ) : (
              <motion.div
                key="no-sign"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="text-gray-400 text-lg"
              >
                Waiting for gesture...
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {sign && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="text-sm text-gray-500 text-center"
          >
            {`Last updated: ${new Date().toLocaleTimeString()}`}
          </motion.div>
        )}
      </div>
    </Card>
  );
}
