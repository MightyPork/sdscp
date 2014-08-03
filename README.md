SDS-C Plus
==========

The goal of this project is to enable better coding practices and more powerful features in the SDS-C scripting language.

It takes a SDS-C Plus source code, and digests it into a format compatible with the official SDS-C compiler (that is, ugly code).

Things that will be added
-------------------------

- [x] Cleaning source (removing comments)
- [x] `#include` directive
- [x] Branching using `#ifdef`, `#ifndef`, `#endif`, `#else`
- [x] Constant macros with `#define`
- [x] Function-like macros with `#define`
- [x] Using macros in another macros
- [ ] Code tokenization & conversion to an AST **Partially done**
- [x] Output to file
- [x] Verbose mode

...
