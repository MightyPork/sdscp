main() {
    /// Three args with sub-call
	three_args(12, 5+79, ram[12+5]+sys[99+ram[12*sys[999+54]]]);
	
	/// Three args pure
	three_args_with_no_inner_calls(1, 2, 3);	

    /// recurs
	recurs(5);

    /// goto moo
	moo: goto moo;
}

three_args(a, b, c) {
	echo("a + b =", a + b, ", c = ", c);
	foo(); // Inner call forces a,b,c to be moved from arg variables to temporaries
}

foo() {}

three_args_with_no_inner_calls(a, b, c) {
	echo("a + b =", a + b, ", c = ", c);
}

recurs(a) {
    echo("Recurs ", a);
	if(a==0) goto end;

    /// Deeper
	recurs(a-1);

	end:
}
