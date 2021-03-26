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
  __t0 = 1;
  __t1 = 10;
  __t2 = 100;
  __t3 = 1000;
  echo(__t0, __t1, __t2, __t3);
  echo();
  echo('a', 'b', 'c', 'd', '|', 'e');
  echo('a', '|', 'b', 'c', 'd', 'e');
  echo('%s %s %s %s', 'a', 'b');
  echo('NO_VALUES');
  goto __main_loop;
}
