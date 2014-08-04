# SDS-C Plus

The goal of this project is to enable better coding practices and more powerful features in the SDS-C scripting language.

It takes a SDS-C Plus source code, and digests it into a format compatible with the official SDS-C compiler (that is, ugly code).

## Available Features

### Pre-processing

#### Include Guards

Note, that until all files are connected, the evaluation is linear.

That means that macro is not defined above it's `#define` directive, and it is defined all the way below it. Included files can see all already defined macros.

This can be used for the Include Guards:

```c
#ifndef UTILS_INCLUDED
#define UTILS_INCLUDED

// utils code

#endif
```

Such file can still be included multiple times, but will be evaluated only the first time.

This is the same as with real C header files.


#### Include directive

One of the main problems with SDS-C is that all has to be in single source file.

Such file tends to be very long and hard to work with. Includes to the rescue!

```c
#include "constants.c"
#include "folder/other_file.c"
```

It is possible to chain-include (`#include` in included file), but be careful not to create a cycle.

Note that `#include` (except for evaluating directives) means verbatim copy-paste.
If the included file does something stupid, it will have effect on the main file as well.


#### Define and # branching

Define lets you create flags for branching with `#ifdef` and `#ifndef`:

```c
#define DO_STUFF
// #define BE_LAZY

// later...

#ifdef DO_STUFF
	// stuff
#else
	// do something other
#endif


main()
{
	#ifndef BE_LAZY
	// work hard
	#endif
}
```

When you use `#define <name>`, it will be asigned value 1.


#### Constant macros

You can use `#define <name> <value>` to create constants.

*NOTE: SDSCP does **not** force you to use uppercase.*

```c
#define GARAGE_DOOR sys[231]

#define Dog "Kitten"

main()
{
	// some logic
	GARAGE_DOOR = 1;
	// ...
	print("Hot" Dog)
	// -> print("HotKitten") /* lol */

}
```

Using macros as constants is a great way to make your code more readable, without having to use variables.


#### Function-like macros

When you add parenthesis to the macro name, it becomes a function-like macro.

A function-like macro can contain some calculation, or a piece of code:

```c
#define TWICE(what) (2 * (what) )
```

Notice how the whole macro, and the argument's occurences are parenthesised.

Why?

```c
#define TWICE_BAD(what) 2*what
#define TWICE_GOOD(what) (2*(what))

var Bad  = TWICE_BAD(10+10)^3;
// -> var Bad  = 2*10+10^3;

var Good = TWICE_GOOD(10+10)^3;
// -> var Good = (2*(10+10))^3;
```

Function-like macros can span multiple lines:

```c
var LONG_MACRO()  do_simething();      \   // <-- backslash wraps a line
                  more_stuff();        \      /* comments here are ignored */
                  almost_done();       \
                  print("It's done!")      // <-- no semicolon
```

#### Array-like macros

They are pretty much the same like function-like macros, except they must take EXACTLY one parameter, and use square brackets:

```c
#define SQUARES[index]  ((index)*(index)) // Fake array of squares

var foo = SQUARES[100];
// -> var foo = ((100)*(100));
```

This can be used to alias the `sys[]` array:

```c
#define RELAY[n] sys[231+((n)-1)]

test()
{
	RELAY[6] = 1;   // -> sys[231+((6)-1)] = 1;
	echo(RELAY[5]); // -> echo(sys[231+((5)-1)]);
}
```

However, this will not work (yet), since SDS-C can't have expression as array index.
That will be taken care of in some future version of SDSCP.

For now, all you can do is this, but it's broken:

```c
var a; // temporary variable
#define RELAY[n] a = 231+((n)-1); \
                 sys[a]

test()
{
	// works fine
	RELAY[6] = 1;
	// -> a = 231+((6)-1); sys[a] = 1;

	// SYNTAX ERROR
	echo( RELAY[5] );
	// -> echo( a = 231+((5)-1); sys[a] );

	// TOTAL DISASTER
	foo = RELAY[6] + RELAY[2] ;
	// -> foo = a = 231+((6)-1); sys[a] + a = 231+((2)-1); sys[a] ;
}
```

#### Using macros in another macros

...obviously works, unlike in SDS-C.

Check this:

```c
// --- some huge library file ---
// ...
#define RELAY1 sys[231]

// --- application file ---
#define GARAGE RELAY1

// ...

GARAGE = 1; // open door
// -> sys[231] = 1;
```



 ## Planned Features

- Conversion to an Abstract Syntax Tree
- Extra control structures
  - `FOR`
  - `WHILE`
  - `UNTIL`
  - `SWITCH`
  - `IF_ELSEIF_ELSE`
- Stack in `ram[]`
- Return value, Arguments
- Local variables (keeping variable value after function call)
- New way of implementing functions using `goto`, labels and a redirection vector
