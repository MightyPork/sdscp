# SDSCP - a SDS-C preprocessor

*SDSCP is free software, available under GPL v2*

**[Český návod ZDE](https://docs.google.com/document/d/1yKPp9HRQfGiGkIW1-4BfH-r1ENqbp_OQmSHbkxUufpk/edit?usp=sharing)**

This project's goal is to enable better syntax in [SDS-C](http://wiki.merenienergie.cz/index.php/Sdsc_sysf).

It's a python script that works as a processor, digesting your source to a form which the SDS-C compiler can understand.

## Features

Look in the unit tests folder to see what transformations SDSCP can do.

Highlights:

### Macros and directives

- `#include` directive
- Function-like and array-like macros
- Code branching with `#ifdef`, `#ifndef`, `#if`, `defined()` ...

### String fixes

- Double quotes for strings, single quotes for ASCII characters
- Adjacent strings without comma are now correctly joined

### Control structures

- `for(var i = 0; i < 100; i++)`, even with multiple variables and complex expressions
- `while(cond)`
- `do {} while(cond)`
- `switch` - just like in C, including `default:`, `break;` and fall-through
- `break`, `continue` in all loops
- `if - else if - else`, with unlimited chaining
- Free-standing blocks `{}`

### Functions

- Reimplemented functions (with arguments and return values). 
- Unlimited number of functions
- Stack in `ram[]` - Used for argument passing and return values
- Single-use function inlining
- Dead code removal
- Any function can be called from anywhere, declaration order does not matter like in classic C or SDS-C
- `goto` is only allowed within a function, 
- labels are local to function

### Variables

- Global, function and block scope
- All variables can have default value (`var x = 15;`)
- Automatic management and re-use of temporary variables, this works around the variable limit in SDS-C

### SDS-C bug workarounds

- Incorrect arithmetic operator precedence: SDSCP automatically adds parentheses to expressions
- Fix unary minus not working correctly in SDS-C
- `if()` can now have any statement as body, not only goto or block
- All built-in functions now accept arbitary expressions as arguments: e.g. `echo()`, `sprintf()`
- Arrays can use any expression as index: `sys[]`, `text[]`, `ram[]`, `share[]`. SDS-C only allows a variable or number as index.

## How to use SDSCP

To run SDSCP, you need Python 3 installed.

It is designed for use on Linux, some small adjustments may be needed to use it on other systems. (Not tested)

There is a bunch of python files in the project, the `sdscp` one being the main executable. Add this to your PATH and you're good.

Then, use `sdscp -h` for the most up-to-date info on command line arguments.

The most basic use is like so:

```bash
# show output code on screen
sdscp input.c -d

# store output code to a file
sdscp input.c -o output.c
```

SDSCP generates a SDS-C compatible source code, or warns you if there is a problem.

