
hello()
{
	print("Hello ", whom);

	wh_1_continue:
	if(2 + 45^foo / (bar % 2) >> 2)
		goto wh_1_body;
	else
		goto wh_1_break;
	wh_1_body:

		sw_1_test_1:
		if(moo != 3) goto sw_1_test_2;
		sw_1_case_1:

			print("3");

			goto sw_1_case_2;
		sw_1_test_2:
		if(moo != 4) goto sw_1_default;
		sw_1_case_2:
			print("4");
			goto sw_1_break;

		sw_1_default:
			print("Unknown");

			if(aa == bb)
				print("yo");
			else if(sss == ffff+23)
				print("dawg");

		for_1_continue:
		if(1) goto for_1_body; else goto for_1_break;
		for_1_body:

			moo(1+klmn);

		goto for_1_continue;
		for_1_break:

	goto wh_1_continue;
	wh_1_break:
}
