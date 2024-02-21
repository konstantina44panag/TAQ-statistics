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
    group_name="group_20090302"
    base_name=$(basename $sas_file .gz)
    
    gzip -dk $sas_file
    readstat ${base_name} - | python3 hdf.py $hdf5_file $group_name
done


echo "All files have been processed and appended to $hdf5_file."
