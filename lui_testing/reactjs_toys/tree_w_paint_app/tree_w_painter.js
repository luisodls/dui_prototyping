'use client'
import Image from "next/image";
import { useRef, useEffect } from "react";
import { useState } from 'react';

var tree_log = ["-- Do a GET to see the tree --"];

function build_tree_recr(pos_num, my_lst, indent = 1){
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
  console.log(stp_prn);
  try{
      for (let new_pos of step.nxt) {
          build_tree_recr(new_pos, my_lst, indent + 1);
      }
  } catch (error) {
      console.log("last indent =", indent);
  }
}

function draw_tree(canvasRef) {
  alert(JSON.stringify(tree_log, null, 2));
  const canvas = canvasRef.current;
  if (!canvas) return; // Ensure canvas exists
  const ctx = canvas.getContext("2d");
  ctx.beginPath();
  ctx.moveTo(10, 10); // Start point (x, y)
  ctx.lineTo(50, 50); // End point (x, y)
  ctx.strokeStyle = "black"; // Line color
  ctx.lineWidth = 2; // Line thickness
  ctx.stroke();
  console.log("time to request GET")
}

function MyGetButton({ msgHere, tmpRef}) {
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
      build_tree_recr(0, my_lst, 1);
      draw_tree(tmpRef);
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
        width={200}
        height={100}
        className="border border-gray-400"
      ></canvas>
      <label>
        Dui cmd:
        <input
          value={MyCmd}
          onChange={e => setName(e.target.value)}
        />
      </label>
      <MyPostButton msgHere ={MyCmd} />
      <MyGetButton msgHere ={MyCmd} tmpRef ={canvasRef} />
    </div>
  );
}
