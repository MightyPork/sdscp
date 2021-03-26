#define canny_http_get(route, args...)	http_get(ip1, ip2, ip3, ip4, "localhost",		\
											route "?id=", ID, ## args					\  // "&aaa=", aaa, "&bbb=", bbb ...
										);												\

										wait_for_http_get();							\

										if ( HTTP_GET_OK() ) {							\

											echo("GET success: ", HTTP_GET_RESULT());	\

										} else {										\

											echo("GET error: ", HTTP_GET_RESULT() );	\

										}

main() {
	var ip1 = 192;
	var ip2 = 168;
	var ip3 = 0;
	var ip4 = 10;
	canny_http_get("HELLO", "&such=", "route", "&much=", "awesome");
}
