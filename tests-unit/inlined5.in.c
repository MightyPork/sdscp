#pragma inline_one_use_functions true
#pragma comments true

inlined(addr, start, count) {
  should_inline2(/* clobbering __a0 */ 6);
}

// Used in main() and in unused1(), which is unused
should_inline1(addr, start, count) {
  inlined(addr, start, count);
  /// Bug: __a0 used while clobbered in 'inlined1'
  echo(addr, start, count);
}

should_inline2(len) {}

unused1(addr, start, count, store_at) {
  should_inline1(addr, start, count);
}

unused2() {
  should_inline2(0);
}

main() {
    should_inline1(1, 0x6002, 4);
}
