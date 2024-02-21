#!/bin/bash
set -eu

export PATH=$PATH:/home/konstantina/.local/bin

# Check if LD_LIBRARY_PATH is already set and append to it if so; initialize it if not
if [ -z "${LD_LIBRARY_PATH+x}" ]; then
    export LD_LIBRARY_PATH=/usr/local/lib
else
    export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
fi

hdf5_file="200903.h5"
for sas_file in ctm_20090302.sas7bdat.gz ; do
    group_name="20090302"
    base_name=$(basename $sas_file .gz)

    gzip -dk $sas_file
    readstat ${base_name} - | awk -F',' '{ print $0 >> $4 "_ctm_20090302.csv" }' 
    for file in *_ctm_20090302.csv; do
    gzip "$file"
    done
done


