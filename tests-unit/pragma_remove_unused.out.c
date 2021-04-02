var __addr;
var __rval;
var __sp;

main
{
  label __reset:
  label __init:
  __sp = 512;
  label __init_end:
  label __main_loop:
  goto __fnmainL_end;
  echo('not accessible!');
  label __fnmainL_bugger:
  label __fnmainL_stupid_nonsense:
  label __fnmainL_blabla:
  if (0) {
    echo('Never');
  }
  label __fnmainL_end:
  label __main_loop_end:
  goto __main_loop;
  label __fn1_unused:
  echo('Never used!!');
  __rval = 0;
  label __fn1_end:
  __addr = ram[__sp];
  __sp += 1;
  label __err_bad_addr:
}
