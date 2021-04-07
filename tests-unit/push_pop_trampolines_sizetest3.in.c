#pragma push_pop_trampolines true

// This test should have 3122 bytes after SDS-C compilation with trampolines disabled,
// and 2986 with them enabled.

main() {
    three1(1, 2, 3);
    three2(1, 2, 3);
    three3(1, 2, 3);
    three4(1, 2, 3);
    three5(1, 2, 3);
}

three1(a,b,c) { nop(); }
three2(a,b,c) { nop(); }
three3(a,b,c) { nop(); }
three4(a,b,c) { nop(); }
three5(a,b,c) { nop(); }

nop() {}
