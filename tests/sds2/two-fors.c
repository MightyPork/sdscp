#pragma check_stack_bounds false

main()
{
	for(var i=0; i<100; i++) {
		echo(i*2);
	}

	for(var i=0; i<100; i++) {
		echo(i*3);
	}
}
