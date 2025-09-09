let lst = [0, 1, 1];
console.log("lst =", lst);
const size = 15;
for (let n: number = 1; n < size + 1; n++) {
    lst.push(lst[n] + lst[n + 1])
}
console.log("lst =", lst)
