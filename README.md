# SDSCP - a SDS-C preprocessor

**This is a free software, using GPL v2**

## What is SDS-C?

SDS-C is a (pretty bad) scripting language for SDS devices - see their [website](http://wiki.merenienergie.cz/index.php/Sdsc_sysf).

### What is wrong with SDS-C?

I won't go as far as saying "everything", but it'd be pretty close.


**= Common things missing =**

- No control structures except `If-Else` and procedures. Why? *"You can just use GOTO"*
- No function arguments (*"To keep it simple and reliable"*)
- No return values
- No function-like macros
- Can't create arrays.
- No support for ternary operator (`<cond> ? <then> : <else>`)
- Can't use branching (`#ifdef` etc)


**= Bugs & bad design =**

- `GOTO`s everywhere
- Can't use macros in other macros
- Can't use `++` and `--` in expression
- Strings use single quotes. And don't support escapes - no way to print `'`
- Tab in `#define` is syntax error
- The compiler usually gives meaningless error messages.


**= Dumb limitations =**

- Can't use expression as array index, only variable or number.
- No variable scope, all is global
- Stack is limited to 6
- Can have only 48 routines.
- Can have only 128 variables.
- Everything is signed *int32*. (Except strings, but you can't put them in a variable)


SDSs are actually quite powerful devices - the compiler is just **REALLY STUPID**.


## Goals of SDSCP

This project's goal is to enable better C-like syntax without all the stupid limitations of SDS-C.

It's a python script that works as a macro processor, and later will be added a proper tokenizer, making it possible to add new control structures and other features missing from SDS-C script.


### Already implemented

- `#include` directive
- Function-like macros
- Array-like macros
- Double quotes for strings
- Code branching with `#ifdef`, `#ifndef` etc...
- Tokenizer


### Planned Features

- Fixing SDS-C bugs (expression as array index, etc.)
- Token -> AST conversion
- AST -> source coversion (allowing AST manipulations to alter output code)
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

say_hello()
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

	say_hello();
}
```

**Process by SDSCP**

(`-c` flag to remove comments and extra whitespace)

    $ sdscp -c project/main.c out/project.c


**Ready for SDS!**

```c
// out/project.c

say_hello
{
	echo('Hello.');
}

change_mode
{
	if (((sys[231]) != 0)) {
		sys[231] = (0);
		sys[232] = (1);
	} else {
		sys[232] = (0);
		sys[231] = (1);
	}

	say_hello();
}
```


## How to use SDSCP

To run SDSCP, you need Python 3 installed.

It is designed for use on Linux, some small adjustments may be needed to use it on other systems. (Not tested)

**Help page**

Use `sdscp -h` for the most up-to-date info.

At the time of writing this, you would get:

```none
$ sdscp -h
usage: sdscp [-h] [-o OUTPUT] [-c] [-v] [-t] [-m] [-p] [-r] [-s] [-d] source

SDS-C macro preprocessor

positional arguments:
  source                The source file to process

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        The output file; If not specified, output will be
                        printed to console.
  -c, --clean           Remove some whitespace and all comments
  -v, --verbose         Show all optional debug info.
  -t, --show-tokens     Show tokenization.
  -m, --show-macros     List all macros
  -p, --show-processed  Show code after replacing macros (preprocessor output)
  -r, --show-resolved   Show code after processing includes and # branching.
  -s, --show-source     Show original source (only main file)
  -d, --show-output     Show the final source
```

**Some examples:**

```bash

# process a file, show the output
sdscp -d input.c

# store the output to a file
sdscp input.c -o output.c

# clean the produced code
sdscp input.c -c -o output.c

# verbose mode (show tons of debug info)
sdscp input.c -v

```

Setups for unit testing:

```bash
# for the macro tests
sdscp input.c -smpc

# for tokenizer tests
sdscp input.c -ptc

# to test the "pretty" to "SDS-C" filter
sdscp input.c -pdc
``


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

Such file tends to be very long and hard to work with. **Includes to the rescue!**

```c
#include "constants.c"
#include "folder/other_file.c"
```

It is possible to chain-include (`#include` in included file), but be careful not to create a cycle.

Note that `#include` (except for evaluating directives) means verbatim copy-paste.
If the included file does something stupid, it will have effect on the main file as well.


#### Define and # branching

Define lets you create flags for branching with `#ifdef` and `#ifndef`.

When you use `#define <name>`, it will be asigned value 1.
If you set the value to 0 with `#define <name> 0`, it will be treated as undefined.

That means you can set value to 0 to disable a flag, instead of commenting it out.

```c

#define DO_STUFF
#define BE_LAZY 0 // Don't be lazy

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
	work_hard(); // only if not lazy
	#endif
}
```


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
                      print("It's done!")      // <-- no semicolon, to allow syntax like LONG_MACRO();
```

#### Array-like macros

They are pretty much the same like function-like macros, except they must take EXACTLY one parameter, and use square brackets:

```c
#define SQUARES[index]  ((index)*(index)) // Fake array of squares

var foo = SQUARES[100];
// -> var foo = ((100)*(100));
```

Array-like macros can work as access to some other array, or a virtual table of values.
Placing statements in an array-like macro is generally a bad idea

Typical array-like macro usage - alias to a part of the `sys[]` array:

```c
#define RELAY[n] sys[231+((n)-1)]

test()
{
	RELAY[6] = 1;   // -> sys[231+((6)-1)] = 1;
	echo(RELAY[5]); // -> echo(sys[231+((5)-1)]);
}
```

However, this **will not work (yet)**, since SDS-C can't handle expression as array index.
That will be taken care of in some future version of SDSCP.

For now, all you can do is this, but it's broken:

```c
var a; // temporary variable
#define RELAY[n] a = 231+((n)-1); \  // <-- see the statement? That's not good.
                 sys[a]

test()
{
	// Works fine
	RELAY[6] = 1;
	// ->
	//    a = 231+((6)-1);    // Assign address to a temporary variable
	//    sys[a] = 1;         // assign the value


	// Does not work
	echo( RELAY[5] );
	// ->
	//    echo(
	//      a = 231+((5)-1);  // statement inside echo
	//      sys[a]
	//    );

	// Neither does this
	foo = RELAY[6] + RELAY[2];
	// ->
	//    foo = a = 231+((6)-1);    // I doubt SDS-C can handle this
	//    sys[a] + a = 231+((2)-1); // This doesn't even make any sense
	//    sys[a];                   // Neither does this
}
```

Conclusion? Be careful with macros - in general.

#### Using macros in other macros

...obviously works, unlike in SDS-C.

This is shown in the example at the very top.
