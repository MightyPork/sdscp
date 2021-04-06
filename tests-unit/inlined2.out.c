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
var __t9;
var __t10;
var __t11;
var __t12;
var __t13;

main
{
  __sp = 512;
  label __main_loop:
  __sp -= 1;
  ram[__sp] = 1;
  goto __fn1_inner;
  label __rp1:
  __sp -= 1;
  ram[__sp] = 2;
  goto __fn1_inner;
  label __rp2:
  goto __main_loop;
  label __fn1_inner:
  __sp -= 1;
  ram[__sp] = __t0;
  __sp -= 1;
  ram[__sp] = __t1;
  __sp -= 1;
  ram[__sp] = __t2;
  __sp -= 1;
  ram[__sp] = __t3;
  __sp -= 1;
  ram[__sp] = __t4;
  __sp -= 1;
  ram[__sp] = __t5;
  __sp -= 1;
  ram[__sp] = __t6;
  __sp -= 1;
  ram[__sp] = __t7;
  __sp -= 1;
  ram[__sp] = __t8;
  __sp -= 1;
  ram[__sp] = __t9;
  __sp -= 1;
  ram[__sp] = __t10;
  __sp -= 1;
  ram[__sp] = __t11;
  __sp -= 1;
  ram[__sp] = __t12;
  __sp -= 1;
  ram[__sp] = __t13;
  __t0 = 15;
  /// Level 0
  __t2 = 1;
  __t3 = 2;
  __t4 = 3;
  /// Level 1
  __t7 = __t2;
  __t8 = __t3;
  /// Level 2
  __t11 = __t7;
  __t12 = __t8;
  /// Level 3
  __t13 = __t11 + __t12;
  /// End 3
  __t10 = __t13;
  __t9 = __t10;
  /// End 2
  __t6 = __t9;
  __t5 = __t6;
  /// End 1
  __t1 = __t5 + __t4;
  echo(__t1);
  /// End 0
  echo(__t0);
  __rval = 0;
  __t13 = ram[__sp];
  __sp += 1;
  __t12 = ram[__sp];
  __sp += 1;
  __t11 = ram[__sp];
  __sp += 1;
  __t10 = ram[__sp];
  __sp += 1;
  __t9 = ram[__sp];
  __sp += 1;
  __t8 = ram[__sp];
  __sp += 1;
  __t7 = ram[__sp];
  __sp += 1;
  __t6 = ram[__sp];
  __sp += 1;
  __t5 = ram[__sp];
  __sp += 1;
  __t4 = ram[__sp];
  __sp += 1;
  __t3 = ram[__sp];
  __sp += 1;
  __t2 = ram[__sp];
  __sp += 1;
  __t1 = ram[__sp];
  __sp += 1;
  __t0 = ram[__sp];
  __sp += 1;
  __addr = ram[__sp];
  __sp += 1;
  if (__addr == 1) goto __rp1;
  if (__addr == 2) goto __rp2;
}
