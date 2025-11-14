const rootElement = document.getElementById('root');

import React from 'react';
import ReactDOM from 'react-dom/client';

import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { useRef, useEffect, useState } from "react";

import { StepMap, draw_tree } from "./deps";

'use client'

interface Step {
  success: boolean | null;
  lin_num: number;
  command: string;
  here: boolean;
  nxt: number[];
}

let tree_data_str: string[] = ["-- Do a GET to see the tree --"];
let tree_data_map: StepMap[] = [];

function build_tree_recr(pos_num: number, my_lst: Step[], indent: number = 1, parent_row: number = 0): void {
  const step = my_lst[pos_num];
  let stp_suss: string;
  if (step.success === true) {
    stp_suss = " T ";
  } else if (step.success === false) {
    stp_suss = " F ";
  } else {
    stp_suss = " N ";
  }
  const str_lin_num = String(step.lin_num);
  let stp_prn = stp_suss + "  " + str_lin_num + "     ".repeat(indent) + " >__";
  const stp_cmd = String(step.command);
  stp_prn = stp_prn + " [ " + stp_cmd+ " ] ";
  const step_map: StepMap = {
    command: stp_cmd,
    lin_num: step.lin_num,
    success: stp_suss,
    indent: indent,
    here: step.here,
    my_row: tree_data_map.length,
    parent_row: parent_row
  };
  tree_data_str.push(stp_prn);
  tree_data_map.push(step_map);
  try {
    for (let new_pos of step.nxt) {
      build_tree_recr(new_pos, my_lst, indent + 1, step_map.my_row);
    }
  } catch (error) {
    console.log("last indent =", indent);
  }
}

interface MyGetButtonProps {
  msgHere: string;
  tmpRef: React.RefObject<HTMLCanvasElement>;
}

function MyGetButton({ msgHere, tmpRef }: MyGetButtonProps) {
  const [response, setResponse] = useState<any>(null);

  const handleClick = async () => {
    try {
      const path_in = new URLSearchParams({ msgHere }).toString();
      const res = await fetch(`http://127.0.0.1:45678?${path_in}`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });
      const data = await res.json();
      setResponse(data);
      const my_lst: Step[] = data.Answer;
      console.log("Received Data:", my_lst);
      tree_data_str = [" St lin# ", "__________________________"];
      tree_data_map = [];
      build_tree_recr(0, my_lst, 1, 0);
      draw_tree(tmpRef, tree_data_map);
    } catch (error: any) {
      console.error("Fetch failed:", error.message);
      setResponse({ error: "Failed to connect to the server." });
    }
  };

  return (
    <div>
      <button onClick={handleClick}>
        Do GET
      </button>
      {tree_data_str && (
        <pre style={
            {
              background: "#f4f4f4", padding: "10px", borderRadius: "5px",
              font: "12px Mono", textAlign: "left"
            }
          }>
          {JSON.stringify(tree_data_str, null, 2)}
        </pre>
      )}
    </div>
  );
}

interface MyPostButtonProps {
  msgHere: string;
}

function MyPostButton({ msgHere }: MyPostButtonProps) {
  const [response, setResponse] = useState<any>(null);

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
    } catch (error: any) {
      console.error("❌ Error:", error.message || error);
      setResponse({ error: error.message || "Failed to connect to the server." });
    }
  };

  return (
    <button onClick={handleClick}>
      Do POST
    </button>
  );
}

//////////////////////////////////////////////////////////////////////////////
export default function App() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [MyCmd, setName] = useState<string>('');

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  }, []);

  return (
    <div>
      <h2>Dui2 Style tree</h2>
      <canvas
        ref={canvasRef}
        width={900}
        height={500}
        className="border border-gray-400"
      ></canvas>
      <label>
        Dui cmd:
        <input
          value={MyCmd}
          onChange={e => setName(e.target.value)}
        />
      </label>
      <MyPostButton msgHere={MyCmd} />
      <MyGetButton msgHere={MyCmd} tmpRef={canvasRef} />
    </div>
  );
}



if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);

  root.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
} else {
  console.error("Failed to find the root element.");
}

