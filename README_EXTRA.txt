# Pragmas

Default pragma settings:

```c
#pragma safe_stack true
#pragma stack_start 300
#pragma stack_end 511
#pragma keep_names false
#pragma show_trace false
#pragma fullspeed true
#pragma builtin_logging true
#pragma builtin_error_logging true
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
