import * as numeric from 'numeric';

function f(x: number): number{
    return x
}
let pi = 3.14159265358;
let n = 5;
let step = 0.1;

let interval_from = -pi;
let interval_to = pi;
let diff_L = (interval_to - interval_from) / 2;

function summation_a_0(x_min: number, x_max: number): number {
  let sum = 0;
  for (let x = x_min; x < x_max; x += step) {
    sum +=  f(x) * step;
  }
  sum = ( 1 / (2 * diff_L) ) * sum;
  return sum;
}
let a0 = summation_a_0(interval_from, interval_to);
console.log("a0", a0);

function summation_a_n(x_min: number, x_max: number, n: number): number {
  let sum = 0;
  for (let x = x_min; x < x_max; x += step) {
    sum +=  f(x) * Math.cos(n * x) * step;
  }
  sum = ( 1 / diff_L ) * sum;
  return sum;
}
function summation_b_n(x_min: number, x_max: number, n: number): number {
  let sum = 0;
  for (let x = x_min; x < x_max; x += step) {
    sum +=  f(x) * Math.sin(n * x) * step;
  }
  sum = ( 1 / diff_L ) * sum;
  return sum;
}
let an: number[] = []
let bn: number[] = []
for (let num: number = 1; num < n + 1; num++) {
  let an_val = summation_a_n(interval_from, interval_to, num);
  console.log("a[", num, "] = ", an_val);
  an.push(an_val);

  let bn_val = summation_b_n(interval_from, interval_to, num);
  console.log("b[", num, "] = ", bn_val);
  bn.push(bn_val);
}
console.log("an =", an)
console.log("bn =", bn)

function fourier_approx(x: number): number {
    let sum = a0;
    for (let num: number = 1; num < n + 1; num++) {
        sum +=  an[n - 1] * Math.cos((num * x * pi) / diff_L)
              + bn[n - 1] * Math.sin((num * x * pi) / diff_L);
        //console.log("sum=", sum)
    }
    return sum;
}


for (let x = interval_from; x < interval_to; x += step) {
    console.log(" f approx(", x, ")=", fourier_approx(x));
}
