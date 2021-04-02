#pragma inline_one_use_functions true

// Trampolines should be correct

main () {
	inlined();
	inlined2();
}

inlined() {
	/// inl1
	not_inlined();
}

inlined2() {
	/// inl2
	not_inlined();
}

not_inlined() {
	echo("Not inlined");
}
