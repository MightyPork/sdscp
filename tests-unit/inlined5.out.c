// Globals declaration
var __a0;
var __a1;
var __a2;
var __addr;
var __rval;
var __sp;
var __t0;
var __t1;
var __t2;

main
{
  // --------------------------------- FUNC: init() ---------------------------------
  __sp = 512;
  // --------------------------------- FUNC: main() ---------------------------------
  label __main_loop:
  // CALL: should_inline1()
  __a0 = 1;
  __a1 = 0x6002;
  __a2 = 4;
  __sp -= 1;
  ram[__sp] = 1;
  goto __fn2_should_inline1;
  label __rp1:
  goto __main_loop;
  // --------------------- FUNC should_inline1(addr,start,count) --------------------
  label __fn2_should_inline1:
  // Push used tmp vars
  __sp -= 1;
  ram[__sp] = __t0;
  __sp -= 1;
  ram[__sp] = __t1;
  __sp -= 1;
  ram[__sp] = __t2;
  // Function body
  // INLINED: inlined1()
  __t0 = __a0;
  __t1 = __a1;
  __t2 = __a2;
  // CALL: should_inline2()
  __a0 = 6;
  __sp -= 1;
  ram[__sp] = 2;
  goto __fn3_should_inline2;
  label __rp2:
  __rval = 0;
  // End of inlined inlined1
  /// Bug: __a0 used while clobbered in 'inlined1'
  echo(__a0, __a1, __a2);
  __rval = 0;
  // Pop used tmp vars
  __t2 = ram[__sp];
  __sp += 1;
  __t1 = ram[__sp];
  __sp += 1;
  __t0 = ram[__sp];
  __sp += 1;
  // Return to caller
  __sp += 1;
  // Only one caller
  goto __rp1;
  // --------------------------- FUNC should_inline2(len) ---------------------------
  label __fn3_should_inline2:
  // Function body
  __rval = 0;
  // Return to caller
  __sp += 1;
  // Only one caller
  goto __rp2;
}
