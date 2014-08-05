var i;

main()
{
lbl1:
	i = 356;
	
	goto loop;
	
loop:
	print("Yo dawg");
	wait(1000);
	goto loop;	
}

otherfunc()
{
	// invalid jump
	goto lbl1;
}
