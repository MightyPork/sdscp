// This example shows how strings behave within macros

#define INDEX "index.php"

#define MOO "(moo)"

main()
{
	http_get(198, 162, 11, 111, "localhost",
        // the strings are joined, just like in C
        MOO INDEX"?a=", sys[459], "&foo=", "bar");
}
