var __addr;
var __rval;
var __sp;

main
{
  __sp = 512;
  label __main_loop:
  http_get(198, 162, 11, 111, 'localhost', '(moo)index.php?a=', sys[459], '&foo=', 'bar');
  goto __main_loop;
}
