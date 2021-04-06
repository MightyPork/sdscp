#pragma push_pop_trampolines true

main() {
    three1(1, 2, 3);
    three2(4, 5, 6);
    two1(1, 2);
    two2(3, 4);
}

three1(a,b,c) { nop(); }
three2(a,b,c) { nop(); }
two1(a,b) { nop(); }
two2(a,b) { nop(); }

nop() {}
