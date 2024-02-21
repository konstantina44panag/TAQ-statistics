#!/usr/bin/env python3
import pandas as pd
import argparse
import sys

def append_data_to_hdf5(hdf5_path, group_name, csv_input, chunksize=1000000):
    reader = pd.read_csv(csv_input, chunksize=chunksize, low_memory=False) 

    with pd.HDFStore(hdf5_path, mode='a', complevel=9, complib='zlib') as store:
        for chunk in reader:
            chunk['SYM_SUFFIX'] = chunk['SYM_SUFFIX'].astype(str)
            for unique_key, group_df in chunk.groupby(chunk.columns[3]):
                hdf5_key = f'{group_name}/{unique_key.replace("/", "_").replace(" ", "_").replace("-", "_")}'
                min_itemsize = {
                    'TR_SCOND': 50,  
                    'TR_STOPIND': 50 
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
