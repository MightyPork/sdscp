var __addr;
var __rval;
var __sp;

main
{
  __sp = 512;
  /// Normal func
  __sp -= 1;
  ram[__sp] = 1;
  goto __fn1_fuu;
  label __rp1:
  /// Main loop
  label __fnmainL_omg:
  echo('yo');
  goto __fnmainL_omg;
  label __fn1_fuu:
  label __fn1L_omg:
  echo('aaa');
  if (sys[15]) {
    goto __fn1L_omg;
  }
  __rval = 0;
  __sp += 1;
  goto __rp1;
}
