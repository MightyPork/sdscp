#pragma safe_stack true
#pragma stack_start 100
#pragma stack_end 200

main () {
	func();
}

func() {
	func(); // infinite recursion
}
