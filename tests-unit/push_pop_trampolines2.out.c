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
  __a0 = 1;
  __sp -= 1;
  ram[__sp] = 1;
  goto __fn1_one1;
  label __rp1:
  __a0 = 2;
  __sp -= 1;
  ram[__sp] = 2;
  goto __fn2_one2;
  label __rp2:
  __a0 = 1;
  __a1 = 2;
  __sp -= 1;
  ram[__sp] = 3;
  goto __fn3_two1;
  label __rp3:
  __a0 = 3;
  __a1 = 4;
  __sp -= 1;
  ram[__sp] = 4;
  goto __fn4_two2;
  label __rp4:
  __a0 = 1;
  __a1 = 2;
  __a2 = 3;
  __sp -= 1;
  ram[__sp] = 5;
  goto __fn5_three1;
  label __rp5:
  __a0 = 4;
  __a1 = 5;
  __a2 = 6;
  __sp -= 1;
  ram[__sp] = 6;
  goto __fn6_three2;
  label __rp6:
  __a0 = 1;
  __a1 = 2;
  __a2 = 3;
  __a3 = 4;
  __sp -= 1;
  ram[__sp] = 7;
  goto __fn7_four1;
  label __rp7:
  __a0 = 5;
  __a1 = 6;
  __a2 = 7;
  __a3 = 8;
  __sp -= 1;
  ram[__sp] = 8;
  goto __fn8_four2;
  label __rp8:
  goto __main_loop;
  label __fn1_one1:
  __sp -= 1;
  ram[__sp] = __t0;
  __t0 = __a0;
  __sp -= 1;
  ram[__sp] = 9;
  goto __fn9_nop;
  label __rp9:
  __rval = 0;
  __t0 = ram[__sp];
  __sp += 1;
  __sp += 1;
  goto __rp1;
  label __fn2_one2:
  __sp -= 1;
  ram[__sp] = __t0;
  __t0 = __a0;
  __sp -= 1;
  ram[__sp] = 10;
  goto __fn9_nop;
  label __rp10:
  __rval = 0;
  __t0 = ram[__sp];
  __sp += 1;
  __sp += 1;
  goto __rp2;
  label __fn3_two1:
  __sp -= 1;
  ram[__sp] = __t0;
  __sp -= 1;
  ram[__sp] = __t1;
  __t0 = __a0;
  __t1 = __a1;
  __sp -= 1;
  ram[__sp] = 11;
  goto __fn9_nop;
  label __rp11:
  __rval = 0;
  __t1 = ram[__sp];
  __sp += 1;
  __t0 = ram[__sp];
  __sp += 1;
  __sp += 1;
  goto __rp3;
  label __fn4_two2:
  __sp -= 1;
  ram[__sp] = __t0;
  __sp -= 1;
  ram[__sp] = __t1;
  __t0 = __a0;
  __t1 = __a1;
  __sp -= 1;
  ram[__sp] = 12;
  goto __fn9_nop;
  label __rp12:
  __rval = 0;
  __t1 = ram[__sp];
  __sp += 1;
  __t0 = ram[__sp];
  __sp += 1;
  __sp += 1;
  goto __rp4;
  label __fn5_three1:
  __addr = 5;
  goto __push_tmps_3;
  label __fn5_push_tmps_end:
  __t0 = __a0;
  __t1 = __a1;
  __t2 = __a2;
  __sp -= 1;
  ram[__sp] = 13;
  goto __fn9_nop;
  label __rp13:
  __rval = 0;
  __sp += 3;
  __addr = 5;
  goto __pop_tmps_3;
  label __fn5_pop_tmps_end:
  __sp += 3;
  __sp += 1;
  goto __rp5;
  label __fn6_three2:
  __addr = 6;
  goto __push_tmps_3;
  label __fn6_push_tmps_end:
  __t0 = __a0;
  __t1 = __a1;
  __t2 = __a2;
  __sp -= 1;
  ram[__sp] = 14;
  goto __fn9_nop;
  label __rp14:
  __rval = 0;
  __sp += 3;
  __addr = 6;
  goto __pop_tmps_3;
  label __fn6_pop_tmps_end:
  __sp += 3;
  __sp += 1;
  goto __rp6;
  label __fn7_four1:
  __addr = 7;
  goto __push_tmps_4;
  label __fn7_push_tmps_end:
  __t0 = __a0;
  __t1 = __a1;
  __t2 = __a2;
  __t3 = __a3;
  __sp -= 1;
  ram[__sp] = 15;
  goto __fn9_nop;
  label __rp15:
  __rval = 0;
  __sp += 4;
  __addr = 7;
  goto __pop_tmps_4;
  label __fn7_pop_tmps_end:
  __sp += 4;
  __sp += 1;
  goto __rp7;
  label __fn8_four2:
  __addr = 8;
  goto __push_tmps_4;
  label __fn8_push_tmps_end:
  __t0 = __a0;
  __t1 = __a1;
  __t2 = __a2;
  __t3 = __a3;
  __sp -= 1;
  ram[__sp] = 16;
  goto __fn9_nop;
  label __rp16:
  __rval = 0;
  __sp += 4;
  __addr = 8;
  goto __pop_tmps_4;
  label __fn8_pop_tmps_end:
  __sp += 4;
  __sp += 1;
  goto __rp8;
  label __fn9_nop:
  __rval = 0;
  __addr = ram[__sp];
  __sp += 1;
  if (__addr == 9) goto __rp9;
  if (__addr == 10) goto __rp10;
  if (__addr == 11) goto __rp11;
  if (__addr == 12) goto __rp12;
  if (__addr == 13) goto __rp13;
  if (__addr == 14) goto __rp14;
  if (__addr == 15) goto __rp15;
  if (__addr == 16) goto __rp16;
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
  if (__addr == 5) goto __fn5_push_tmps_end;
  if (__addr == 6) goto __fn6_push_tmps_end;
  if (__addr == 7) goto __fn7_push_tmps_end;
  if (__addr == 8) goto __fn8_push_tmps_end;
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
  if (__addr == 5) goto __fn5_pop_tmps_end;
  if (__addr == 6) goto __fn6_pop_tmps_end;
  if (__addr == 7) goto __fn7_pop_tmps_end;
  if (__addr == 8) goto __fn8_pop_tmps_end;
  goto __err_bad_addr;
}
