var __a0;
var __a1;
var __addr;
var __rval;
var __sp;
var __t0;
var __t1;

main
{
  __sp = 512;
  label __main_loop:
  __a0 = 1;
  __a1 = 2;
  __sp -= 1;
  ram[__sp] = 1;
  goto __fn1_add;
  label __rp1:
  __t0 = __rval;
  echo(__t0, ' Hello World!');
  goto __main_loop;
  label __fn1_add:
  __sp -= 1;
  ram[__sp] = __t0;
  __sp -= 1;
  ram[__sp] = __t1;
  __t0 = __a0;
  __t1 = __a1;
  /// Add
  __rval = (__t0 + __t1);
  __t1 = ram[__sp];
  __sp += 1;
  __t0 = ram[__sp];
  __sp += 1;
  __sp += 1;
  goto __rp1;
}
