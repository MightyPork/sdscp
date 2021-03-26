var __addr;
var __rval;
var __sp;
var __t0;

main
{
  __sp = 512;
  echo('Cau');
  __t0 = 13;
  __sp -= 1;
  ram[__sp] = __t0;
  __t0 = 27;
  __t0 = ram[__sp];
  __sp += 1;
  echo(__t0);
  echo('[INFO] Program halted.');
  label __halt_loop:
  wait(1000);
  goto __halt_loop;
}
