#((myenv) [kpanag@login02 scripts]$ cat csv_stock_files.sh):
#!/bin/bash
set -eu

export PATH=$PATH:/users/pa24/kpanag/.local/bin

# Check if LD_LIBRARY_PATH is already set and append to it if so; initialize it if not
if [ -z "${LD_LIBRARY_PATH+x}" ]; then
    export LD_LIBRARY_PATH=/usr/local/lib
else
    export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
fi

SAS_FILES=("/work/pa24/kpanag/taq_msec2023/m202301/ctm_20230103.sas7bdat.bz2")
SAS_FILE=${SAS_FILES[0]}
BASE_NAME=${SAS_FILE%.bz2}
GROUP_NAME=$(basename $SAS_FILE .sas7bdat.bz2)

NEW_DIR="/work/pa24/kpanag/$GROUP_NAME"
if [ ! -d "$NEW_DIR" ]; then
    mkdir -p "$NEW_DIR"
fi
cd "$NEW_DIR"

# Decompress the file
bzip2 -dk $SAS_FILE

# Process the decompressed SAS file and convert it to CSV
readstat ${BASE_NAME} - | awk -F',' '{ print $0 >> $4 "_'${GROUP_NAME}'.csv" }'

# Compress the CSV files generated
for file in *_"${GROUP_NAME}".csv; do
    gzip "$file"
done
