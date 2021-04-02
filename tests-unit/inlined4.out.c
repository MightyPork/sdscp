var __addr;
var __rval;
var __sp;

main
{
  __sp = 512;
  label __main_loop:
  /// inl1
  __sp -= 1;
  ram[__sp] = 1;
  goto __fn3_not_inlined;
  label __rp1:
  __rval = 0;
  /// inl2
  __sp -= 1;
  ram[__sp] = 2;
  goto __fn3_not_inlined;
  label __rp2:
  __rval = 0;
  goto __main_loop;
  label __fn3_not_inlined:
  echo('Not inlined');
  __rval = 0;
  __addr = ram[__sp];
  __sp += 1;
  if (__addr == 1) goto __rp1;
  if (__addr == 2) goto __rp2;
}
