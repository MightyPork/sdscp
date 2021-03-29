main () {
#if 0
	echo("BAD1");
#endif
	#if 0
		echo("BAD2");
	#endif
	
#if 1
	echo("GOOD1");
#endif
	#if 1
		echo("GOOD2");
	#endif

#if 0
	echo("BAD3");
#else
	echo("GOOD3");
#endif
}
