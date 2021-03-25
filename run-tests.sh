#!/bin/bash

for filename in unit-tests/*.in.c; do
    ./sdscp -q "$filename" -o "out/test.c"
    
    if [[ $? == 1 ]]; then
		echo -e "\x1b[31mTest \"${filename}\" failed!\x1b[m"
		exit
	fi
    
    outfile=$(echo "${filename}" | sed 's/.in.c/.out.c/')
    if cmp -s "${outfile}" "out/test.c"; then
		echo -e "\x1b[32mTEST \"${filename}\" OK\x1b[m"
	else
		echo -e "\x1b[31mTest \"${filename}\" output differs!\x1b[m"
		diff -u "${outfile}" "out/test.c"
		exit
	fi
done
