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


#1 Algorithms for trade signs
#I implement the code by Jukartis (2022): https://github.com/jktis/
python3 setup.py build_ext -i
./sign_algorithms.py


#2 Creation of bars
./bar_analysis.py

#3 Variables
./variables.py
