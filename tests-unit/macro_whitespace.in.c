#define canny_http_get(route, args...)	http_get(ip1, ip2, ip3, ip4, "localhost",		\
											route "?id=", ID, ## args					\  // "&aaa=", aaa, "&bbb=", bbb ...
										);												\

										wait_for_http_get();							\

										if ( sys[123]==456 ) {							\ /// doc comment is also stripped

											echo("GET success: ", text[0]);	\

										} else {		/* comment*/ 				\

											echo("GET error: ", text[0] );	\

										}

#define ID 111222

wait_for_http_get() {
	wait(2000);
}

main() {
	var ip1 = 192;
	var ip2 = 168;
	var ip3 = 0;
	var ip4 = 10;
	canny_http_get("HELLO", "&such=", "route", "&much=", "awesome");
}
