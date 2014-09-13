#pragma renderer sds2

main()
{
	omg:
	echo("yo");
	if(1) goto omg;

	fuu();
}

fuu() {
	omg:
	echo("aaa");
	if(1) goto omg;
}
