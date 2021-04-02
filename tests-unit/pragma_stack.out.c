var __addr;
var __rval;
var __sp;

main
{
  __sp = 201;
  label __main_loop:
  __sp -= 1;
  if (__sp < 100) goto __err_so;
  ram[__sp] = 1;
  goto __fn1_func;
  label __rp1:
  goto __main_loop;
  label __fn1_func:
  __sp -= 1;
  if (__sp < 100) goto __err_so;
  ram[__sp] = 2;
  goto __fn1_func;
  label __rp2:
  __rval = 0;
  if (__sp > 200) goto __err_su;
  __addr = ram[__sp];
  __sp += 1;
  if (__addr == 1) goto __rp1;
  if (__addr == 2) goto __rp2;
  goto __err_bad_addr;
  label __err_so:
  label __err_su:
  label __err_bad_addr:
}
