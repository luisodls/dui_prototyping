'use client'
import Image from "next/image";

import React, { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { useState } from 'react';

var tree_log = ["-- Do a GET to see the tree --"];

function show_tree(pos_num, my_lst, indent = 1){
    let step = my_lst[pos_num]
    let stp_prn = "";
    if( step.success === true ){
        stp_prn = " T ";
    }else if( step.success === false ){
        stp_prn = " F ";
    }else{
        stp_prn = " N ";
    }
    let str_lin_num = String(step.lin_num);
    stp_prn = stp_prn + "  " + str_lin_num + "      ".repeat(indent) + " └──";
    try{
        stp_prn = stp_prn + String(step.command)
    } catch (error) {
        stp_prn = stp_prn + "None"
    }
    tree_log.push(stp_prn);
    console.log(stp_prn)
    try{
        for (let new_pos of step.nxt) {
            show_tree(new_pos, my_lst, indent + 1);
        }
    } catch (error) {
        console.log("last indent =", indent);
    }
}

function MyGetButton({ msgHere }) {
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
      const my_lst = data.Answer;
      console.log("Received Data:", my_lst);
      tree_log = [" St lin# ", "__________________________"];
      show_tree(0, my_lst, 1);
      alert(JSON.stringify(tree_log, null, 2));
    } catch (error) {
      console.error("Fetch failed:", error.message);
      setResponse({ error: "Failed to connect to the server." });
    }
  };
  return (
    <div>
      <button onClick={handleClick}>
        Do GET
      </button>
      {tree_log && (
        <pre style={{ background: "#f4f4f4", padding: "10px", borderRadius: "5px" }}>
          {JSON.stringify(tree_log, null, 2)}
        </pre>
      )}
    </div>
  );
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
