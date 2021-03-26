var __a0;
var __addr;
var __rval;
var __sp;
var __t0;
var __t1;
var __t2;

main
{
  label __reset:
  __sp = 512;
  label __main_loop:
  __a0 = 100;
  __sp -= 1;
  if (__sp < 100) goto __err_so;
  ram[__sp] = 1;
  goto __fn1_sum;
  label __rp1:
  __t0 = __rval;
  echo('*** ', __t0);
  goto __main_loop;
  label __fn1_sum:
  __sp -= 1;
  if (__sp < 100) goto __err_so;
  ram[__sp] = __t0;
  __sp -= 1;
  if (__sp < 100) goto __err_so;
  ram[__sp] = __t1;
  __sp -= 1;
  if (__sp < 100) goto __err_so;
  ram[__sp] = __t2;
  __t0 = __a0;
  __rval = 0;
  /// SUM func
  if (__t0 == 1) {
    __rval = 1;
    goto __fn1_end;
  }
  __a0 = (__t0 -1);
  __sp -= 1;
  if (__sp < 100) goto __err_so;
  ram[__sp] = 2;
  goto __fn1_sum;
  label __rp2:
  __t2 = __rval;
  __t1 = (__t0 + __t2);
  __rval = __t1;
  label __fn1_end:
  if (__sp > 511) goto __err_su;
  __t2 = ram[__sp];
  __sp += 1;
  if (__sp > 511) goto __err_su;
  __t1 = ram[__sp];
  __sp += 1;
  if (__sp > 511) goto __err_su;
  __t0 = ram[__sp];
  __sp += 1;
  if (__sp > 511) goto __err_su;
  __addr = ram[__sp];
  __sp += 1;
  if (__addr == 1) goto __rp1;
  if (__addr == 2) goto __rp2;
  goto __err_bad_addr;
  label __err_so:
  echo('[ERROR] Stack overflow!');
  goto __reset;
  label __err_su:
  echo('[ERROR] Stack underflow!');
  goto __reset;
  label __err_bad_addr:
  echo('[ERROR] Bad address!');
  goto __reset;
}
