#!/bin/bash

PRAGMAS="
    -p indent 2sp
    -p keep_names true
    -p stack_start 300
    -p stack_end 511
    -p header false
    -p safe_stack false
    -p builtin_logging false
    -p builtin_error_logging false
    -p fullspeed false
    -p comments false
    -p simplify_ifs false
    -p inline_one_use_functions false
    -p push_pop_trampolines false
"

echo "Pragmas:" $PRAGMAS;

echo "Unit tests..."
for filename in tests-unit/*.in.c; do
    resultfile=$(echo "$filename" | sed 's/.in.c/.out.c/' | sed 's/tests-unit/out/')
    expectation=$(echo "$filename" | sed 's/.in.c/.out.c/')

    ./sdscp -q "$filename" -o "$resultfile" $PRAGMAS

    if [[ $? == 1 ]]; then
		echo -e "\x1b[31mTest \"$filename\" failed!\x1b[m"
		exit
	fi

    if cmp -s "$expectation" "$resultfile"; then
		echo -e "\x1b[32mTEST \"$filename\" OK\x1b[m"
	else
		echo -e "\x1b[31mTest \"$filename\" output differs!\x1b[m"
		diff -u "$expectation" "$resultfile"
		exit
	fi
done

echo "Unit tests with default settings..."
# smoke test to see if any of our tests explode with default settings
for filename in tests-unit/*.in.c; do
    ./sdscp -q "$filename" -o /tmp/sdscp-dummy.c

    if [[ $? == 1 ]]; then
		echo -e "\x1b[31mTest \"$filename\" failed!\x1b[m"
		exit
	fi

	echo -e "\x1b[32mTEST \"$filename\" OK\x1b[m"
done

echo "Error tests..."
for filename in tests-error/*.in.c; do
    resultfile=$(echo "$filename" | sed 's/.in.c/.out.c/' | sed 's/tests-error/out/')
    errorfile=$(echo "$filename" | sed 's/.in.c/.out.txt/' | sed 's/tests-error/out/')
    expectation=$(echo "$filename" | sed 's/.in.c/.out.txt/')

    ./sdscp -q "$filename" -o "$resultfile" $PRAGMAS > "$errorfile";

    if [[ $? == 0 ]]; then
		echo -e "\x1b[31mTest \"$filename\" should have failed, but did not!\x1b[m"
		exit
	fi

    if cmp -s "$expectation" "$errorfile"; then
		echo -e "\x1b[32mTEST \"$filename\" failed as expected\x1b[m"
	else
		echo -e "\x1b[31mTEST \"$filename\" failed as expected, but OUTPUT DIFFERS!\x1b[m"
		diff -u "$expectation" "$errorfile"
		exit
	fi
done
