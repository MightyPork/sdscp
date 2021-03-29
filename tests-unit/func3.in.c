return_zero() {
	return_42();
	echo("cau");
}

return_42() {
	return 42;
}

main() {
	var zero = return_zero();
	if (zero != 0) echo("WHAT??!!");
}
