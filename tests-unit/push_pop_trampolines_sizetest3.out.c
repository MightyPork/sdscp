var __a0;
var __a1;
var __a2;
var __addr;
var __rval;
var __sp;
var __t0;
var __t1;
var __t2;

main
{
  __sp = 512;
  label __main_loop:
  __a0 = 1;
  __a1 = 2;
  __a2 = 3;
  __sp -= 1;
  ram[__sp] = 1;
  goto __fn1_three1;
  label __rp1:
  __a0 = 1;
  __a1 = 2;
  __a2 = 3;
  __sp -= 1;
  ram[__sp] = 2;
  goto __fn2_three2;
  label __rp2:
  __a0 = 1;
  __a1 = 2;
  __a2 = 3;
  __sp -= 1;
  ram[__sp] = 3;
  goto __fn3_three3;
  label __rp3:
  __a0 = 1;
  __a1 = 2;
  __a2 = 3;
  __sp -= 1;
  ram[__sp] = 4;
  goto __fn4_three4;
  label __rp4:
  __a0 = 1;
  __a1 = 2;
  __a2 = 3;
  __sp -= 1;
  ram[__sp] = 5;
  goto __fn5_three5;
  label __rp5:
  goto __main_loop;
  label __fn1_three1:
  __addr = 1;
  goto __push_tmps_3;
  label __fn1_push_tmps_end:
  __t0 = __a0;
  __t1 = __a1;
  __t2 = __a2;
  __sp -= 1;
  ram[__sp] = 6;
  goto __fn6_nop;
  label __rp6:
  __rval = 0;
  __sp += 3;
  __addr = 1;
  goto __pop_tmps_3;
  label __fn1_pop_tmps_end:
  __sp += 3;
  __sp += 1;
  goto __rp1;
  label __fn2_three2:
  __addr = 2;
  goto __push_tmps_3;
  label __fn2_push_tmps_end:
  __t0 = __a0;
  __t1 = __a1;
  __t2 = __a2;
  __sp -= 1;
  ram[__sp] = 7;
  goto __fn6_nop;
  label __rp7:
  __rval = 0;
  __sp += 3;
  __addr = 2;
  goto __pop_tmps_3;
  label __fn2_pop_tmps_end:
  __sp += 3;
  __sp += 1;
  goto __rp2;
  label __fn3_three3:
  __addr = 3;
  goto __push_tmps_3;
  label __fn3_push_tmps_end:
  __t0 = __a0;
  __t1 = __a1;
  __t2 = __a2;
  __sp -= 1;
  ram[__sp] = 8;
  goto __fn6_nop;
  label __rp8:
  __rval = 0;
  __sp += 3;
  __addr = 3;
  goto __pop_tmps_3;
  label __fn3_pop_tmps_end:
  __sp += 3;
  __sp += 1;
  goto __rp3;
  label __fn4_three4:
  __addr = 4;
  goto __push_tmps_3;
  label __fn4_push_tmps_end:
  __t0 = __a0;
  __t1 = __a1;
  __t2 = __a2;
  __sp -= 1;
  ram[__sp] = 9;
  goto __fn6_nop;
  label __rp9:
  __rval = 0;
  __sp += 3;
  __addr = 4;
  goto __pop_tmps_3;
  label __fn4_pop_tmps_end:
  __sp += 3;
  __sp += 1;
  goto __rp4;
  label __fn5_three5:
  __addr = 5;
  goto __push_tmps_3;
  label __fn5_push_tmps_end:
  __t0 = __a0;
  __t1 = __a1;
  __t2 = __a2;
  __sp -= 1;
  ram[__sp] = 10;
  goto __fn6_nop;
  label __rp10:
  __rval = 0;
  __sp += 3;
  __addr = 5;
  goto __pop_tmps_3;
  label __fn5_pop_tmps_end:
  __sp += 3;
  __sp += 1;
  goto __rp5;
  label __fn6_nop:
  __rval = 0;
  __addr = ram[__sp];
  __sp += 1;
  if (__addr == 6) goto __rp6;
  if (__addr == 7) goto __rp7;
  if (__addr == 8) goto __rp8;
  if (__addr == 9) goto __rp9;
  if (__addr == 10) goto __rp10;
  label __err_bad_addr:
  label __push_tmps_3:
  __sp -= 1;
  ram[__sp] = __t2;
  __sp -= 1;
  ram[__sp] = __t1;
  __sp -= 1;
  ram[__sp] = __t0;
  if (__addr == 1) goto __fn1_push_tmps_end;
  if (__addr == 2) goto __fn2_push_tmps_end;
  if (__addr == 3) goto __fn3_push_tmps_end;
  if (__addr == 4) goto __fn4_push_tmps_end;
  if (__addr == 5) goto __fn5_push_tmps_end;
  goto __err_bad_addr;
  label __pop_tmps_3:
  __sp -= 1;
  __t2 = ram[__sp];
  __sp -= 1;
  __t1 = ram[__sp];
  __sp -= 1;
  __t0 = ram[__sp];
  if (__addr == 1) goto __fn1_pop_tmps_end;
  if (__addr == 2) goto __fn2_pop_tmps_end;
  if (__addr == 3) goto __fn3_pop_tmps_end;
  if (__addr == 4) goto __fn4_pop_tmps_end;
  if (__addr == 5) goto __fn5_pop_tmps_end;
  goto __err_bad_addr;
}
