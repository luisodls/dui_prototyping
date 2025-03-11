class MyGreetingClass {
    who_2_greet: string;
    dummy_str: string = "";
    constructor(name_in: string) {
        this.who_2_greet = name_in;
    }
    greet() {
        return `Hi there, ${this.who_2_greet}!`;
    }

    set_dummy(cad_in: string) {
        this.dummy_str = cad_in;
    }
}

let greeter = new MyGreetingClass("Luiso's world");
console.log(greeter.greet());
greeter.set_dummy("AAAA");
console.log("set_dummy ... done");
console.log("[MyGreetingClass.dummy_str] =", greeter.dummy_str);
