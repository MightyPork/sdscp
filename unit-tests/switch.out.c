var __addr;
var __rval;
var __sp;
var __t0;

main
{
  __sp = 512;
  label __main_loop:
  __t0 = 20;
  if (__t0 != 10) goto __case_2;
  echo('One');
  goto __sw_break_1;
  label __case_2:
  if (__t0 != 20) goto __case_3;
  echo('Two');
  goto __sw_break_1;
  label __case_3:
  if (__t0 != 30) goto __case_4;
  echo('Three');
  /// Fall-through
  goto __case_matched_4;
  label __case_4:
  if (__t0 != 40) goto __case_5;
  label __case_matched_4:
  /// Fall-through to default
  label __case_5:
  echo('Default');
  label __sw_break_1:
  /// --- Early default
  __t0 = 15;
  if (__t0 != 10) goto __case_8;
  echo('One');
  goto __sw_break_2;
  label __case_8:
  echo('Default');
  /// Fall though to 20
  echo('Two');
  label __sw_break_2:
  goto __main_loop;
}
