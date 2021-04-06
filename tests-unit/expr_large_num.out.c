var __a0;
var __addr;
var __rval;
var __sp;
var __t0;
var __t1;
var __t2;
var __t3;
var __t4;
var __t5;
var __t6;
var __t7;
var __t8;

main
{
  __sp = 512;
  label __main_loop:
  /// Echo with negative
  echo(-1);
  /// Call with negative
  __a0 = -1;
  __sp -= 1;
  ram[__sp] = 1;
  goto __fn1_foo;
  label __rp1:
  /// Assign negative
  __t0 = -1;
  /// Simplified expr resulting in negative
  __t1 = 0xfffffffc;
  /// becames too large for signed int
  __t2 = 0x80000000;
  /// Invert operator producing hex
  __t3 = 0x500;
  __t4 = __t3 & 0xffffff00;
  __t5 = 0xffffffff;
  __t6 = 0xffffffff;
  __t7 = 0x80000000;
  __t8 = 0x80000001;
  goto __main_loop;
  label __fn1_foo:
  __rval = 0;
  __sp += 1;
  goto __rp1;
}
