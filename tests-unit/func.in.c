before() {
	/// Before
	echo("Hello");
}

main() {
	/// Call before
	before();
	/// Call after
	after();
	/// Store output to a variable
	var added = add(4, 5);
	echo(added);
	/// Call "variables"
	// This generates a seemingly meaningless temporary.
	//  This makes sense if there are multiple calls
	//  in one expression
	var q = variables(1,2);
	// The temporary is now released for re-use
	/// Multiply nested call
	echo(add(1, 2), add(3+3, 4-add(5, 6)));
}

after() {
	/// After
	echo("Hello");
}

unused() {
	/// Unused
	echo("Delete me");
}

add(a, b) {
	/// Add a + b
	/// First, call before
	before();
	/// Return sum
	return a + b;
}

variables(a, b) {
	/// Variable test
	var x = a;
	var y = x + b;
	var z = x + y;
	x = z;
	a = 15;
	return z + add(a, b);
}
