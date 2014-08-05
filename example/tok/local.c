
var g = 15; // global

do_stuff()
{
	var loc = 444;
	g = 7;
}

task()
{
	var loc = 57;

	g = 13;
	do_stuff();
	echo("g ", loc);

	echo("loc ", loc);
}
