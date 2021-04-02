#pragma inline_one_use_functions true

main () {
	inlined();
	hell:
	echo("Fuck");
}

inlined() {
	goto hell;
}
