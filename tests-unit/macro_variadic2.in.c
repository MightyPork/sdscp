
#define moo_printf(var...) echo(var)
#define first_va(a..., b) echo(a, "|", b)

#define last_va(a, b...) echo(a, "|", b)

#define reverse_printf(values..., format) echo(format, ## values)

main () {
    var hello=1, how=10, are=100, you=1000;
	moo_printf(hello, how, are, you);
	moo_printf();

	first_va("a", "b", "c", "d", "e");

	last_va("a", "b", "c", "d", "e");

	reverse_printf("a", "b", "%s %s %s %s");
	reverse_printf("NO_VALUES");
}
