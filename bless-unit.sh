#!/bin/bash

test="$1"
resultfile="out/$test.out.c"
echo "Bless test output: $resultfile"
cp "$resultfile" tests-unit/
