var __a0;
var __a1;
var __a2;
var __addr;
var __rval;
var __sp;
var __t0;
var __t1;
var __t2;
var __t3;

main
{
  __sp = 512;
  /// Three args with sub-call
  __t0 = 12 * sys[1053];
  __t1 = 99 + ram[__t0];
  __a0 = 12;
  __a1 = 84;
  __a2 = ram[17] + sys[__t1];
  __sp -= 1;
  ram[__sp] = 1;
  goto __fn1_three_args;
  label __rp1:
  /// Three args pure
  __a0 = 1;
  __a1 = 2;
  __a2 = 3;
  __sp -= 1;
  ram[__sp] = 2;
  goto __fn3_three_args_with_no_inner_calls;
  label __rp2:
  /// recurs
  __a0 = 5;
  __sp -= 1;
  ram[__sp] = 3;
  goto __fn4_recurs;
  label __rp3:
  /// goto moo
  label __fnmainL_moo:
  goto __fnmainL_moo;
  label __fn1_three_args:
  __sp -= 1;
  ram[__sp] = __t0;
  __sp -= 1;
  ram[__sp] = __t1;
  __sp -= 1;
  ram[__sp] = __t2;
  __sp -= 1;
  ram[__sp] = __t3;
  __t0 = __a0;
  __t1 = __a1;
  __t2 = __a2;
  __t3 = __t0 + __t1;
  echo('a + b =', __t3, ', c = ', __t2);
  __sp -= 1;
  ram[__sp] = 4;
  goto __fn2_foo;
  label __rp4:
  __rval = 0;
  __t3 = ram[__sp];
  __sp += 1;
  __t2 = ram[__sp];
  __sp += 1;
  __t1 = ram[__sp];
  __sp += 1;
  __t0 = ram[__sp];
  __sp += 1;
  __sp += 1;
  goto __rp1;
  label __fn2_foo:
  __rval = 0;
  __sp += 1;
  goto __rp4;
  label __fn3_three_args_with_no_inner_calls:
  __sp -= 1;
  ram[__sp] = __t0;
  __t0 = __a0 + __a1;
  echo('a + b =', __t0, ', c = ', __a2);
  __rval = 0;
  __t0 = ram[__sp];
  __sp += 1;
  __sp += 1;
  goto __rp2;
  label __fn4_recurs:
  __sp -= 1;
  ram[__sp] = __t0;
  __t0 = __a0;
  echo('Recurs ', __t0);
  if (__t0 == 0) {
    goto __fn4L_end;
  }
  /// Deeper
  __a0 = __t0 -1;
  __sp -= 1;
  ram[__sp] = 5;
  goto __fn4_recurs;
  label __rp5:
  label __fn4L_end:
  __rval = 0;
  __t0 = ram[__sp];
  __sp += 1;
  __addr = ram[__sp];
  __sp += 1;
  if (__addr == 3) goto __rp3;
  if (__addr == 5) goto __rp5;
}
