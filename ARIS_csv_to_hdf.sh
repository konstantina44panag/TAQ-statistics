#((myenv) [kpanag@login02 scripts]$ cat csv_to_hdf.sh) :
#!/bin/bash
set -eu


SAS_FILES=("/work/pa24/kpanag/taq_msec2023/m202301/ctm_20230103.sas7bdat.bz2")

export PATH=$PATH:/users/pa24/kpanag/.local/bin

if [ -z "${LD_LIBRARY_PATH+x}" ]; then
    export LD_LIBRARY_PATH=/users/pa24/kpanag/local/lib
else
    export LD_LIBRARY_PATH=/users/pa24/kpanag/local/lib:$LD_LIBRARY_PATH
fi

hdf5_file="/work/pa24/kpanag/200903.h5"

SAS_FILE=${SAS_FILES[0]}
GROUP_NAME=$(basename $SAS_FILE .sas7bdat.bz2)
BASE_NAME=${SAS_FILE%.bz2}

bzip2 -dk $SAS_FILE
readstat ${BASE_NAME} - | python3 /work/pa24/kpanag/scripts/hdf.py $hdf5_file $GROUP_NAME

echo "File $SAS_FILE has been processed and appended to $hdf5_file."
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#((myenv) [kpanag@login02 scripts]$ cat hdf.py ):
#!/usr/bin/env python3
import pandas as pd
import argparse
import sys

def append_data_to_hdf5(hdf5_path, group_name, csv_input, chunksize=1000000):
    reader = pd.read_csv(csv_input, chunksize=chunksize, low_memory=False)

    with pd.HDFStore(hdf5_path, mode='a', complevel=9, complib='zlib') as store:
        for chunk in reader:
            chunk['SYM_SUFFIX'] = chunk['SYM_SUFFIX'].astype(str)
            chunk['TR_STOP_IND'] = chunk['TR_STOP_IND'].astype(str)
            for unique_key, group_df in chunk.groupby(chunk.columns[3]):
                hdf5_key = f'{group_name}/{unique_key.replace("/", "_").replace(" ", "_").replace("-", "_")}'
                min_itemsize = {
                    col: 50 for col in group_df.columns
                }
                store.append(hdf5_key, group_df, format='table', data_columns=True, index=False, min_itemsize=min_itemsize)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Append CSV data to an HDF5 file, organized by unique values in the fourth column.")
    parser.add_argument("hdf5_path", help="Path to the HDF5 file.")
    parser.add_argument("group_name", help="Name of the group under which data should be stored.")
    parser.add_argument("csv_path", nargs='?', default=sys.stdin, help="Path to the input CSV file or '-' for stdin.")
    args = parser.parse_args()

    if args.csv_path is sys.stdin or args.csv_path == '-':
        if sys.stdin.isatty():
            print("Error: No data piped to script and no CSV file path provided.", file=sys.stderr)
            sys.exit(1)
        else:
            append_data_to_hdf5(args.hdf5_path, args.group_name, sys.stdin)
    else:
        append_data_to_hdf5(args.hdf5_path, args.group_name, args.csv_path)


        
