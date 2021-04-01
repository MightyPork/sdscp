main() {
    var res = add6(1, 2, add2(3, 4), 5, add2(6, add2(7, 8)), 9);
	if (res != 45) {
		echo("BAD SUM!");
	} else {
		echo ("OK: ", res);
	}
}

add6(a, b, c, d, e, f) {
	return a + b + c + d + e + f;
}

add2(a, b) {
	return a + b;
}
