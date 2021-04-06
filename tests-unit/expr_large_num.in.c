main() {
	/// Echo with negative
	echo(-1);
	/// Call with negative
	foo(-1);
	/// Assign negative
	var x = -1;
	/// Simplified expr resulting in negative
	var a = 1 - 5;
	/// becames too large for signed int
	var b = 2147483647 + 1;
	/// Invert operator producing hex
	var h500 = 0x500;
	var c = h500 & ~0xFF;
	
	var max = 4294967295; // 0xffffffff
	var max_hex = 0xffffffff;
	var min = -2147483648;
	var too_big_for_dec = 2147483649;
}

foo(x) {}
