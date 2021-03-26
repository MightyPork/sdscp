var __addr;
var __rval;
var __sp;
var __t0;

main
{
  __sp = 512;
  label __main_loop:
  /// No braces
  label __wh_cont_1:
  if (! (sys[15] == 1)) goto __wh_break_1;
  echo('Cycle');
  goto __wh_cont_1;
  label __wh_break_1:
  /// Simple
  label __wh_cont_2:
  if (! (sys[15] == 1)) goto __wh_break_2;
  echo('Cycle');
  goto __wh_cont_2;
  label __wh_break_2:
  /// Infinite loop
  label __wh_cont_3:
  if (! 1) goto __wh_break_3;
  echo('Cycle');
  goto __wh_cont_3;
  label __wh_break_3:
  /// Simple do-while
  label __dowh_body_1:
  echo('Cycle');
  if (sys[15] == 1) goto __dowh_body_1;
  /// Infinite loop do-while
  label __dowh_body_2:
  echo('Cycle');
  if (1) goto __dowh_body_2;
  /// Do-while-false
  label __dowh_body_3:
  echo('Cycle');
  if (0) goto __dowh_body_3;
  /// Downcount
  __t0 = 100;
  label __wh_cont_4:
  if (! (__t0 > 10)) goto __wh_break_4;
  __t0 -= 1;
  echo(__t0);
  goto __wh_cont_4;
  label __wh_break_4:
  /// Nested
  label __wh_cont_5:
  if (! 1) goto __wh_break_5;
  label __dowh_body_4:
  echo('yo');
  if (1) goto __dowh_body_4;
  goto __wh_cont_5;
  label __wh_break_5:
  goto __main_loop;
}
