#pragma push_pop_trampolines true
#pragma safe_stack true

// This should use trampolines if safe stack is enabled,
// the threshold is then lowered to 2

main() {
    two1(1, 2);
    two2(1, 2);
    two3(1, 2);
    two4(1, 2);
    two5(1, 2);
}

two1(a,b) { nop(); }
two2(a,b) { nop(); }
two3(a,b) { nop(); }
two4(a,b) { nop(); }
two5(a,b) { nop(); }

nop() {}
