/*******************************************************************************
 *   Test data collecting
 *   Test seskupeni vyrazu a jejich priority
 *   @Piduch
 ******************************************************************************/

#pragma keep_names true
#pragma comments true

var vys, aa, bb, cc;

main() {
   // vys = aa;
    vys = -bb;
    vys = aa - bb;
    vys = - aa - bb;
    vys = aa - - cc;
    vys = aa - cc + bb;
    vys = aa + bb + cc;
    vys = aa + bb + cc - aa + bb + cc * aa;
    vys = aa * bb - bb / cc + aa<<bb && cc - aa;

    if (aa<bb) cc = bb;
    if ((cc+aa+bb)||(aa-bb+cc)&&!(aa+bb-cc))  aa=cc;

    if (sys[17] - aa >= 10 || sys[17] < bb) {
        aa = sys[17];
    }

    if(!aa || bb == 0) {
		echo("fail");
	}
}
