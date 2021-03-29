/// Test the various literal formats

main() {
	echo("String", "String with spaces", "apos' and \"quote", "newline\nescape");
	echo('a', 's', 'c', 'i', 'i');
	echo(0, 1, -1, 2147483647, -2147483647); // XXX -2147483648 is valid, but rejected by SDS-C EXE
	echo(0xF, 0xFF, 0x01234567, 0x89ABCDEF, 0xFFFFFFFF); // this is fine, SDS-C seems to be OK with hex out of i32 range
	echo(0xF, 0xF_F, 0x01_23_45_67_);
	echo(0b0, 0b111000111, 0b1111111111111111111111111111111, 0b11_1_1_1111, 0b1111_1111_);
}
