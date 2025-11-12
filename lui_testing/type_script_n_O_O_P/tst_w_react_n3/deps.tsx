
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
