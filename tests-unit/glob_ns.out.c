var __a0;
var __a1;
var __addr;
var __rval;
var __sp;
var _skfk;
var k;
var u__fuck;
var u__sp;
var u__xx;
var u__xx1;
var u__xx2;
var uu__sp;

main
{
  __sp = 512;
  u__fuck = -10;
  u__sp = 10;
  uu__sp = 20;
  u__xx = 111;
  u__xx1 = 112;
  u__xx2 = 222;
  _skfk = 30;
  k = 40;
  label __main_loop:
  u__sp = 75;
  echo('yolo', u__sp);
  u__sp = 555;
  uu__sp = 99;
  __a0 = u__sp;
  __a1 = u__fuck;
  __sp -= 1;
  ram[__sp] = 1;
  goto __fn1_moo;
  label __rp1:
  echo('u__sp', uu__sp);
  echo('__sp', u__sp);
  goto __main_loop;
  label __fn1_moo:
  __rval = __a0 + __a1;
  __sp += 1;
  goto __rp1;
}
