
'use client'
import './App.css'
//import Image from "next/image";
import { useRef, useEffect, useState } from "react";

interface Step {
  success: boolean | null;
  lin_num: number;
  command: string;
  here: boolean;
  nxt: number[];
}

interface StepMap {
  command: string;
  lin_num: number;
  success: string;
  indent: number;
  here: boolean;
  my_row: number;
  parent_row: number;
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
  let stp_prn = stp_suss + "  " + str_lin_num + "     ".repeat(indent) + " └──";
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

function drawLine(x1: number, y1: number, x2: number, y2: number, ctx: CanvasRenderingContext2D, color: string = "black", width: number = 2): void {
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.strokeStyle = color;
  ctx.lineWidth = width;
  ctx.stroke();
}

function draw_tree(canvasRef: React.RefObject<HTMLCanvasElement>): void {
  const canvas = canvasRef.current;
  if (!canvas) return; // Ensure canvas exists
  const ctx = canvas.getContext("2d");
  if (!ctx) return; // Ensure context exists

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const x_scale = 25;
  const y_scale = 30;

  ctx.fillStyle = "lightgray";
  for (let i = 0; i < tree_data_map.length; i=i + 2) {
    ctx.fillRect(0, i * y_scale, 900, y_scale);
  }

  for (let ste_pos of tree_data_map) {
    let x_text_corner = (ste_pos.indent * 2.5 + 0.3) * x_scale;
    let y_text_corner = (ste_pos["my_row"] + 0.7) * y_scale;

    ctx.fillStyle = "black";
    ctx.font = "16px Mono";
    ctx.fillText(
      ste_pos.command, x_text_corner, y_text_corner
    );

    ctx.fillText(
      ste_pos.lin_num, x_scale * 0.5, y_text_corner
    );
  }

  for (let ste_pos of tree_data_map) {
    let x_ini_vezier = (ste_pos.indent * 2.5 - 1.5) * x_scale;
    let x_end_vezier = (ste_pos.indent * 2.5) * x_scale;
    let y_ini_vezier = ste_pos.my_row * y_scale;
    let y_end_vezier = (ste_pos.my_row + 0.5) * y_scale;
    if (ste_pos.lin_num > 0) {
      drawLine(
        x_ini_vezier, (ste_pos.parent_row + 1) * y_scale,
        x_ini_vezier, y_ini_vezier, ctx, "blue", 2
      );
      ctx.beginPath();
      ctx.moveTo(x_ini_vezier, y_ini_vezier);
      ctx.quadraticCurveTo(
        x_ini_vezier, y_end_vezier, x_end_vezier, y_end_vezier
      );
      ctx.strokeStyle = "blue";
      ctx.lineWidth = 2;
      ctx.stroke();
    }

    ctx.strokeRect(
      x_end_vezier, y_end_vezier - y_scale * 0.4,
      110, y_scale * 0.8
    );
  }
  console.log("drawing done");
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
      draw_tree(tmpRef);
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

