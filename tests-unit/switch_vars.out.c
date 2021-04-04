var __addr;
var __rval;
var __sp;
var __t0;
var __t1;
var __t2;

main
{
  __sp = 512;
  label __main_loop:
  __t0 = 20;
  if (__t0 != 10) goto __case_2;
  __t1 = 15;
  __t2 = __t1 + 1;
  echo('10 ', __t2);
  goto __sw_break_1;
  label __case_2:
  if (__t0 != 11) goto __case_3;
  __t1 = 16;
  __t2 = __t1 + 1;
  echo('11 ', __t2);
  goto __case_matched_3;
  label __case_3:
  if (__t0 != 12) goto __case_4;
  label __case_matched_3:
  __t1 = 17;
  __t2 = __t1 + 1;
  echo('12 ', __t2);
  goto __sw_break_1;
  label __case_4:
  __t1 = 18;
  __t2 = __t1 + 1;
  echo('default', __t2);
  label __sw_break_1:
  goto __main_loop;
}
