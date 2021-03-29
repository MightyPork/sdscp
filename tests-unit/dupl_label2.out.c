var __addr;
var __rval;
var __sp;

main
{
  __sp = 512;
  /// Noreturn
  __sp -= 1;
  ram[__sp] = 1;
  goto __fn2_fuu2;
  label __fnmainL_omg:
  echo('yo');
  goto __fnmainL_omg;
  label __fn2_fuu2:
  label __fn2L_omg:
  echo('aaa');
  goto __fn2L_omg;
}
