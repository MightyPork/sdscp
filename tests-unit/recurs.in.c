// This demo, more than anything, shows stack safeguards
// and error handling on stack overflow.

#pragma safe_stack true
#pragma builtin_error_logging true
#pragma stack_start 100

main(){
	echo("*** ", sum(100));
}

sum(n)
{
    //echo("at ", n);
    /// SUM func
	if(n == 1) return 1;
    // These are allocated for the sole purpose of inflating the stack
	var m = n + sum(n-1);
    //echo("ret ", m);
    return m;
}
