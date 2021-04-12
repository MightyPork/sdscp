#pragma inline_one_use_functions true

main()
{
	echo("Cau");

	var a = 13;
	push(a);

	a = 27;

	pop(a);

	echo(a);

	end();
}
