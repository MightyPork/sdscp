// This example shows how to use variadic arguments macros

// simply aliasing echo() as print()
#define print(t...) echo(t)

print(one, two, three, 4, 5, 6, sys[123], "dfgdfgsd");




// easy aliasing long functions with providing some default values
#define my_http_get(path...) http_get(192, 165, 120, 11, "localhost", path)

my_http_get("index.php?a=", sys[140], "&b=", sys[445], "&c=", myVar);




// variadic argument can be in various positions...

// put ## before variadic argument in the macro code, and it will consume
// the preceding comma, if the argument is missing.
// Works only with comma.


#define variadic_start(foo..., b, c)      echo(" b=", b, " c=", c, "other=", ##foo)
#define variadic_end(b, c, foo...)        echo(" b=", b, " c=", c, "other=", ##foo)
#define variadic_middle(b, c, foo..., d)  echo(" b=", b, " c=", c, " d=", d, "other=", ##foo)

// testing varargs at start
variadic_start(v, vv, vvv, BBB, CCC);
variadic_start(v, BBB, CCC);
variadic_start(BBB, CCC);

// at end (THE BEST OPTION)
variadic_end(BBB, CCC, v, vv, vvv);
variadic_end(BBB, CCC, v, vv);
variadic_end(BBB, CCC);

// anywhere in between
variadic_middle(BBB, CCC, v, vv, vvv, DDD);
variadic_middle(BBB, CCC, v, DDD);
variadic_middle(BBB, CCC, DDD);

// Fair warning: Even if it *IS* possible to use other than "end"
// variadic macro, it is confusing and can cause errors.
