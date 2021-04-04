var __addr;
var __rval;
var __sp;
var __t0;
var __t1;
var __t2;
var __t3;
var __t4;
var __t5;
var __t6;
var __t7;
var __t8;
var __t9;
var __t10;
var __t11;
var __t12;
var __t13;

main
{
  __sp = 512;
  label __main_loop:
  __t0 = 15;
  /// Level 0
  __t2 = 1;
  __t3 = 2;
  __t4 = 3;
  /// Level 1
  __t7 = __t2;
  __t8 = __t3;
  /// Level 2
  __t11 = __t7;
  __t12 = __t8;
  /// Level 3
  __t13 = __t11 + __t12;
  /// End 3
  __t10 = __t13;
  __t9 = __t10;
  /// End 2
  __t6 = __t9;
  __t5 = __t6;
  /// End 1
  __t1 = __t5 + __t4;
  echo(__t1);
  /// End 0
  echo(__t0);
  goto __main_loop;
}
