
#define moo_printf(var...) printf(var)
#define first_va(a..., b) [a | b]

#define last_va(a, b...) [a | b]

#define reverse_printf(values..., format) printf(format, ## values)

main() {
	moo_printf(hello, how, are, you);
	moo_printf();

	first_va("a", "b", "c", "d", "e");

	last_va("a", "b", "c", "d", "e");

	reverse_printf("a", "b", "%s %s %s %s");
	reverse_printf("NO_VALUES");
}
