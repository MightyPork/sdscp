var __addr;
var __rval;
var __sp;

main
{
  __sp = 512;
  label __main_loop:
  __sp -= 1;
  ram[__sp] = 1;
  goto __fn1_inlined;
  label __rp1:
  goto __main_loop;
  label __fn1_inlined:
  echo('aaa');
  __rval = 0;
  __sp += 1;
  goto __rp1;
}
