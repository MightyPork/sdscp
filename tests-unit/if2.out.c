var __addr;
var __rval;
var __sp;
var __t0;
var __t1;

main
{
  __sp = 512;
  __t0 = 12;
  __t1 = __t0 + 3;
  if ((__t0 == 32) || (sys[__t1] == (__t0 * 2))) {
    echo('Then');
  } else {
    echo('Else');
    echo('moo');
  }
  echo('[INFO] Program halted.');
  label __halt_loop:
  wait(1000);
  goto __halt_loop;
}
