#define RELAY[n] sys[230 + (n)]

var a = sys[12 + 3];
var b;

init() {
	b = sys[12 + ram[57 + 2]] + ram[12 + a];

	a = b + RELAY[3] + RELAY[RELAY[6] + 1];
}

main() {
	echo("Sup");
}

headed() {
	b = sys[12 + ram[57 + 2]] + ram[12 + a];
	a = b + RELAY[3] + RELAY[RELAY[6] + 1];
	a = RELAY[3];
	RELAY[a+2] = b;
}
