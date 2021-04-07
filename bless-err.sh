#!/bin/bash

test="$1"
resultfile="out/$test.out.txt"
echo "Bless test error: $resultfile"
cp "$resultfile" tests-err/
