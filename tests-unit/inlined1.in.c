#pragma inline_one_use_functions true

main () {
	/// Not inlined 1
	echo(not_inlined_add(1,2));
	/// Not inlined 2
	echo(not_inlined_add(3,4));
	/// Inlined
	echo(inlined_add(5, 6));
	/// Inlined2
	echo(inlined_add2(5, 6));
	/// Inlined nested
	echo(2 * inlined_nested(7, 8) + 2);
	/// no return inline
	inlined_with_no_return();
}

inlined_with_no_return() {
	echo("cau");
}

inlined_add(a, b) {
	return a + b;
}

inlined_add2(a, b) {
	return a + b;
}

not_inlined_add(a, b) {
	return a + b;
}

inlined_nested(a, b) {
	return inlined_nested2(a, b) * 2;
}

inlined_nested2(a, b) {
	return a + b;
}
