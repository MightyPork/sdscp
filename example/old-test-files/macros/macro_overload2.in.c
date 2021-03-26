
#define add +
#define add[foo] ((foo)*16)
#define add(a) (a)
#define add(a, b) ((a) + (b))
#define add(a, b, c) ((a) + (b) + (c))
#define add(a, b, c, d) ((a) + (b) + (c) + (d))

var a;
main{
	a = add(1);
	a = add(1, 2);
	a = add(1, 2, 3);
	a = add(1, 2, 3, 4);
	a = 15 add 6;
	a = add[4445565];
}
