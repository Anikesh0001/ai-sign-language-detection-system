"use client";

import { useEffect, useRef, useState } from 'react';
import { Card } from './ui/card';

interface VideoFeedProps {
  onGestureDetected?: (gesture: string) => void;
}

export function VideoFeed({ onGestureDetected }: VideoFeedProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    // Initialize WebSocket connection
    const ws = new WebSocket('ws://localhost:8000/ws');
    wsRef.current = ws;

    ws.onopen = () => {
      setIsConnected(true);
      setError('');
      startVideoStream();
    };

    ws.onclose = () => {
      setIsConnected(false);
      setError('Connection to server lost');
    };

    ws.onerror = (error) => {
      setError('Failed to connect to server');
      console.error('WebSocket error:', error);
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.prediction !== null) {
        // Update processed frame
        if (data.processed_frame) {
          const img = new Image();
          img.onload = () => {
            const canvas = canvasRef.current;
            const ctx = canvas?.getContext('2d');
            if (canvas && ctx) {
              ctx.clearRect(0, 0, canvas.width, canvas.height);
              ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            }
          };
          img.src = `data:image/jpeg;base64,${data.processed_frame}`;
        }

        // Play audio if available
        if (data.audio) {
          const audio = new Audio(`data:audio/wav;base64,${data.audio}`);
          audio.play();
        }

        // Notify parent component of detected gesture
        if (data.sign_text && onGestureDetected) {
          onGestureDetected(data.sign_text);
        }
      }
    };

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
      stopVideoStream();
    };
  }, [onGestureDetected]);

  const startVideoStream = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: 640,
          height: 480,
          facingMode: 'user'
        }
      });

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
        startFrameCapture();
      }
    } catch (err) {
      setError('Failed to access webcam');
      console.error('Error accessing webcam:', err);
    }
  };

  const stopVideoStream = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream;
      stream.getTracks().forEach(track => track.stop());
    }
  };

  const startFrameCapture = () => {
    const captureFrame = () => {
      if (
        videoRef.current &&
        canvasRef.current &&
        wsRef.current &&
        wsRef.current.readyState === WebSocket.OPEN
      ) {
        const canvas = canvasRef.current;
        const video = videoRef.current;
        const ctx = canvas.getContext('2d');

        if (ctx) {
          // Draw the current video frame
          ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

          // Convert the frame to base64 and send to server
          const frame = canvas.toDataURL('image/jpeg', 0.8);
          wsRef.current.send(JSON.stringify({
            data: frame.split(',')[1]  // Remove data URL prefix
          }));
        }
      }

      // Schedule next frame capture
      requestAnimationFrame(captureFrame);
    };

    captureFrame();
  };

  return (
    <Card className="p-4">
      <div className="relative w-full aspect-video bg-black rounded-lg overflow-hidden">
        {error && (
          <div className="absolute inset-0 flex items-center justify-center bg-red-500/10">
            <p className="text-red-500 font-medium">{error}</p>
          </div>
        )}
        <video
          ref={videoRef}
          className="absolute inset-0 w-full h-full object-cover"
          playsInline
          muted
        />
        <canvas
          ref={canvasRef}
          width={640}
          height={480}
          className="absolute inset-0 w-full h-full object-cover"
        />
        {!isConnected && !error && (
          <div className="absolute inset-0 flex items-center justify-center bg-black/50">
            <p className="text-white">Connecting to server...</p>
          </div>
        )}
      </div>
    </Card>
  );
}
