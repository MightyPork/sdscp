var __a0;
var __addr;
var __rval;
var __sp;
var __t0;

main
{
  __sp = 512;
  label __main_loop:
  __a0 = 15;
  __sp -= 1;
  ram[__sp] = 1;
  goto __fn1_a_func;
  label __rp1:
  goto __main_loop;
  label __fn1_a_func:
  __sp -= 1;
  ram[__sp] = __t0;
  __t0 = __a0;
  __sp -= 1;
  ram[__sp] = 2;
  goto __fn2_other_func;
  label __rp2:
  if (__t0 != 10) goto __case_2;
  echo('One');
  goto __sw_break_1;
  label __case_2:
  echo('Default');
  /// Fall though to 20
  echo('Two');
  label __sw_break_1:
  __rval = 0;
  __t0 = ram[__sp];
  __sp += 1;
  __sp += 1;
  goto __rp1;
  label __fn2_other_func:
  __rval = 0;
  __sp += 1;
  goto __rp2;
}
