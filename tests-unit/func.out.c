var __a0;
var __a1;
var __addr;
var __rval;
var __sp;
var __t0;
var __t1;
var __t2;
var __t3;
var __t4;
var __t5;

main
{
  __sp = 512;
  label __main_loop:
  /// Call before
  __sp -= 1;
  ram[__sp] = 1;
  goto __fn1_before;
  label __rp1:
  /// Call after
  __sp -= 1;
  ram[__sp] = 2;
  goto __fn2_after;
  label __rp2:
  /// Store output to a variable
  __a0 = 4;
  __a1 = 5;
  __sp -= 1;
  ram[__sp] = 3;
  goto __fn4_add;
  label __rp3:
  __t1 = __rval;
  __t0 = __t1;
  echo(__t0);
  /// Call "variables"
  __a0 = 1;
  __a1 = 2;
  __sp -= 1;
  ram[__sp] = 4;
  goto __fn5_variables;
  label __rp4:
  __t2 = __rval;
  __t1 = __t2;
  /// Multiply nested call
  __a0 = 1;
  __a1 = 2;
  __sp -= 1;
  ram[__sp] = 5;
  goto __fn4_add;
  label __rp5:
  __t2 = __rval;
  __a0 = 5;
  __a1 = 6;
  __sp -= 1;
  ram[__sp] = 6;
  goto __fn4_add;
  label __rp6:
  __t3 = __rval;
  __a0 = 6;
  __a1 = 4 - __t3;
  __sp -= 1;
  ram[__sp] = 7;
  goto __fn4_add;
  label __rp7:
  __t3 = __rval;
  echo(__t2, __t3);
  goto __main_loop;
  label __fn1_before:
  /// Before
  echo('Hello');
  __rval = 0;
  __addr = ram[__sp];
  __sp += 1;
  if (__addr == 1) goto __rp1;
  if (__addr == 8) goto __rp8;
  goto __err_bad_addr;
  label __fn2_after:
  /// After
  echo('Hello');
  __rval = 0;
  __sp += 1;
  goto __rp2;
  label __fn4_add:
  __sp -= 1;
  ram[__sp] = __t0;
  __sp -= 1;
  ram[__sp] = __t1;
  __t0 = __a0;
  __t1 = __a1;
  /// Add a + b
  /// First, call before
  __sp -= 1;
  ram[__sp] = 8;
  goto __fn1_before;
  label __rp8:
  /// Return sum
  __rval = __t0 + __t1;
  __t1 = ram[__sp];
  __sp += 1;
  __t0 = ram[__sp];
  __sp += 1;
  __addr = ram[__sp];
  __sp += 1;
  if (__addr == 3) goto __rp3;
  if (__addr == 5) goto __rp5;
  if (__addr == 6) goto __rp6;
  if (__addr == 7) goto __rp7;
  if (__addr == 9) goto __rp9;
  goto __err_bad_addr;
  label __fn5_variables:
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
  __t0 = __a0;
  __t1 = __a1;
  /// Variable test
  __t2 = __t0;
  __t3 = __t2 + __t1;
  __t4 = __t2 + __t3;
  __t2 = __t4;
  __t0 = 15;
  __a0 = __t0;
  __a1 = __t1;
  __sp -= 1;
  ram[__sp] = 9;
  goto __fn4_add;
  label __rp9:
  __t5 = __rval;
  __rval = __t4 + __t5;
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
  __sp += 1;
  goto __rp4;
  label __err_bad_addr:
}
