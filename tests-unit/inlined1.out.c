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
  /// Not inlined 1
  __a0 = 1;
  __a1 = 2;
  __sp -= 1;
  ram[__sp] = 1;
  goto __fn4_not_inlined_add;
  label __rp1:
  __t0 = __rval;
  echo(__t0);
  /// Not inlined 2
  __a0 = 3;
  __a1 = 4;
  __sp -= 1;
  ram[__sp] = 2;
  goto __fn4_not_inlined_add;
  label __rp2:
  __t0 = __rval;
  echo(__t0);
  /// Inlined
  __t1 = 5;
  __t2 = 6;
  __rval = (__t1 + __t2);
  __t0 = __rval;
  echo(__t0);
  /// Inlined2
  __t1 = 5;
  __t2 = 6;
  __rval = (__t1 + __t2);
  __t0 = __rval;
  echo(__t0);
  /// Inlined nested
  __t1 = 7;
  __t2 = 8;
  __t4 = __t1;
  __t5 = __t2;
  __rval = (__t4 + __t5);
  __t3 = __rval;
  __rval = (__t3 * 2);
  __t0 = __rval;
  __t3 = ((2 * __t0) + 2);
  echo(__t3);
  /// no return inline
  echo('cau');
  __rval = 0;
  goto __main_loop;
  label __fn4_not_inlined_add:
  __sp -= 1;
  ram[__sp] = __t0;
  __sp -= 1;
  ram[__sp] = __t1;
  __t0 = __a0;
  __t1 = __a1;
  __rval = (__t0 + __t1);
  __t1 = ram[__sp];
  __sp += 1;
  __t0 = ram[__sp];
  __sp += 1;
  __addr = ram[__sp];
  __sp += 1;
  if (__addr == 1) goto __rp1;
  if (__addr == 2) goto __rp2;
}
