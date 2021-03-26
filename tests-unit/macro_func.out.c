var __addr;
var __rval;
var __sp;
var __t0;
var __t1;

main
{
  __sp = 512;
  label __main_loop:
  __t0 = 25;
  __t1 = (((__t0 > 13) * 666) + ((1 - (__t0 > 13)) * 471));
  echo(__t0, __t1);
  goto __main_loop;
}
