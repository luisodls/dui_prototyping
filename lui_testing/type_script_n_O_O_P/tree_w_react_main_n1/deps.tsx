
import React from 'react';
import ReactDOM from 'react-dom/client';

import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { useRef, useEffect, useState } from "react";

'use client'

export function drawLine(
  x1: number, y1: number, x2: number, y2: number,
  ctx:CanvasRenderingContext2D, color: string = "black", width: number = 2
): void {
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.strokeStyle = color;
  ctx.lineWidth = width;
  ctx.stroke();
}

export interface StepMap {
  command: string;
  lin_num: number;
  success: string;
  indent: number;
  here: boolean;
  my_row: number;
  parent_row: number;
}

export function draw_tree(
  canvasRef: React.RefObject<HTMLCanvasElement>, tree_data_map: StepMap[]
): void {
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
      String(ste_pos.lin_num), x_scale * 1.5, y_text_corner
    );

    ctx.fillText(
      String(ste_pos.success), x_scale * 0.5, y_text_corner
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
