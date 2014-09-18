main(){
	echo(sum(100));
}

sum(n)
{
	if(n == 1) return 1;
	var k;
	var l;
	var m;
	return n + sum(n-1);
}
