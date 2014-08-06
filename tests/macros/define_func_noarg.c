
#define moo() print("Moo")

// ok
moo();

// should NOT replace
moo
moo[]
// only on right
moo = 15+moo()*moo()
