// this test explores how the dead code cleaner works

main()
{
    /// Noreturn
    fuu2();

    /// Normal func

    // This will be removed
    fuu();
    echo("Hello!!!!!! what");

    /// Main loop
	omg: // jump target, so this is kept
	echo("yo");
	if(1) goto omg;
}

fuu() {
    // The dead code remover removes this whole section
   echo("aaa");
   echo("aaa");
   echo("aaa");
}

fuu2() {
    omg:
    echo("aaa");
    goto omg; // the dead code remover detects this
    // and the return goto's and labels will be removed
}
