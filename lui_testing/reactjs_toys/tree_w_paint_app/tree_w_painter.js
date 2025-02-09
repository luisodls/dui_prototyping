'use client'
import Image from "next/image";
import { useRef, useEffect } from "react";
import { useState } from 'react';

var tree_data_str = ["-- Do a GET to see the tree --"];
var tree_data_map = ["---------------"];

function build_tree_recr(pos_num, my_lst, indent = 1){
  let step = my_lst[pos_num]
  let stp_suss = "";
  if( step.success === true ){
      stp_suss = " T ";
  }else if( step.success === false ){
      stp_suss = " F ";
  }else{
      stp_suss = " N ";
  }
  let str_lin_num = String(step.lin_num);
  let stp_prn = stp_suss + "  " + str_lin_num + "      ".repeat(indent) + " └──";
  let stp_cmd = String(step.command);
  stp_prn = stp_prn + stp_cmd;
  let stp_dict = {
    command: stp_cmd, lin_num: step.lin_num,
    success: stp_suss, indent:indent
  };

  tree_data_str.push(stp_prn);
  tree_data_map.push(stp_dict);
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
  //alert(JSON.stringify(tree_data_str, null, 2));
  alert(JSON.stringify(tree_data_map));
  console.log("tree_data_map =", tree_data_map);
  /*for (let new_step of tree_data_map) {
    console.log("step.command =", new_step.get("command"));
  };*/

  console.log("len(tree_data_str) = ", tree_data_str.length)

  const canvas = canvasRef.current;
  if (!canvas) return; // Ensure canvas exists
  const ctx = canvas.getContext("2d");

  let x2 = tree_data_str.length * 5
  let y2 = tree_data_str.length * 5

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.beginPath();
  ctx.moveTo(10, 10);
  ctx.lineTo(x2, 100);
  ctx.strokeStyle = "black";
  ctx.lineWidth = 2;
  ctx.stroke();
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
      tree_data_map = ["---------------"];
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
        width={300}
        height={200}
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
