// Define a simple class
class Greeter {

    who_2_greet: string;
    local_num: number;

    constructor(name_in: string) {
        this.who_2_greet = name_in;
        this.local_num = 5;
    }

    greet() {
        console.log("local_num =", this.local_num)
        return "Hi there, " + this.who_2_greet;
    }
}


let greeter = new Greeter("Tester");
console.log(greeter.greet());
