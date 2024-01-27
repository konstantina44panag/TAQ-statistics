#I estimate statistics for the MSFT TAQ data of 02/03/2009
#Files Download: 
#scp panagopkonst@memos1.troias.offices.aueb.gr:/taq93-23/taq_msec2009/m200903/complete_nbbo_20090302.sas7bdat.* .   
#scp panagopkonst@memos1.troias.offices.aueb.gr:/taq93-23/taq_msec2009/m200903/ctm_20090302.sas7bdat.* .      
#Then the conversion of files to csv follows, and the creation of stock specific files
#MSFT_complete_nbbo_20090302.csv is created, but it has no headers
#MSFT_ctm_20090302.csv is created, but it has no headers


head -n 2 temp.csv > header.txt
cat header.txt MSFT_complete_nbbo_20090302.csv > quotes_data.csv
head -n 2 temp.csv > header.txt
cat header.txt MSFT_ctm_20090302.csv > trades_data.csv

#By running variables.py, the trade sign algorithm, the creation of bar variables, and the computation of variables are executes for the stock files.

#(1 Algorithms for trade signs, I implement the code by Jukartis (2022): https://github.com/jktis/ in sign_algorithms.py)

#(2 Creation of bars in bar_analysis.py)

#(3 Creation of Variables in variables.py)
