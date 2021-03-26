// test functions

var a = 12;
var b = 13;
var c;

init() {
	echo("Init");
	if(a == b) echo("Yep");
}

main() {
	echo("Main, yo!");

    func_with_args(4,5,6);

}

func_with_args(moo, yo, dawg) {
    echo("func_with_args");
	echo(moo, " is ", yo, " under ", dawg);
    other_func(77777);
}

other_func(booo) {
	echo("other_func", booo);
}


noargs() {
	do_stuff();
}


do_stuff() {
    echo("Stuff");
}
