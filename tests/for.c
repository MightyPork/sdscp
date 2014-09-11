main()
{
	var i=0;
	for(; i<10; i++) {
		bar();
		if(1==2) break;
		if(4==5) continue;
		echo("yo");
	}
}

bar()
{
	echo("foo");
}
