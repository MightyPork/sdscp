var __a0;
var __a1;
var __a2;
var __addr;
var __rval;
var __sp;
var __t0;
var __t1;
var __t2;
var __t3;

main
{
  __sp = 512;
  /// Headed
  __t0 = (12 * sys[1053]);
  __t1 = (99 + ram[__t0]);
  __a0 = 12;
  __a1 = 84;
  __a2 = (ram[17] + sys[__t1]);
  __sp -= 1;
  ram[__sp] = 1;
  goto __fn1_headed;
  label __rp1:
  /// recurs
  __a0 = 5;
  __sp -= 1;
  ram[__sp] = 2;
  goto __fn2_recurs;
  label __rp2:
  /// goto moo
  label __fnmainL_moo:
  goto __fnmainL_moo;
  label __fn1_headed:
  __sp -= 1;
  ram[__sp] = __t0;
  __sp -= 1;
  ram[__sp] = __t1;
  __sp -= 1;
  ram[__sp] = __t2;
  __sp -= 1;
  ram[__sp] = __t3;
  __t0 = __a0;
  __t1 = __a1;
  __t2 = __a2;
  __t3 = (__t0 + __t1);
  echo('a + b =', __t3, ', c = ', __t2);
  __rval = 0;
  __t3 = ram[__sp];
  __sp += 1;
  __t2 = ram[__sp];
  __sp += 1;
  __t1 = ram[__sp];
  __sp += 1;
  __t0 = ram[__sp];
  __sp += 1;
  __sp += 1;
  goto __rp1;
  label __fn2_recurs:
  __sp -= 1;
  ram[__sp] = __t0;
  __t0 = __a0;
  echo('Recurs ', __t0);
  if (__t0 == 0) {
    goto __fn2L_end;
  }
  /// Deeper
  __a0 = (__t0 -1);
  __sp -= 1;
  ram[__sp] = 3;
  goto __fn2_recurs;
  label __rp3:
  label __fn2L_end:
  __rval = 0;
  __t0 = ram[__sp];
  __sp += 1;
  __addr = ram[__sp];
  __sp += 1;
  if (__addr == 2) goto __rp2;
  if (__addr == 3) goto __rp3;
}
