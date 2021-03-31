main() {
	var a = 15;
	echo("a");
	/// First free block
	{
		var b = 15;
		echo(b + 1);
		
		/// -- Nested free block 1
		{
			var x = 15;
			echo(x);
		}
		/// -- end block
	}
	/// end block
	/// Second free block
	{
		var b = 15;
		echo(b + 1);
		
		/// -- Nested free block 2
		{
			var x = 15;
			echo(x);
		}
		/// -- end block
	}
	/// end block
	echo(a);
}
