SDS-C Plus
==========

The goal of this project is to enable better coding practices and more powerful features in the SDS-C scripting language.

It takes a SDS-C Plus source code, and digests it into a format compatible with the official SDS-C compiler (that is, ugly code).

Available Features
------------------

- Cleaning source (removing comments)
- `#include` directive
- Branching using `#ifdef`, `#ifndef`, `#endif`, `#else`
- Constant macros with `#define`
- Function-like macros with `#define`
- Using macros in another macros
- Output to file
- Verbose mode
- Code tokenization (partial)


Planned Features
----------------

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
