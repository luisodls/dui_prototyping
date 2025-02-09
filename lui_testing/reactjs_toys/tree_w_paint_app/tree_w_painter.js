'use client'
import Image from "next/image";
import { useRef, useEffect } from "react";
import { useState } from 'react';

var tree_data_str = ["-- Do a GET to see the tree --"];
var tree_data_map = ["---------------"];

function build_tree_recr(pos_num, my_lst, indent = 1, parent_row = 0){
  const step = my_lst[pos_num]
  let stp_suss = "";
  if( step.success === true ){
      stp_suss = " T ";
  }else if( step.success === false ){
      stp_suss = " F ";
  }else{
      stp_suss = " N ";
  }
  const str_lin_num = String(step.lin_num);
  let stp_prn = stp_suss + "  " + str_lin_num + "     ".repeat(indent) + " └──";
  const stp_cmd = String(step.command);
  stp_prn = stp_prn + stp_cmd;
  const step_map = {
    command: stp_cmd, lin_num: step.lin_num, success: stp_suss,
    indent:indent, my_row:tree_data_map.length, parent_row:parent_row
  };
  tree_data_str.push(stp_prn);
  tree_data_map.push(step_map);
  try{
      for (let new_pos of step.nxt) {
          build_tree_recr(new_pos, my_lst, indent + 1, step_map.my_row);
      }
  } catch (error) {
      console.log("last indent =", indent);
  }
}

function drawLine(x1, y1, x2, y2, ctx, color = "black", width = 2) {
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.strokeStyle = color;
  ctx.lineWidth = width;
  ctx.stroke();
}

function draw_tree(canvasRef) {
  //alert(JSON.stringify(tree_data_str, null, 2));
  //alert(JSON.stringify(tree_data_map));
  console.log("tree_data_map =", tree_data_map);

  const canvas = canvasRef.current;
  if (!canvas) return; // Ensure canvas exists
  const ctx = canvas.getContext("2d");

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const x_scale = 25;
  const y_scale = 20;

  for (let i = 0; i < tree_data_map.length; i++) {
    ctx.fillStyle = i % 2 === 0 ? "white" : "lightgray";
    ctx.fillRect(0, i * y_scale, 500, y_scale);

    ctx.fillStyle = "black";
    ctx.font = "12px Mono";
    ctx.fillText(` ${tree_data_map[i].lin_num}`, 10, (i + 1) * y_scale - 6);

    ctx.fillText(
      tree_data_map[i].command,
      (tree_data_map[i].indent * 2.5 + 0.5) * x_scale + x_scale * 0.75,
      (i + 1) * y_scale - 6
    );
  }

  for (let ste_pos of tree_data_map) {
    let x_ini_vezier = ste_pos.indent * 2.5 * x_scale;
    let y_ini_vezier = ste_pos.my_row * y_scale;
    let x_end_vezier = (ste_pos.indent * 2.5 + 0.5) * x_scale;
    let y_end_vezier = (ste_pos.my_row + 0.5) * y_scale;
    drawLine(
      x_ini_vezier, (ste_pos.parent_row + 1) * y_scale,
      x_ini_vezier, y_ini_vezier,    ctx, "blue", 2
    );
    ctx.moveTo(x_ini_vezier, y_ini_vezier);  // Move to the start point
    ctx.quadraticCurveTo(
      x_ini_vezier, y_end_vezier, x_end_vezier, y_end_vezier
    );
    ctx.strokeStyle = "blue";
    ctx.lineWidth = 2;
    ctx.stroke();

    drawLine(
      x_end_vezier, y_end_vezier,
      x_end_vezier + x_scale * 0.5, y_end_vezier,    ctx, "blue", 2
    );
  }
  console.log("drawing done")
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
      tree_data_str = [" St lin# ", "__________________________"];
      tree_data_map = [];
      build_tree_recr(0, my_lst, 1, 0);
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
      {tree_data_str && (
        <pre style={{ background: "#f4f4f4", padding: "10px", borderRadius: "5px" }}>
          {JSON.stringify(tree_data_str, null, 2)}
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
        width={500}
        height={400}
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
