'use client'
import Image from "next/image";
import { useRef, useEffect } from "react";
import { useState } from 'react';



export default function Home() {
  const canvasRef = useRef(null);
  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height); // Fill background white
  }, []);

  function handleLine (){
      const canvas = canvasRef.current;
      const ctx = canvas.getContext("2d");
      ctx.beginPath();
      ctx.moveTo(50, 50); // Start point (x, y)
      ctx.lineTo(200, 200); // End point (x, y)
      ctx.strokeStyle = "black"; // Line color
      ctx.lineWidth = 2; // Line thickness
      ctx.stroke();
      console.log("drawn line");
    };

  return (
    <div>
      <h1>Button w canvas</h1>
      <canvas
        ref={canvasRef}
        width={500}
        height={400}
        className="border border-gray-400"
      ></canvas>
      <button onClick={handleLine} className="p-2 bg-blue-300 rounded">Click here</button>
    </div>
  );
}
