#pragma simplify_expressions false

main()
{
    var f;
    // TODO "|"" looks like it might need higher associativity than compare operators
	var a1 =     12 +  47 *  ~   -5     +   -8    <<   4 / 2  + 1   >   ! 2 +    - f     * 14    | 2;
	var a2 =     12 +  47 *  ~  - 5     +  - 8    <<   4 / 2  + 1   >   ! 2 +    - f     * 14    | 2;
	var a3 = 5 * -1;
	var a4 = 5 * - 1;
	var a5 = 5 - -1;
	var a6 = 5 - - 1;
    // __t1 = (((((12 + (47 * (~ (- 5)))) + (- 8)) << ((4 / 2) + 1)) > ((! 2) + ((- __t0) * 14))) | 2);
	
	
}
