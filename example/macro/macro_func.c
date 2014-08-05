
// This file tests macro processing

#define ADD(a, b) ((a) + (b))

#define Q(_if, _true, _false)	( 								\
									(_if)*(_true) 				\
									+ (1 - (_if)) * (_false)	\
								)

main()
{
	var a = ADD(12, 13);
	var b = Q(a > 13, ADD(ADD(Inner1, Inner2), Outer), 456+15);
}
