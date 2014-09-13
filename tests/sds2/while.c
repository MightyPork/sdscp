#pragma renderer sds2

var k = 100;

main()
{
	while(k > 10) {
		k--;
		echo(k);
	}

	do {
		echo(123);
	} while(1);

	while(1 == 1) {
		do {
			echo("yo");
		} while(2 == 2);
	}
}
