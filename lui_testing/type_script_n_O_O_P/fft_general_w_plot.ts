import * as numeric from 'numeric';
import { plot, Plot } from 'nodeplotlib';

function f(x: number): number{
    return x * x
}
let pi = 3.14159265358;
let n_max = 5;
let step = 0.001;

let interval_from = 0;
let interval_to = 5;
let diff_L = interval_to - interval_from;

function summation_a_0(x_min: number, x_max: number): number {
  let sum = 0;
  for (let x = x_min; x < x_max; x += step) {
    sum +=  f(x) * step;
  }
  sum = ( 1 / diff_L) * sum;
  return sum;
}
let a0 = summation_a_0(interval_from, interval_to);
console.log("a0", a0);

function summation_an_p_bn(
  x_min: number, x_max: number, n: number
): [number, number] {
  let sum_a = 0;
  let sum_b = 0;
  for (let x = x_min; x < x_max; x += step) {
    sum_a +=  f(x) * Math.cos(2 * pi * n * x / diff_L) * step;
    sum_b +=  f(x) * Math.sin(2 * pi * n * x / diff_L) * step;
  }
  sum_a = ( 2 / diff_L ) * sum_a;
  sum_b = ( 2 / diff_L ) * sum_b;
  return [sum_a, sum_b];
}

let an: number[] = [];
let bn: number[] = [];
for (let n: number = 1; n < n_max + 1; n++) {
  let [an_tst, bn_tst] = summation_an_p_bn(interval_from, interval_to, n);
  an.push(an_tst);
  bn.push(bn_tst);
}

console.log("an =", an)
console.log("bn =", bn)
function fourier_approx(x: number): number {
    let sum = a0;
    for (let n: number = 1; n < n_max + 1; n++) {
        sum += an[n - 1] * Math.cos(2 * pi * n * x / diff_L)
            +  bn[n - 1] * Math.sin(2 * pi * n * x / diff_L);
    }
    return sum;
}

let fun_org_x: number[] = [];
let fun_org_y: number[] = [];
let fun_app_y: number[] = [];

for (let x = interval_from; x < interval_to; x += 0.1) {
    console.log(" f approx(", x, ")=", fourier_approx(x));
    fun_org_x.push(x);
    fun_org_y.push(f(x));
    fun_app_y.push(fourier_approx(x));
}
const data1: Plot[] = [
  { x: fun_org_x, y: fun_org_y, type: 'scatter', },
];
const data2: Plot[] = [
  { x: fun_org_x, y: fun_app_y, type: 'scatter', },
];
plot(data1);
plot(data2);
