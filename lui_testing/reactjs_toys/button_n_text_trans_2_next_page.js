'use client'
import Image from "next/image";
import styles from "./page.module.css";

import React, { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { useState } from 'react';

function MyButton({nameHere}) {
  function handleClick() {
    alert(nameHere);
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
      <MyButton nameHere ={usrName} />
    </div>
  );
}
