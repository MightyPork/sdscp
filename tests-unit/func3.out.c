var __addr;
var __rval;
var __sp;
var __t0;
var __t1;

main
{
  __sp = 512;
  label __main_loop:
  __sp -= 1;
  ram[__sp] = 1;
  goto __fn1_return_zero;
  label __rp1:
  __t1 = __rval;
  __t0 = __t1;
  if (__t0 != 0) {
    echo('WHAT??!!');
  }
  goto __main_loop;
  label __fn1_return_zero:
  __sp -= 1;
  ram[__sp] = 2;
  goto __fn2_return_42;
  label __rp2:
  echo('cau');
  __rval = 0;
  __sp += 1;
  goto __rp1;
  label __fn2_return_42:
  __rval = 42;
  __sp += 1;
  goto __rp2;
}
