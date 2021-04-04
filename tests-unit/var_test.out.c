var __addr;
var __rval;
var __sp;
var __t0;
var __t1;
var a;
var b;

main
{
  __sp = 512;
  a = sys[15];
  __t0 = 12 + ram[59];
  __t1 = 12 + a;
  b = sys[__t0] + ram[__t1];
  __t0 = 230 + (sys[236] + 1);
  a = (b + sys[233]) + sys[__t0];
  label __main_loop:
  echo('Sup');
  goto __main_loop;
}
