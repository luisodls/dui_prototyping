
// Define a simple class
export class Greeter {
    // Property
    who_2_greet: string;

    // Constructor
    constructor(name_in: string) {
        this.who_2_greet = name_in;
    }

    // Method
    greet() {
        return `Hi there, ${this.who_2_greet}!`;
    }
}

// Create an instance of the class
let greeter = new Greeter("Luiso's world");

// Call the method and print the result
console.log(greeter.greet());
