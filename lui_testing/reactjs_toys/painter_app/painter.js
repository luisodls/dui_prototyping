'use client'
import Image from "next/image";

import React, { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { useRef, useEffect, useState } from "react";

export default function Canvas() {
  const canvasRef = useRef(null);
  const [drawing, setDrawing] = useState(false);
  const [mode, setMode] = useState("line");

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height); // Fill background white
  }, []);

  // Start drawing
  const handleMouseDown = (e) => {
    if (mode !== "line") return;
    setDrawing(true);
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.beginPath();
    ctx.moveTo(e.nativeEvent.offsetX, e.nativeEvent.offsetY);
  };

  // Draw when moving the mouse
  const handleMouseMove = (e) => {
    if (!drawing || mode !== "line") return;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.lineTo(e.nativeEvent.offsetX, e.nativeEvent.offsetY);
    ctx.stroke();
  };

  // Stop drawing
  const handleMouseUp = () => {
    setDrawing(false);
  };

  // Clear canvas
  const clearCanvas = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
  };

  return (
    <div className="flex flex-col items-center space-y-4 p-4">
      <canvas
        ref={canvasRef}
        width={900}
        height={700}
        className="border border-gray-400"
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
      ></canvas>
      <div className="space-x-2">
        <button onClick={() => setMode("line")} className="p-2 bg-gray-300 rounded">Draw Line</button>
        <button onClick={clearCanvas} className="p-2 bg-red-300 rounded">Clear</button>
      </div>
    </div>
  );
}
