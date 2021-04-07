#pragma push_pop_trampolines true

main() {
    one1(1);
    one2(2);
    two1(1, 2);
    two2(3, 4);
    three1(1, 2, 3);
    three2(4, 5, 6);
    four1(1, 2, 3, 4);
    four2(5, 6, 7, 8);
}

one1(a) { nop(); }
one2(a) { nop(); }

two1(a,b) { nop(); }
two2(a,b) { nop(); }

three1(a,b,c) { nop(); }
three2(a,b,c) { nop(); }

four1(a,b,c,d) { nop(); }
four2(a,b,c,d) { nop(); }

nop() {}
