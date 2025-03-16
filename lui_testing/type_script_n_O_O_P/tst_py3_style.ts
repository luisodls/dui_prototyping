// Define a simple class
class Greeter {

    who_2_greet: string;

    constructor(name_in: string) {
        this.who_2_greet = name_in;
    }

    greet() {
        return `Hi there, ${this.who_2_greet}!`;
    }
}


let greeter = new Greeter("Tester");
console.log(greeter.greet());
