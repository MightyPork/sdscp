var __a0;
var __a1;
var __a2;
var __a3;
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
  label __main_loop:
  __t0 = 1;
  __t1 = 2;
  __t2 = 3;
  __t3 = 4;
  __a0 = 7;
  __a1 = 8;
  __a2 = 9;
  __a3 = 0;
  __sp -= 1;
  ram[__sp] = 1;
  goto __fn1_four;
  label __rp1:
  if (! (__t0 == 1)) {
    echo('Assert: ', 'root a=', __t0);
    label __wh_cont_1:
    if (! 1) goto __wh_break_1;
    goto __wh_cont_1;
    label __wh_break_1:
  }
  if (! (__t1 == 2)) {
    echo('Assert: ', 'root b=', __t1);
    label __wh_cont_2:
    if (! 1) goto __wh_break_2;
    goto __wh_cont_2;
    label __wh_break_2:
  }
  if (! (__t2 == 3)) {
    echo('Assert: ', 'root c=', __t2);
    label __wh_cont_3:
    if (! 1) goto __wh_break_3;
    goto __wh_cont_3;
    label __wh_break_3:
  }
  if (! (__t3 == 4)) {
    echo('Assert: ', 'root d=', __t3);
    label __wh_cont_4:
    if (! 1) goto __wh_break_4;
    goto __wh_cont_4;
    label __wh_break_4:
  }
  goto __main_loop;
  label __fn1_four:
  __addr = 1;
  goto __push_tmps_4;
  label __fn1_push_tmps_end:
  __t0 = __a0;
  __t1 = __a1;
  __t2 = __a2;
  __t3 = __a3;
  __t0 = 10;
  __t1 = 20;
  __t2 = 30;
  __t3 = 40;
  __a0 = 11;
  __a1 = 22;
  __a2 = 33;
  __sp -= 1;
  ram[__sp] = 2;
  goto __fn2_three;
  label __rp2:
  if (! (__t0 == 10)) {
    echo('Assert: ', 'four a=', __t0);
    label __wh_cont_5:
    if (! 1) goto __wh_break_5;
    goto __wh_cont_5;
    label __wh_break_5:
  }
  if (! (__t1 == 20)) {
    echo('Assert: ', 'four b=', __t1);
    label __wh_cont_6:
    if (! 1) goto __wh_break_6;
    goto __wh_cont_6;
    label __wh_break_6:
  }
  if (! (__t2 == 30)) {
    echo('Assert: ', 'four c=', __t2);
    label __wh_cont_7:
    if (! 1) goto __wh_break_7;
    goto __wh_cont_7;
    label __wh_break_7:
  }
  if (! (__t3 == 40)) {
    echo('Assert: ', 'four d=', __t3);
    label __wh_cont_8:
    if (! 1) goto __wh_break_8;
    goto __wh_cont_8;
    label __wh_break_8:
  }
  __rval = 0;
  __sp += 4;
  __addr = 1;
  goto __pop_tmps_4;
  label __fn1_pop_tmps_end:
  __sp += 4;
  __sp += 1;
  goto __rp1;
  label __fn2_three:
  __addr = 2;
  goto __push_tmps_3;
  label __fn2_push_tmps_end:
  __t0 = __a0;
  __t1 = __a1;
  __t2 = __a2;
  __t0 = 100;
  __t1 = 200;
  __t2 = 300;
  __sp -= 1;
  ram[__sp] = 3;
  goto __fn3_nop;
  label __rp3:
  __rval = 0;
  __sp += 3;
  __addr = 2;
  goto __pop_tmps_3;
  label __fn2_pop_tmps_end:
  __sp += 3;
  __sp += 1;
  goto __rp2;
  label __fn3_nop:
  __rval = 0;
  __sp += 1;
  goto __rp3;
  label __err_bad_addr:
  label __push_tmps_4:
  __sp -= 1;
  ram[__sp] = __t3;
  label __push_tmps_3:
  __sp -= 1;
  ram[__sp] = __t2;
  __sp -= 1;
  ram[__sp] = __t1;
  __sp -= 1;
  ram[__sp] = __t0;
  if (__addr == 1) goto __fn1_push_tmps_end;
  if (__addr == 2) goto __fn2_push_tmps_end;
  goto __err_bad_addr;
  label __pop_tmps_4:
  __sp -= 1;
  __t3 = ram[__sp];
  label __pop_tmps_3:
  __sp -= 1;
  __t2 = ram[__sp];
  __sp -= 1;
  __t1 = ram[__sp];
  __sp -= 1;
  __t0 = ram[__sp];
  if (__addr == 1) goto __fn1_pop_tmps_end;
  if (__addr == 2) goto __fn2_pop_tmps_end;
  goto __err_bad_addr;
}
