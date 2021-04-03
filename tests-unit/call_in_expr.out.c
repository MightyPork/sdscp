var __a0;
var __a1;
var __addr;
var __rval;
var __sp;
var __t0;

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
  /// Add
  __rval = (__a0 + __a1);
  __sp += 1;
  goto __rp1;
}
