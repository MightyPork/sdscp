
//
// This file shows some fun ways of using #include with this pre-processor
//

// #define FOO_1
// #define FOO_2
#define FOO_3

do_foo()
{
// various implementations of foo

#ifdef FOO_1
#include "foo_1.c"
#endif

#ifdef FOO_2
#include "foo_2.c"
#endif

#ifdef FOO_3
#include "foo_3.c"
#endif
}

