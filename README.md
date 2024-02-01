# Data-files Processing in Unix

In Unix, the data files undergo several steps:

1. Decompression.
2. Conversion to CSV format.
3. Separation of stock-files.
4. Compression.

### Decompression and Processing Scripts

Use the `Taqdata_csv_stock_files.sh` script for processing. 

#Also headers are added in unix, for example for the files MSFT_complete_nbbo_20090302.csv.gz :
gzip -d MSFT_complete_nbbo_20090302.csv.gz
head -n 2 temp.csv > header.txt
cat header.txt MSFT_complete_nbbo_20090302.csv > quotes_data.csv


# Statistics

Running `variables.py` triggers a sequence of operations and scripts that prepare the datasets, execute algorithms, and compute various variables. Below is a breakdown of these processes:

- **Data Preparation**: This is handled by `preparation.py`, which sets up the datasets for further analysis.

- **Trade Sign Algorithm**: Implemented in `sign_algorithms.py`. This script applies the algorithm developed by Jukartis (2022), available at [Jukartis GitHub Repository](https://github.com/jktis/).

- **Bar Variable Creation**: The script `bar_analysis.py` is responsible for creating bar variables as part of the data analysis process.

- **Variable Computation**: Finally, `variables.py` computes various important variables needed for the project.
