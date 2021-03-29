# Changelog

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
