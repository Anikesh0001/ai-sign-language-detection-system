"use client";

import { useState } from 'react';
import { VideoFeed } from '@/components/VideoFeed';
import { DetectedSign } from '@/components/DetectedSign';
import { HistoryLog } from '@/components/HistoryLog';

interface HistoryEntry {
  id: string;
  sign: string;
  timestamp: Date;
}

export default function Home() {
  const [currentSign, setCurrentSign] = useState<string | null>(null);
  const [confidence, setConfidence] = useState<number | undefined>();
  const [history, setHistory] = useState<HistoryEntry[]>([]);

  const handleGestureDetected = (sign: string, detectedConfidence?: number) => {
    setCurrentSign(sign);
    setConfidence(detectedConfidence);
    
    // Add to history
    setHistory(prev => [
      ...prev,
      {
        id: Date.now().toString(),
        sign,
        timestamp: new Date()
      }
    ]);
  };

  return (
    <main className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto space-y-8">
          {/* Header */}
          <div className="text-center space-y-4">
            <h1 className="text-4xl font-bold text-gray-900">
              Sign Language Detection
            </h1>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Real-time sign language detection and translation using AI. 
              Make hand gestures in front of your camera to see them translated.
            </p>
          </div>

          {/* Main Content */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Video Feed */}
            <div className="lg:col-span-2">
              <VideoFeed onGestureDetected={handleGestureDetected} />
            </div>

            {/* Current Sign and History */}
            <div className="space-y-8">
              <DetectedSign
                sign={currentSign}
                confidence={confidence}
              />
              <HistoryLog entries={history} />
            </div>
          </div>

          {/* Instructions */}
          <div className="bg-white rounded-lg p-6 shadow-sm">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              How to Use
            </h2>
            <div className="grid gap-4 md:grid-cols-3">
              <div className="space-y-2">
                <div className="font-medium text-gray-900">1. Position</div>
                <p className="text-gray-600">
                  Position your hands clearly in front of the camera in good lighting.
                </p>
              </div>
              <div className="space-y-2">
                <div className="font-medium text-gray-900">2. Make Signs</div>
                <p className="text-gray-600">
                  Make clear hand gestures for American Sign Language letters and words.
                </p>
              </div>
              <div className="space-y-2">
                <div className="font-medium text-gray-900">3. View Results</div>
                <p className="text-gray-600">
                  See detected signs displayed in real-time with audio feedback.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
