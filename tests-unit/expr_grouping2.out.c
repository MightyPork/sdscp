var __addr;
var __rval;
var __sp;
var v;

main
{
  __sp = 512;
  v = (! 0) + 1;
  if (v != 2) {
    echo('Test 1 failed');
  }
  v = (1 + 1) << 5;
  if (v != 64) {
    echo('Test 2 failed: ', v);
  }
  v = (3 - 1) << 5;
  if (v != 64) {
    echo('Test 3 failed: ', v);
  }
  v = 1 << (3 + 2);
  if (v != 32) {
    echo('Test 4 failed: ', v);
  }
  v = 1 << (7 - 2);
  if (v != 32) {
    echo('Test 5 failed: ', v);
  }
  v = (9 - 5) < 5;
  if (v != 1) {
    echo('Test 6 failed: ', v);
  }
  v = (1 << 3) == 8;
  if (v != 1) {
    echo('Test 7 failed: ', v);
  }
  v = (1 << 4) | (1 << 1);
  if (v != 18) {
    echo('Test 8 failed: ', v);
  }
  v = (15 * 1) | (100 * 2);
  if (v != 207) {
    echo('Test 9 failed: ', v);
  }
  v = (10 < 100) == (4 < 5);
  if (v != 1) {
    echo('Test 10 failed: ', v);
  }
  v = (1 + (2 * 3)) - 4;
  if (v != 3) {
    echo('Test 11 failed: ', v);
  }
  v = 1 - (-1);
  if (v != 2) {
    echo('Test 12 failed: ', v);
  }
  v = 0x5FF & (-256);
  if (v != 1280) {
    echo('Test 13 failed: ', v);
  }
  v = 0x5FF & 0xFFFFFF00;
  if (v != 1280) {
    echo('Test 14 failed: ', v);
  }
  v = 0x80000000;
  if (v != 0x80000000) {
    echo('Test 15 failed: ', v);
  }
  echo('Tests done.');
  label __fnmainL_end:
  goto __fnmainL_end;
}
