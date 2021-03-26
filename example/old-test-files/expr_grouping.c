/*******************************************************************************
 *   Test data collecting
 *   Test seskupeni vyrazu a jejich priority
 *   @Piduch
 ******************************************************************************/

#pragma keep_names true
#pragma comments true

var vys, a, b, c;

main() {
   // vys = a;
    vys = -b;
    vys = a - b;
    vys = - a - b;
    vys = a - - c;
    vys = a - b + c;
    vys = a - b - b;
    vys = a - b - c + b;
    vys = a - b - c - b;
    vys = a - b - c - b - a;
    vys = a - b - c - b - a - b - c - b - a;
    vys = a + b + c;
    vys = a + b + c - a + b + c * a;
    vys = a * b - b / c + a<<b && c - a;
    vys = -b;
    vys = a - b;
    vys = a - - b;
    vys = + a - b;
    vys = - a - b;


    if (a<b) c = b;
    if ((c+a+b)||(a-b+c)&&!(a+b-c))  a=c;

    if (sys[17] - a >= 10 || sys[17] < b) {
        a = sys[17];
    }

    if(!a || b == 0) {
		echo("fail");
	}
}
