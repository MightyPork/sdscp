var __addr;
var __rval;
var __sp;
var __t0;
var __t1;

main
{
  __sp = 512;
  label __main_loop:
  __t0 = 0;
  label __for_test_1:
  if (! (__t0 < 100)) goto __for_break_1;
  __t1 = __t0 * 2;
  echo(__t1);
  __t0 += 1;
  goto __for_test_1;
  label __for_break_1:
  __t0 = 0;
  label __for_test_2:
  if (! (__t0 < 100)) goto __for_break_2;
  __t1 = __t0 * 3;
  echo(__t1);
  __t0 += 1;
  goto __for_test_2;
  label __for_break_2:
  goto __main_loop;
}
