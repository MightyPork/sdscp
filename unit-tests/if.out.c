var __addr;
var __rval;
var __sp;
var __t0;

main
{
  __sp = 512;
  label __main_loop:
  __t0 = 15;
  /// Simple expr
  if (__t0 == 15) {
    echo('fifteen');
  }
  if (__t0 == 15) {
    echo('fifteen');
  }
  /// Variable only
  if (__t0) {
    echo('yes');
  }
  /// Always false
  /// Always true 1
  echo('Always run 1');
  /// Always true 2
  if (! 0) {
    echo('Always run 2');
  }
  /// Always true 3
  if (! 0) {
    echo('Always run 3');
  }
  /// Always true 4
  if (1) {
    echo('Always run 4');
  }
  /// Simple if-else
  if (__t0 == 12) {
    echo('yes');
  } else {
    echo('no');
  }
  /// No braces
  if (__t0 == 12) {
    echo('yes');
  } else {
    echo('no');
  }
  /// 2 chained
  if (__t0 == 1) {
    echo('One');
  } else {
    if (__t0 == 2) {
      echo('Two');
    }
  }
  /// 3 chained
  if (__t0 == 10) {
    echo('Ten');
  } else {
    if (__t0 == 20) {
      echo('Twenty');
    } else {
      if (__t0 == 30) {
        echo('Thirty');
      }
    }
  }
  /// 3 chained + else
  if (__t0 == 10) {
    echo('Ten');
  } else {
    if (__t0 == 20) {
      echo('Twenty');
    } else {
      if (__t0 == 30) {
        echo('Thirty');
      } else {
        echo('Other');
      }
    }
  }
  goto __main_loop;
}
