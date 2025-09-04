
function add(a: number, b: number): number {
  return a + b;
}
console.log("2 + 2 = ", add(2, 2))

function add_with_func_in(b: number): number {
  return add(3, 3) + b;
}
console.log("(1 + 1) + (1 + 1) = ", add(add(1, 1), add(1, 1)))
console.log("add_with_func_in(3) = ", add_with_func_in(3))

