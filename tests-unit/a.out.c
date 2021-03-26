var __addr;
var __rval;
var __sp;
var __t0;
var __t1;
var __t2;
var __t3;

main
{
  __sp = 512;
  label __main_loop:
  __t0 = 1122;
  __t1 = 15;
  __t2 = 0;
  label __for_test_1:
  if (! (__t2 < 100)) goto __for_break_1;
  __sp -= 1;
  ram[__sp] = 1;
  goto __fn1_do_stuff;
  label __rp1:
  __t2 += 1;
  goto __for_test_1;
  label __for_break_1:
  echo(' ');
  __t2 = __t0;
  if (__t2 != 7) goto __case_2;
  echo('7');
  goto __sw_break_1;
  label __case_2:
  __sp -= 1;
  ram[__sp] = 2;
  goto __fn2_get_magic_number;
  label __rp2:
  __t3 = __rval;
  if (__t2 != __t3) goto __case_3;
  echo('magic');
  goto __case_matched_3;
  label __case_3:
  if (__t2 != 111111111) goto __case_4;
  label __case_matched_3:
  echo('magic or 111111111');
  goto __sw_break_1;
  label __case_4:
  if (__t2 != __t1) goto __case_5;
  echo('yo');
  goto __case_matched_5;
  label __case_5:
  if (__t2 != 16) goto __case_6;
  label __case_matched_5:
  echo('yo or 16');
  goto __sw_break_1;
  label __case_6:
  __sp -= 1;
  ram[__sp] = 3;
  goto __fn3_one;
  label __rp3:
  __t3 = __rval;
  if (__t2 != ((1 + __t3) + __t1)) goto __case_7;
  echo('1+one()+yo');
  goto __sw_break_1;
  label __case_7:
  echo('default');
  label __sw_break_1:
  goto __main_loop;
  label __fn1_do_stuff:
  __rval = 0;
  echoinline('Stuff');
  __sp += 1;
  goto __rp1;
  label __fn2_get_magic_number:
  __rval = 0;
  __rval = 123456;
  __sp += 1;
  goto __rp2;
  label __fn3_one:
  __rval = 0;
  __rval = 1;
  __sp += 1;
  goto __rp3;
}
