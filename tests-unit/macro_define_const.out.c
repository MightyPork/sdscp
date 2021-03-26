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
  if (! (__t0 < 15)) goto __for_break_1;
  echo('A string macro.');
  __t0 += 1;
  goto __for_test_1;
  label __for_break_1:
  goto __main_loop;
}
