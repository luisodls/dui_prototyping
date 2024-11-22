'use client'
import Image from "next/image";
import styles from "./page.module.css";

import React, { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { useState } from 'react';

function MyButton({msgHere}) {
  function handleClick() {
    console.log(msgHere);
    fetch('http://127.0.0.1:45678', { method: "POST", body: msgHere });
    alert(msgHere);
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
