#pragma inline_one_use_functions true

// Labels should be namespaced correctly

main () {
	retry:
	inlined();
	goto retry;
}

inlined() {
	if (sys[1]==0) goto retry;
	echo("cau");
	retry:
	
	inlined2();
	
	return 5;
	echo("aaa");
}

inlined2() {
	if (sys[1]==1) goto retry;
	echo("cau");
	retry:
	return 5;
	echo("aaa");
}
