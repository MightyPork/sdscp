#define FOO(a, b) echo("Look at my args: ", a, b)

main () {
    // this will cause warning in terminal
    FOO("no", "variant", "takes", "five", "args");
}
