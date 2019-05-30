#!/bin/bash

if [ -n "$1" ]:
then
    head -1 $2 > $1.csv
    for f in *.csv;
    do  echo "seaching for $1 year data"
	sed 1d $f >> $1.csv
	echo "merged $f into $1.csv"
    done
else
    echo "can't find the file"
fi
