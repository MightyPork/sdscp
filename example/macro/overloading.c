// This file shows how you can overload a macro
// For variable number of arguments, use Variadic Macros.


// USE ONLY IF REALLY NEEDED!
// It's non-standard and can lead to mistakes in your code.


// constant macro
#define FOO 15

// arraylike macro
#define FOO[i] (FOO * (i)) // using FOO macro - no problem with it

// function-like macro
#define FOO() echo("Hello Foo!")

// function-like macro with two arguments
#define FOO(a, b) echo("Look at my args: ", a, b)



var f = FOO;
var g = FOO[5];

FOO();
FOO(55, 66);

// this will cause warning in terminal
FOO("no", "variant", "takes", "five", "args");

