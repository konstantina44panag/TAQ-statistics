#I estimate statistics for the MSFT TAQ data of 02/03/2009
#Files Download: 
#scp panagopkonst@memos1.troias.offices.aueb.gr:/taq93-23/taq_msec2009/m200903/complete_nbbo_20090302.sas7bdat.* .   
#scp panagopkonst@memos1.troias.offices.aueb.gr:/taq93-23/taq_msec2009/m200903/ctm_20090302.sas7bdat.* .      
#Then the conversion of files to csv follows, and the creation of stock specific files
#MSFT_complete_nbbo_20090302.csv is created, but no headers
#MSFT_ctm_20090302.csv is created, but no headers:

head -n 2 temp.csv > header.txt
cat header.txt MSFT_complete_nbbo_20090302.csv > quotes_data.csv
head -n 2 temp.csv > header.txt
cat header.txt MSFT_ctm_20090302.csv > trades_data.csv

#By running variables.py, the datasets undergo some preparation operations* and the following are executed: the trade sign algorithm**, the creation of bar variables***, and the computation of variables****.
#*preparation.py
#**sign_algorithms.py where I implement the code by Jukartis (2022): https://github.com/jktis/  
#***bar_analysis.py
#****variables.py
