#pragma remove_dead_code false

// this test checks that dead code removal can be disabled

main () {
	goto end;
	echo("not accessible!");
	bugger:
	stupid_nonsense:
	blabla:
	if(0) {
		echo("Never");
	}
	end:
}


unused() {
	echo("Never used!!");
}
