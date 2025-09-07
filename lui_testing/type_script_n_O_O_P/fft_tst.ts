import * as numeric from 'numeric';

function f(x: number): number{
    return x
}
let pi = 3.14159265358;
let n = 5;
let step = 0.001;

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

function summation_an_p_bn(x_min: number, x_max: number, n: number): [number, number] {
  let sum_a = 0;
  let sum_b = 0;
  for (let x = x_min; x < x_max; x += step) {
    sum_a +=  f(x) * Math.cos(n * x) * step;
    sum_b +=  f(x) * Math.sin(n * x) * step;
  }
  sum_a = ( 1 / diff_L ) * sum_a;
  sum_b = ( 1 / diff_L ) * sum_b;
  return [sum_a, sum_b];
}

let an: number[] = [];
let bn: number[] = [];
for (let num: number = 1; num < n + 1; num++) {
  let [an_tst, bn_tst] = summation_an_p_bn(interval_from, interval_to, num);
  an.push(an_tst);
  bn.push(bn_tst);
}

console.log("an =", an)
console.log("bn =", bn)
function fourier_approx(x: number): number {
    let sum = a0;
    for (let num: number = 1; num < n + 1; num++) {
        sum += an[num - 1] * Math.cos((num * x * pi) / diff_L)
            +  bn[num - 1] * Math.sin((num * x * pi) / diff_L);
    }
    return sum;
}

for (let x = interval_from; x < interval_to; x += 0.1) {
    console.log(" f approx(", x, ")=", fourier_approx(x));
}
