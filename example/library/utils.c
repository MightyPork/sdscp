#pragma renderer sds2
#pragma once

#include "sys.c"

// absolute value
#define _abs(x) ((x) * (1 - (2 * ((x) < 0))))

// random in range (from, to) including "from"
#define _rand(from, to) ((from) + (_RANDOM % ((to) - (from))))

// signum
#define _sgn(x) (((x) > 0) * 1 + ((x) < 0) * (-1))


// improved ATOI that returns the result
// end mark is stored in _ATOI_END.
var _ATOI_END;
_atoi(t)
{
	atoi(text[t]);

	_ATOI_END = -1;
	for(; t < TEXT_END; t++) {
		if(text[t] == 0) {
			_ATOI_END = t;
			break;
		}
	}

	if(_ATOI_END == -1)
		_ATOI_END = TEXT_END;

	return _ATOI_RESULT;
}


// print a number, return index
_sprintf_n(text_index, number)
{
	sprintf(text[text_index], number);
	return _SPRINTF_END;
}
