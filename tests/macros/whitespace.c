
#define canny_http_get(route, args...)	load_ip(); 										\ // store IP in the IP variables
										http_get(ip1, ip2, ip3, ip4, "localhost",		\
											route "?id=", ID, ## args					\  // "&aaa=", aaa, "&bbb=", bbb ...
										);												\
										wait_for_http_get();							\
										if ( HTTP_GET_OK() ) {							\
											echo("GET success: ", HTTP_GET_RESULT());	\
										} else {										\
											echo("GET error: ", HTTP_GET_RESULT() );	\
										}


canny_http_get("YO_DAWG", "&such=", "route", "&much=", "awesome");
