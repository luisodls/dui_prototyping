'use client'
import Image from "next/image";
import { useRef, useEffect } from "react";
import { useState } from 'react';

function handleLine(canvasRef) {
  const canvas = canvasRef.current;
  if (!canvas) return; // Ensure canvas exists
  const ctx = canvas.getContext("2d");
  ctx.beginPath();
  ctx.moveTo(50, 50); // Start point (x, y)
  ctx.lineTo(200, 200); // End point (x, y)
  ctx.strokeStyle = "black"; // Line color
  ctx.lineWidth = 2; // Line thickness
  ctx.stroke();
  console.log("Line #1")
}

function MyPostButton({msgHere}) {
  const [response, setResponse] = useState(null);
  const handleClick = async () => {
    try {
      const res = await fetch("http://127.0.0.1:45678", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msgHere }),
      });
      const data = await res.json();
      setResponse(data);
      console.log("✅ Response received:", data);
    } catch (error) {
      console.error("❌ Error:", error.message || error);
      setResponse({ error: error.message || "Failed to connect to the server." });
    }
  }
  return (
    <button onClick={handleClick}>
      Do POST
    </button>
  );
}

export default function Home() {
  const canvasRef = useRef(null);
  const [MyCmd, setName] = useState('');
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  }, []);

  return (
    <div>
      <h1>Button w canvas</h1>
      <canvas
        ref={canvasRef}
        width={300}
        height={200}
        className="border border-gray-400"
      ></canvas>

      <label>
        Give name here:
        <input
          value={MyCmd}
          onChange={e => setName(e.target.value)}
        />
      </label>


      <button onClick={
        () => handleLine(canvasRef)
      } className="p-2 bg-blue-300 rounded">
        Click here
      </button>
      <MyPostButton msgHere ={MyCmd} />
    </div>
  );
}
