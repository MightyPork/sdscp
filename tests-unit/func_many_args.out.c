var __a0;
var __a1;
var __a2;
var __a3;
var __a4;
var __a5;
var __a6;
var __a7;
var __a8;
var __a9;
var __a10;
var __a11;
var __a12;
var __a13;
var __a14;
var __a15;
var __a16;
var __a17;
var __a18;
var __a19;
var __a20;
var __a21;
var __a22;
var __a23;
var __a24;
var __a25;
var __addr;
var __rval;
var __sp;

main
{
  __sp = 512;
  label __main_loop:
  __a0 = 1;
  __a1 = 2;
  __a2 = 3;
  __a3 = 4;
  __a4 = 5;
  __a5 = 6;
  __a6 = 7;
  __a7 = 8;
  __a8 = 9;
  __a9 = 10;
  __a10 = 11;
  __a11 = 12;
  __a12 = 13;
  __a13 = 14;
  __a14 = 15;
  __a15 = 16;
  __a16 = 17;
  __a17 = 18;
  __a18 = 19;
  __a19 = 20;
  __a20 = 21;
  __a21 = 22;
  __a22 = 23;
  __a23 = 24;
  __a24 = 25;
  __a25 = 26;
  __sp -= 1;
  ram[__sp] = 1;
  goto __fn1_many_args;
  label __rp1:
  goto __main_loop;
  label __fn1_many_args:
  echo(__a0, __a1, __a2, __a3, __a4, __a5, __a6, __a7, __a8, __a9, __a10, __a11, __a12, __a13, __a14, __a15, __a16, __a17, __a18, __a19, __a20, __a21, __a22, __a23, __a24, __a25);
  __rval = 0;
  __sp += 1;
  goto __rp1;
}
