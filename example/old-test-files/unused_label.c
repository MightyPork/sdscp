// should throw error
#pragma header 0

main() {
	if(1) {
		var x = 123;
		goto foo;
	}
	foo:
}
