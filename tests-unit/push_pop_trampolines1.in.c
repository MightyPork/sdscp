#pragma push_pop_trampolines true
//#pragma comments true
//#pragma safe_stack true
//#pragma builtin_logging true
//#pragma builtin_error_logging true

// This is a functional test

#define assert(cond, msg...) {
    if (!(cond)) {
        echo("Assert: ", ##msg);
        while(1) {}
    }
}

main() {
    var a = 1;
    var b = 2;
    var c = 3;
    var d = 4;
    four(7, 8, 9, 0);
    assert(a==1, "root a=", a);
    assert(b==2, "root b=", b);
    assert(c==3, "root c=", c);
    assert(d==4, "root d=", d);
}

four(a,b,c,d) {
    a = 10;
    b = 20;
    c = 30;
    d = 40;
    three(11, 22, 33);
    assert(a==10, "four a=", a);
    assert(b==20, "four b=", b);
    assert(c==30, "four c=", c);
    assert(d==40, "four d=", d);
}

three(a,b,c) {
    a = 100;
    b = 200;
    c = 300;
    // An inner call is needed, so that arguments are assigned to temporaries and
    // those become clobbered. Otherwise it would work directly with the argument registers.
    nop();
}

nop() {}
