#pragma renderer sds2

main()
{
    /// Normal func
    fuu();

    /// Main loop
	omg:
	echo("yo");
	if(1) goto omg;
}

fuu() {
	omg:
	echo("aaa");
    // !!! Not using a constant here, it would cause
    // the return label to be optimized out!
	if(sys[15]) goto omg;
}
