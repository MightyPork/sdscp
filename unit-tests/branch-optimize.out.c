var __addr;
var __rval;
var __sp;
var __t0;

main
{
  __sp = 512;
  label __main_loop:
  __t0 = 15;
  /// Always false
  /// Always true 1
  echo('Always run 1');
  /// Always true 2
  echo('Always run 2');
  /// Always true 3
  echo('Always run 3');
  /// Always true 4
  echo('Always run 4');
  /// Infinite loop while
  label __wh_cont_1:
  echo('Cycle');
  goto __wh_cont_1;
  label __wh_break_1:
  /// Infinite loop do-while
  label __dowh_body_1:
  echo('Cycle');
  goto __dowh_body_1;
  /// Do-while-false
  label __dowh_body_2:
  echo('Cycle');
  /// Do-while-false with dead code
  echo('Cycle');
  /// FOR Dead code removal with continue
  __t0 = 0;
  label __for_test_1:
  if (! (__t0 < 10)) goto __for_break_1;
  echo('Loop');
  __t0 += 1;
  goto __for_test_1;
  label __for_break_1:
  /// FOR Dead code removal with break
  __t0 = 0;
  if (! (__t0 < 10)) goto __for_break_2;
  echo('Loop');
  label __for_break_2:
  goto __main_loop;
}
