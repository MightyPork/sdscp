var __addr;
var __rval;
var __sp;
var __t0;

main
{
  __sp = 512;
  label __main_loop:
  __t0 = 0;
  label __for_test_1:
  if (! (__t0 < 10)) goto __for_break_1;
  __sp -= 1;
  ram[__sp] = 1;
  goto __fn1_bar;
  label __rp1:
  if (0) {
    goto __for_break_1;
  }
  if (0) {
    goto __for_cont_1;
  }
  echo('yo');
  label __for_cont_1:
  __t0 += 1;
  goto __for_test_1;
  label __for_break_1:
  goto __main_loop;
  label __fn1_bar:
  __rval = 0;
  echo('foo');
  __sp += 1;
  goto __rp1;
}
