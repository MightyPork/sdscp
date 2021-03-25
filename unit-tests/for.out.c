var __addr;
var __rval;
var __sp;
var __t0;
var __t1;

main
{
  __sp = 512;
  label __main_loop:
  /// No braces
  __t0 = 0;
  label __for_test_1:
  if (! (__t0 < 10)) goto __for_break_1;
  echo('Cycle ', __t0);
  __t0 += 1;
  goto __for_test_1;
  label __for_break_1:
  /// Complex test
  __t0 = 0;
  __t1 = 150;
  /// !
  __t0 = 0;
  label __for_test_2:
  if (! ((__t0 < 100) && (__t1 == 150))) goto __for_break_2;
  echo('Cycle ', __t0);
  __t0 += 1;
  goto __for_test_2;
  label __for_break_2:
  /// Empty init
  __t0 = 0;
  /// !
  label __for_test_3:
  if (! (__t0 < 100)) goto __for_break_3;
  echo('Cycle ', __t0);
  __t0 += 1;
  goto __for_test_3;
  label __for_break_3:
  /// Empty init and increment
  __t0 = 0;
  /// !
  label __for_test_4:
  if (! (__t0 < 100)) goto __for_break_4;
  echo('Cycle ', __t0);
  __t0 += 10;
  goto __for_test_4;
  label __for_break_4:
  /// Infinite loop
  label __for_test_5:
  if (! 1) goto __for_break_5;
  echo('Loop');
  goto __for_test_5;
  label __for_break_5:
  /// Continue
  __t0 = 0;
  label __for_test_6:
  if (! (__t0 < 10)) goto __for_break_6;
  echo('Loop');
  if (sys[10]) {
    goto __for_cont_6;
  }
  echo('Tail');
  label __for_cont_6:
  __t0 += 1;
  goto __for_test_6;
  label __for_break_6:
  /// Continue inner
  __t0 = 0;
  label __for_test_7:
  if (! (__t0 < 10)) goto __for_break_7;
  echo('Loop');
  __t1 = 0;
  label __for_test_8:
  if (! (__t1 < 10)) goto __for_break_8;
  echo('Loop2');
  if (sys[10]) {
    goto __for_cont_8;
  }
  echo('Tail');
  label __for_cont_8:
  __t1 += 1;
  goto __for_test_8;
  label __for_break_8:
  __t0 += 1;
  goto __for_test_7;
  label __for_break_7:
  /// Break
  __t0 = 0;
  label __for_test_9:
  if (! (__t0 < 10)) goto __for_break_9;
  echo('Loop');
  if (sys[10]) {
    goto __for_break_9;
  }
  echo('Tail');
  __t0 += 1;
  goto __for_test_9;
  label __for_break_9:
  /// Break inner
  __t0 = 0;
  label __for_test_10:
  if (! (__t0 < 10)) goto __for_break_10;
  echo('Loop');
  __t1 = 0;
  label __for_test_11:
  if (! (__t1 < 10)) goto __for_break_11;
  echo('Loop2');
  if (sys[10]) {
    goto __for_break_11;
  }
  echo('Tail');
  __t1 += 1;
  goto __for_test_11;
  label __for_break_11:
  __t0 += 1;
  goto __for_test_10;
  label __for_break_10:
  goto __main_loop;
}
