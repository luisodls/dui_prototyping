'use client'
import Image from "next/image";

import React, { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { useState } from 'react';

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
      Do POST
    </button>
  );
}

function MyGetButton({msgHere}) {
  const [response, setResponse] = useState(null);
  const handleClick = async () => {
    try {
      const path_in = new URLSearchParams({ msgHere }).toString();
      const res = await fetch(`http://127.0.0.1:45678?${path_in}`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });

      const data = await res.json();
      setResponse(data);
      console.log("data =", data);
      alert(JSON.stringify(data));
    } catch (error) {
      console.error("Error <<", error, ">>");
      setResponse({ error: "Failed to connect to the server." });
      console.log("res ERROR");
    }
  }
  return (
    <button onClick={handleClick}>
      Do GET
    </button>
  );
}


export default function Home() {
  const [usrName, setName] = useState('');
  return (
    <div>
      <h2> Two http Buttons </h2>
      <label>
        Give name here:
        <input
          value={usrName}
          onChange={e => setName(e.target.value)}
        />
      </label>
      <MyPostButton msgHere ={usrName} />
      <MyGetButton msgHere ={usrName} />
    </div>
  );
}
