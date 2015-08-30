#pragma once
#pragma renderer sds2
#include "sys.c"

var _http_busy = false;

#define _http_success() ((_HTTP_STATUS == 1024) && (_HTTP_CODE == 200))


// Wait for http_get(), before it can be used again
_wait_for_http()
{
	if(!_http_busy) return; // not busy

	echo("[HTTP] Waiting...");

	while(1) {
		var status = _check_http_progress();
		if(status != -1) return status;
		wait(10);
	}
}


// check progress, to show result in console.
// returns 0..fail, 1..ok, -1..no result yet
_check_http_progress()
{
	if(!_http_busy || _HTTP_STATUS == N_HTTP_BUSY)
		return -1; // not waiting for response, or busy with http

	_http_busy = 0;

	if(_http_success()) {
		echo("[HTTP] OK, code ", _HTTP_CODE);
		return 1;
	} else {
		echo("[HTTP] Error, code ", _HTTP_CODE);
		return 0;
	}
}


// musí být jako makro, kvůli stringovým varargs.
// ip.. ip parts
// bytes.. # of bytes to store
// url.. url parts. Must start with slash.
#define _http_get(ip1, ip2, ip3, ip4, port, bytes, url...) {
	_wait_for_http();
	echo("http_get: ",ip1,".",ip2,".",ip3,".",ip4);
	if(ip1 == 0) {
		echo("INVALID IP!");
	} else {
		echo ("-> ", ## url);

		if(bytes == 0) {
			_HTTP_STORE_MODE = N_HTTP_STORE_NONE;
		} else {
			_HTTP_STORE_MODE = N_HTTP_STORE_TEXT;
			_HTTP_STORE_LENGTH = bytes;
		}
		var __port = port;
		if(__port == 0) __port = 80;
		_HTTP_PORT = __port;

		http_get(ip1, ip2, ip3, ip4, "localhost", ## url);
		_http_busy = 1;
		echo ("[HTTP] Working in background.");
	}
}
