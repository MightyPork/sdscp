var __addr;
var __rval;
var __sp;

main
{
  __sp = 512;
  label __main_loop:
  echo('String', 'String with spaces', 'apos\' and "quote', 'newline\nescape');
  echo(97, 115, 99, 105, 105);
  echo(0, 1, -1, 2147483647, -2147483647);
  echo(0xF, 0xFF, 0x01234567, 0x89ABCDEF, 0xFFFFFFFF);
  echo(0xF, 0xFF, 0x01234567);
  echo(0b0, 0b111000111, 0b1111111111111111111111111111111, 0b11111111, 0b11111111);
  goto __main_loop;
}
