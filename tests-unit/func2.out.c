var __a0;
var __a1;
var __a2;
var __addr;
var __rval;
var __sp;
var __t0;
var __t1;
var __t2;
var a;
var b;
var c;

main
{
  __sp = 512;
  a = 12;
  b = 13;
  echo('Init');
  if (a == b) {
    echo('Yep');
  }
  label __main_loop:
  echo('Main, yo!');
  __a0 = 4;
  __a1 = 5;
  __a2 = 6;
  __sp -= 1;
  ram[__sp] = 1;
  goto __fn1_func_with_args;
  label __rp1:
  goto __main_loop;
  label __fn1_func_with_args:
  __sp -= 1;
  ram[__sp] = __t0;
  __sp -= 1;
  ram[__sp] = __t1;
  __sp -= 1;
  ram[__sp] = __t2;
  __t0 = __a0;
  __t1 = __a1;
  __t2 = __a2;
  echo('func_with_args');
  echo(__t0, ' is ', __t1, ' under ', __t2);
  __a0 = 77777;
  __sp -= 1;
  ram[__sp] = 2;
  goto __fn2_other_func;
  label __rp2:
  __rval = 0;
  __t2 = ram[__sp];
  __sp += 1;
  __t1 = ram[__sp];
  __sp += 1;
  __t0 = ram[__sp];
  __sp += 1;
  __sp += 1;
  goto __rp1;
  label __fn2_other_func:
  echo('other_func', __a0);
  __rval = 0;
  __sp += 1;
  goto __rp2;
}
