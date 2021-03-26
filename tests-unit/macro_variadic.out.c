var __addr;
var __rval;
var __sp;

main
{
  __sp = 512;
  label __main_loop:
  echo('one', 'two', 'three', 4, 5, 6, sys[123], 'dfgdfgsd');
  http_get(192, 165, 120, 11, 'localhost', 'index.php?a=', sys[140], '&b=', sys[445], '&c=', 'myVar');
  /// testing varargs at start
  echo(' b=', 'BBB', ' c=', 'CCC', 'other=', 'v', 'vv', 'vvv');
  echo(' b=', 'BBB', ' c=', 'CCC', 'other=', 'v');
  echo(' b=', 'BBB', ' c=', 'CCC', 'other=');
  /// at end (THE BEST OPTION)
  echo(' b=', 'BBB', ' c=', 'CCC', 'other=', 'v', 'vv', 'vvv');
  echo(' b=', 'BBB', ' c=', 'CCC', 'other=', 'v', 'vv');
  echo(' b=', 'BBB', ' c=', 'CCC', 'other=');
  /// anywhere in between
  echo(' b=', 'BBB', ' c=', 'CCC', ' d=', 'DDD', 'other=', 'v', 'vv', 'vvv');
  echo(' b=', 'BBB', ' c=', 'CCC', ' d=', 'DDD', 'other=', 'v');
  echo(' b=', 'BBB', ' c=', 'CCC', ' d=', 'DDD', 'other=');
  goto __main_loop;
}
