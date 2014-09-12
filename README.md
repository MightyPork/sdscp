# SDSCP - a SDS-C preprocessor

*SDSCP is free software, available under GPL v2*

**[Český návod ZDE](https://docs.google.com/document/d/1yKPp9HRQfGiGkIW1-4BfH-r1ENqbp_OQmSHbkxUufpk/edit?usp=sharing)**

This project's goal is to enable better syntax in [SDS-C](http://wiki.merenienergie.cz/index.php/Sdsc_sysf).

It's a python script that works as a processor, digesting your source to a form which the SDS-C compiler can understand.

## Features

For more detailed info, see the **[SDSCP wiki](https://github.com/MightyPork/sdscp/wiki)**.

### Already implemented

- `#include` directive
- Function-like macros
- Array-like macros
- Double quotes for strings
- Code branching with `#ifdef`, `#ifndef` etc...
- Automatic code formatting


### Planned

- Fixing SDS-C bugs (expression as array index, etc.)
- Extra control structures
  - `FOR`
  - `WHILE`
  - `UNTIL`
  - `SWITCH`
  - `IF_ELSEIF_ELSE`
- Stack in `ram[]` - Used for argument passing and return values
- Local variables (keeping variable value after a function call)
- Expression as array index
- Reimplemented functions (with arguments and return values)


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

SDSCP generates a SDS-C compatible source code, or warns you if there is some problem.
