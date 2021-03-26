// trying to break the variable renamer
var __fuck = -10;
var __sp = 10;
var u__sp = 20;
var u__xx = 111;
var u__xx1 = 112;
var __xx = 222;
var _skfk = 30;
var k = 40;

main()
{
	__sp = 75;
	echo("yolo", __sp);

	__sp = 555;
	u__sp = 99;

	moo(__sp, __fuck);

	echo("u__sp", u__sp);
	echo("__sp", __sp);
}

moo(__sp, __fuck)
{

}
