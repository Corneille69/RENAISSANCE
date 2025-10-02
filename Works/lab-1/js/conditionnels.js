console.log("If else condition");
let score=prompt("Enter your score");

let scoreInNumber= parseInt(score, 10);
console.log(typeof scoreInNumber);

if(scoreInNumber>=50){
    console.log("pass");
} else {
    console.log("Fail");
}

console.log("switch statement");
let day=prompt("Enter the day:");

switch (day){
     case"Monday":
    console.log("Back to work");
    break

      case"Friday":
    console.log("Almost weekend");
    break

    default:
        console.log("Just another day");
        break
}