var __addr;
var __rval;
var __sp;

main
{
  __sp = 512;
  label __fnmainL_retry:
  if (sys[1] == 0) {
    goto __fn1L_retry;
  }
  echo('cau');
  label __fn1L_retry:
  if (sys[1] == 1) {
    goto __fn2L_retry;
  }
  echo('cau');
  label __fn2L_retry:
  __rval = 5;
  __rval = 5;
  goto __fnmainL_retry;
}
