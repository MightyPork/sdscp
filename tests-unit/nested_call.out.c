var __a0;
var __a1;
var __a2;
var __a3;
var __a4;
var __a5;
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
  __a0 = 3;
  __a1 = 4;
  __sp -= 1;
  ram[__sp] = 1;
  goto __fn2_add2;
  label __rp1:
  __t1 = __rval;
  __a0 = 7;
  __a1 = 8;
  __sp -= 1;
  ram[__sp] = 2;
  goto __fn2_add2;
  label __rp2:
  __t2 = __rval;
  __a0 = 6;
  __a1 = __t2;
  __sp -= 1;
  ram[__sp] = 3;
  goto __fn2_add2;
  label __rp3:
  __t2 = __rval;
  __a0 = 1;
  __a1 = 2;
  __a2 = __t1;
  __a3 = 5;
  __a4 = __t2;
  __a5 = 9;
  __sp -= 1;
  ram[__sp] = 4;
  goto __fn1_add6;
  label __rp4:
  __t1 = __rval;
  __t0 = __t1;
  if (__t0 != 45) {
    echo('BAD SUM!');
  } else {
    echo('OK: ', __t0);
  }
  goto __main_loop;
  label __fn1_add6:
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
  __t2 = __a2;
  __t3 = __a3;
  __t4 = __a4;
  __t5 = __a5;
  __rval = (((((__t0 + __t1) + __t2) + __t3) + __t4) + __t5);
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
  label __fn2_add2:
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
  if (__addr == 3) goto __rp3;
}
