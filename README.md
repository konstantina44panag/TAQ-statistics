#In Unix the datafiles undergo decompression, conversion to csv format, separation of stock-files and compression.*
*Taqdata_csv_stock_files.sh
#Also headers are added in unix:
head -n 2 temp.csv > header.txt
cat header.txt MSFT_complete_nbbo_20090302.csv > quotes_data.csv
head -n 2 temp.csv > header.txt
cat header.txt MSFT_ctm_20090302.csv > trades_data.csv

#By running variables.py, the datasets undergo some preparation operations* and the following are executed: the trade sign algorithm**, the creation of bar variables***, and the computation of variables****.
#*preparation.py
#**sign_algorithms.py where I implement the code by Jukartis (2022): https://github.com/jktis/  
#***bar_analysis.py
#****variables.py
