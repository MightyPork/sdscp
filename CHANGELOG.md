# Changelog

## 1.8.7

- Allow empty strings when they are later joined to another string
- Move empty string warning to SDS-C renderer
- Add transforms to allow `-2147483648` and unsigned int up to `0xFFFFFFFF`, automatically turning it into hex with a warning printed.
- Add parentheses around all negative numbers to work around a SDS-C bug with unary minus (the minus is seemingly discarded)

## 1.8.6

- Add workaround for SDS-C bug with `1 - -1` being interpreted as `1-- 1` and 
  causing error "illegal -- operator"
- Extend simplification to more expression types 
  (now including expressions that contain the `~` and `/` operators)

```c
var j;
main
{
  j = 0x512 & (~ 0xFF); // 1280
  j = 0x512 & -256; // 256 ??? what
  j = 0x512 & (-256); // 1280

  echo(j);
}
```

- Add workaround for SDS-C bug with bitwise operators vs. negative numbers
- Strip outermost parentheses from expressions in assignments. 
  SDS-C adds 10 bytes of bytecode for every parenthesis pair!

## 1.8.5

- Bugfix for switch with `text[]` or similar arguments

## 1.8.4

- New optimizations to reduce code size:
  - Functions that call no other functions (excluding inlined and built-in)
    now use the __aX argument variables directly instead of first moving them
    to temporaries. This saves 5 operations per argument (push, assign, pop)
    and inlining is much more efficient for small functions.
  - Inlined functions store the result directly into the output variable, removing 
    the need to move it from __rval to the output variable at the end. This saves 
    one operation per inlined function.
  - Switch now uses the input directly if it's a variable, instead of moving it to
    a temporary. This will be the most common case. This saves 1 to 5 operations
    per function using the switch.

## 1.8.3

- Add single-use function inlining, enabled by default, plus added new unit tests
  - Inlining reduces code size by avoiding the function call emulation
  - The inlined function works exactly as if it wasn't inlined, e.g. parameters and `return` work
    normally, goto is restricted to the inlined function, local variables are scoped correctly.
- Add warning about unused functions
- Add warning about functions that should be inlined but are not (e.g. because it's disabled)
- New pragmas `inline_one_use_functions` and `remove_dead_code`, both default true

```c
// Inline functions used only once.
// Inlining speeds up execution and reduces code size. 
#pragma inline_one_use_functions true

// Remove dead code, e.g. unused functions, code after a goto,
// or unused labels.
#pragma remove_dead_code true
```

## 1.8.2

- Fix nested function calls lead to mangled arguments
- Temporaries / globals sort now uses natural ordering

## 1.8.1

- Fix that variables could not be declared in switch cases. 
  These variables are scoped to the particular `case` or `default` block and do not survive 
  pass-through.

## 1.8.0

- Correctly implement `#if`, it now supports most compile-time evaluable expressions
- `#ifdef` now works exactly as you'd expect from normal C. This is a **breaking change**!
  - Previously, `#ifdef` would treat `#define FOO 0` as undefined. This is now defined.
- Add compile-time eval for boolean expressions
- `defined(XXX)` can now be used in `#if`, effectively making:
	- `#if defined(XXX)` the equivalent of `#ifdef XXX`
	- `#if !defined(XXX)` the equivalent of `#ifndef XXX`

## 1.7.4

- Fix a bug with implicit return.

The return register was not updated on implicit return, 
so code like this would behave unexpectedly:

```c
five() { 
  return 5;
}

zero() { 
  five();
  echo("Hi");
}

main() {
  echo(zero()); // Prints 5
}
```

All functions that do not return explicitly correctly return zero after this fix. It's confirmed 
by unit tests, which have been updated and some functionally tested.

A side effect is that some generated code is now slightly shorter, as it's easier for the dead 
code removal algorithm to detect the unnecessary register clearing when explicit return is used.

## 1.7.3

- Show error on macro or include recursion

## 1.7.2

- Allow underscore as a group separator in number literals (e.g. 123_456, 0xFFFF_FFFF, 0b1111_1111).
  The underscore is removed after parsing.
- Show error on numeric or string literals that are not supported by SDS-C

## 1.7.1

- Support `#if 1`
- Added unit test for `#if 0` and `#if 1`

## 1.7.0

- Added unit tests with a testing framework (yes it's a bash script)
- Variables now have block scope. 
  - Applies to if/while/do-while/for
  - Each switch case has it's own block.
  - For is special and the scope includes the initializers.
- Optimized some generated code
- Fixed crashes in less often used patterns
- Add checks for duplicate argument names
- Fix bad multi-line macro parsing
- Add `#if 0` (note: ONLY this exact pattern! One space after if)
- Switch case values can now contain variables or function calls
- Improve auto-generated variable naming to avoid collisions
- Fix some errors needlessly showing trace

## 1.6.3

- Fix comments in macro definition tokenized as code, resulting in apostrophes and double quotes
  in comments wrongly treated as char and string boundaries
- Fix tmp variables clobbered while expanding expressions with function calls not push/popped, leading to UB. 
- Fix temporaries not released after push() and pop() calls (magic built-in methods).

## 1.6.2

- Fix crash if an in-line comment is at the end of an expression parenthesis that is wrapped to multiple lines

## 1.6.1

- Error if a function is called with a wrong number of arguments.
  Previously, the unset arguments contained whatever was left there
  from earlier function calls.
- Error if two labels with the same name are defined in a function

## 1.6.0

Add missing system functions and the `share[]` array

.
