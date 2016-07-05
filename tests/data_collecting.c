/*******************************************************************************
 *   Test data collecting
 *   Test seskupeni vyrazu a jejich priority
 *   @Piduch
 ******************************************************************************/

#pragma keep_names true
#pragma comments true

var vysledek, aa, bb, cc;
                                                                                                                                   
main() {

vysledek = aa;
vysledek = -bb;
vysledek = aa - bb;
vysledek = - aa - bb;
vysledek = aa - cc + bb;
vysledek = aa + bb + cc;
vysledek = aa + bb + cc - aa + bb + cc * aa;
vysledek = aa * bb - bb / cc + aa<<bb && cc - aa;

if (aa<bb) cc = bb; 
if ((cc+aa+bb)||(aa-bb+cc)&&!(aa+bb-cc))  aa=cc;


}
