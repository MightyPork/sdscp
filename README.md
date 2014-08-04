# SDS-C Plus

The goal of this project is to enable better coding practices and more powerful features in the SDS-C scripting language.

It takes a SDS-C Plus source code, and digests it into a format compatible with the official SDS-C compiler (that is, ugly code).

**Example of SDSCP in action**

```c
// project/library.c

#ifndef LIBRARY_C_INCLUDED // <-- Include guards
#define LIBRARY_C_INCLUDED

#define RELAY1 sys[231]
#define RELAY2 sys[232]

#define ON	1
#define OFF	0

#define isOn(what) ((what) != OFF)             // parenthesis for safety
#define setTo(what, value) what = (value)

library_function()
{
	echo("Hello.");
}

#endif
```

```c
// project/main.c

// including the library file
#include "library.c"

// We can use macros from library now

#define heating		RELAY1
#define ventilator 	RELAY2

#define on(x)	setTo(x, 1)
#define off(x)	setTo(x, 0)

change_mode()
{
	if (isOn(heating)) {
		off(heating);
		on(ventilator);
	} else {
		off(ventilator);
		on(heating);
	}
}
```

**Process by SDSCP**

    $ sdscp -c project/main.c out/project.c


**Ready for SDS!**

```c
// out/project.c

change_mode
{
	if (((sys[231]) != 0)) {
		sys[231] = (0);
		sys[232] = (1);
	} else {
		sys[232] = (0);
		sys[231] = (1);
	}
}
```


## What is SDS-C anyway?

SDS-C is a scripting language for SDS devices - see the [website](http://wiki.merenienergie.cz/index.php/Sdsc_sysf).

It has to be compiled using a very bad proprietary compiler.

### Why is SDS-C so bad?

- No variable scope, all is global
- `GOTO`s everywhere
- Stack is limited to 6
- No function arguments.
- No return values.
- No control structures except `IF-ELSE`. Why? "You can just use GOTO"
- Everything is signed *Int 32*.
- Except string literals. But you can't store them or do anything with them.
- String literals use single quotes. And don't support escapes - no way to print `'`
- There is almost no support for `++` and `--`
- The authors apparently never heard of ternary operator (`<cond> ? <then> : <else>`)
- Can't create array variables.
- Can't use expression as array index, only variable or number.
- Tab in `#define` is syntax error
- Can't assign value in variable declaration
- Can have only 48 routines.
- Can have only 128 variables.
- No support for multi-line or functional macros
- Can't use macros in other macros
- Can't use branching (`#ifdef` etc)
- The compiler is super buggy and gives useless error messages.

It's not that SDS could not handle better language - the compiler is just **REALLY STUPID**.


## Goals of SDSCP

This project's goal is to enable better C-like syntax without all the stupid limitations of SDS-C.

It's a python script that works as a macro processor, and later will be added a proper tokenizer, making it possible to add new control structures and other features missing from SDS-C script.


### Already implemented

- `#include` directive
- Function-like macros
- Array-like macros
- Double quotes for strings
- Code branching with `#ifdef`, `#ifndef` etc...
- Basic tokenizer (experimental, activate using the -x argument)


### Planned Features

- Extra control structures
  - `FOR`
  - `WHILE`
  - `UNTIL`
  - `SWITCH`
  - `IF_ELSEIF_ELSE`
- Stack in `ram[]` - Used for argument passing and return values
- Local variables (keeping variable value after a function call)
- Expression as array index
- Reimplemented functions (GOTO's, redirection vector, storing index on stack etc.) - to remove SDS-C's limitations such as stack size and function count limit.



## How to use SDSCP

To run SDSCP, you need Python 3 installed.

It is designed for use on Linux, some small adjustments may be needed to use it on other systems. (Not tested)

```none

# get help
sdscp -h

# convert a file (prints it to terminal)
sdscp source.c

# store the output to a file (ready to be pasted in SDS-C)
sdscp source.c -o outfile.c

# clean the produced code (remove comments and extra newlines)
sdscp source.c -c

# verbose mode (show extra info - eg. list of all macros)
sdscp source.c -v

# expermiental mode (show work-in-progress features)
sdscp source.c -x

```

SDSCP generates a SDS-C compatible source code, or warns you if there is some problem.

Since the tokenizer is not yet finished, it will not catch all errors (eg. missing braces).
But stay assured that SDS-C will loudly complain.


## Available Features

### Pre-processing

#### Include Guards

Note, that until all files are connected, the evaluation is linear.

That means that macro is not defined above it's `#define` directive, and it is defined all the way below it. Included files can see all already defined macros.

However, once the files are connected, the definition order no longer matters.

If you re-define a macro, the later definition will have effect (that is, until macro overloading is implemented)


The linear nature of the concatenation phase can be used to make so Include Guards:

```c
#ifndef UTILS_INCLUDED
#define UTILS_INCLUDED

// utils code

#endif
```

Such file can still be included multiple times, but will be evaluated only the first time.

The point is that you don't have to worry about including a file multiple times by accident - the later includes won't have any effect on the output.


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

func()
{
#ifdef DO_STUFF
	stuff();
#else
	something_else();
#endif
}


main()
{
	#ifndef BE_LAZY
	work_hard(); // only if BE_LAZY is not defined
	#endif
}
```

When you use `#define <name>`, it will be asigned value 1.


#### Constant macros

You can use `#define <name> <value>` to create constants.

**NOTE:** SDSCP does NOT force you to use uppercase.

```c
#define GARAGE_DOOR sys[231]

#define Dog "Kitten"

main()
{
	// some logic
	GARAGE_DOOR = 1;
	// -> sys[231] = 1;
	// ...
	print("Hot" Dog);
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
var Bad, Good;

#define BAD(what) 2*what
#define GOOD(what) (2*(what))

Bad  = BAD(10+10)^3;
// -> Bad  = 2*10+10^3; // messed up meaning

Good = GOOD(10+10)^3;
// -> Good = (2*(10+10))^3; // uglier but works properly
```

Function-like macros can span multiple lines:

```c
#define LONG_MACRO()  do_simething();      \   // <-- backslash wraps a line
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
