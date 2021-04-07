
QUIET = False
SHOW_CALLGRAPH = False

# Pushing / popping two items produces less bytecode than a jump to trampoline
# (if provided safe stack is disabled)
PUSHPOP_TRAMPOLINE_MIN_TMP_COUNT = 3