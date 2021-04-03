var __addr;
var __rval;
var __sp;
var __t0;

main
{
  __sp = 512;
  label __main_loop:
  __t0 = text[15];
  if (__t0 != 10) goto __case_2;
  echo('One');
  goto __sw_break_1;
  label __case_2:
  echo('Default');
  /// Fall though to 20
  echo('Two');
  label __sw_break_1:
  goto __main_loop;
}
