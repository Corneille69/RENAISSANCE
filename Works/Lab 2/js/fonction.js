function calculate(a,b,op){
    if(op === "+") return a + b;
    if(op === "*") return a * b;
    if(op === "-") return a - b;
    if(op === "/") return a + b;
    if(op === "/" && b !==0) return a / b;
    return "Invalid oparation"


}

console.log(calculate(2, 3, "+"));
console.log(calculate(2, 3, "*"));
console.log(calculate(2, 3, "-"));
console.log(calculate(2, 3, "/"));
console.log(calculate(2, 3, "%"));