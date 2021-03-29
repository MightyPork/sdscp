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
  __t0 = 192;
  __t1 = 168;
  __t2 = 0;
  __t3 = 10;
  http_get(__t0, __t1, __t2, __t3, 'localhost', 'HELLO?id=', 111222, '&such=', 'route', '&much=', 'awesome');
  __sp -= 1;
  ram[__sp] = 1;
  goto __fn1_wait_for_http_get;
  label __rp1:
  if (sys[123] == 456) {
    echo('GET success: ', text[0]);
  } else {
    echo('GET error: ', text[0]);
  }
  goto __main_loop;
  label __fn1_wait_for_http_get:
  wait(2000);
  __rval = 0;
  __sp += 1;
  goto __rp1;
}
