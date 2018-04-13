#!/usr/bin/env bash

# This adds the header to the output csv
head -1 "$(find . -name '*_exits.csv' | head -1)" > crunchbase_exits.csv

# This appends all csv file data sans header
find . -name '*_exits.csv' -print0 |
    while IFS= read -r -d $'\0' filename; do
        sed 1d "$filename" >> crunchbase_exits.csv
    done

# Rename our vc list of names csv
mv $(find . -name 'investors-*.csv' -print0) investor_list.csv