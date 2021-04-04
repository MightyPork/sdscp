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
  __t0 = 15;
  echo('a');
  /// First free block
  __t1 = 15;
  __t2 = __t1 + 1;
  echo(__t2);
  /// -- Nested free block 1
  __t2 = 15;
  echo(__t2);
  /// -- end block
  /// end block
  /// Second free block
  __t1 = 15;
  __t2 = __t1 + 1;
  echo(__t2);
  /// -- Nested free block 2
  __t2 = 15;
  echo(__t2);
  /// -- end block
  /// end block
  echo(__t0);
  goto __main_loop;
}
