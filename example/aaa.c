// Makro v makru
#define RELE1 sys[231]
#define SVETLO RELE1
// teď funguje!


// Malá pásmena v názvu makra!
#define verze "4.5.6" // <-- Dvojté uvozovky


// Funkční makro
#define Secti(a, b) ((a) + (b))


// Makro s hranatými závorkami (array-like)
#define SQUARES[i] ((i) * (i))
// např. SQUARES[4]

// Zatím nefunguje (omezení SDS-C), ale brzo bude!
#define RELE[i] sys[230 + (i)]


// Podmíněné větvení překladu

#define DEBUG

#ifdef DEBUG
	echo("Dlouha debug zprava");
	echo("Dalsi debuga");
#else
	echo("Strucna zprava");
#endif


// SDSCP pochopitelně umí #include :)

#include "konstanty.c"
#include "utility.c"


// === Tohle je v plánu umožnit ===
funkce(s, argumenty)
{
	// ...
	return 123;
}
