# Changelog

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
