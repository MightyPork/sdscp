# Pragmas

Default pragma settings:

```c
// Print error and restart on stack over/underflow 
#pragma safe_stack true

// Stack region in ram[] lower bound
#pragma stack_start 300

// Stack region in ram[] upper bound
#pragma stack_end 511

// Preserve original label/func/var names in the generated code
#pragma keep_names false

// Embed echo() calls tracing the control flow, only for sdscp debug
#pragma show_trace false

// Disable speed limiter at startup
#pragma fullspeed true

// Include built-in logging (e.g. "main started")
#pragma builtin_logging true

// Include built-in error logging.
// This is enabled independently of `builtin_logging`
#pragma builtin_error_logging true

// Inline functions used only once.
// Inlining speeds up execution and reduces code size. 
#pragma inline_one_use_functions true

// Remove dead code, e.g. unused functions, code after a goto,
// or unused labels.
#pragma remove_dead_code true

// Remove or unwrap IFs that are at compile time known to be always true or false
#pragma simplify_ifs true

// Simplify arithmetic expressions at compile time.
// This effectively evaluates any parts of an expression that doesn't use variables.
#pragma simplify_expressions true

// Use push-pop trampolines to optimize code size.
// Only meaningful if there are many functions with more than 2 arguments
#pragma push_pop_trampolines false
```

Other pragmas:

```
#pragma once
```

# Doc comments

The pre-processor normally discards all comments.

Sometimes we want to preserve a comment in the output, e.g. to mark a variable for easy manual 
editing. To do this, use three slashes: `/// This comment is not removed`

Doc comments (`///`) are supported inside functions, among code. It is NOT allowed in root scope 
(e.g. before a function or a global variable). Use a normal comment if needed.
