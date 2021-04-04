var __addr;
var __rval;
var __sp;
var a;

main
{
  __sp = 512;
  label __main_loop:
  echo('2^2 = ', 4);
  echo('10^3 = ', 1000);
  echo('1000^3 = ', 1000000000);
  a = 236;
  sys[a] = 1;
  sys[236] = 1;
  sys[64] = 6;
  label __fnmainL_foo:
  if (sys[64] == 0) {
    goto __fnmainL_foo;
  }
  a = 236;
  sys[a] = 0;
  goto __main_loop;
}
