'use client'
import Image from "next/image";

import React, { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { useState } from 'react';

function MyButton({msgHere}) {
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
      console.log("data =", data);
      alert(JSON.stringify(data));
    } catch (error) {
      console.error("Error:", error);
      setResponse({ error: "Failed to connect to the server." });
      console.log("res ERROR");
    }
  }
  return (
    <button onClick={handleClick}>
      Click me
    </button>
  );
}


export default function Home() {
  const [usrName, setName] = useState('');
  return (
    <div>
      <h1> Button and text connected </h1>
      <label>
        Give name here:
        <input
          value={usrName}
          onChange={e => setName(e.target.value)}
        />
      </label>
      <MyButton msgHere ={usrName} />
    </div>
  );
}
