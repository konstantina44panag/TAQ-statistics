#I estimate statistics for the MSFT TAQ data of 02/03/2009
#Files Download: 
#scp panagopkonst@memos1.troias.offices.aueb.gr:/taq93-23/taq_msec2009/m200903/complete_nbbo_20090302.sas7bdat.* .   
#scp panagopkonst@memos1.troias.offices.aueb.gr:/taq93-23/taq_msec2009/m200903/ctm_20090302.sas7bdat.* .      
#Then the conversion of files to csv follows, and the creation of stock specific files:     
#FOR COMPLETE_NBBO FILES
gzip -dc complete_nbbo_20090302.sas7bdat.gz > temp.sas7bdat
sas7bdat_to_csv temp.sas7bdat | grep -v "Successfully converted" > temp.csv
awk -F',' '{ filename=$3 "_complete_nbbo_20090302.csv"; $3=""; print $0 >> filename }' temp.csv
for file in *_complete_nbbo_20090302.csv; do
    bzip2 "$file"
done
bzip2 -dk MSFT_complete_nbbo_20090302.csv.bz2
#MSFT_complete_nbbo_20090302.csv is created, but it has no headers
head -n 2 temp.csv > header.txt
cat header.txt MSFT_complete_nbbo_20090302.csv > quotes_data.csv

#FOR CTM FILES
gzip -dc ctm_20090302.sas7bdat.gz > temp.sas7bdat
sas7bdat_to_csv temp.sas7bdat | grep -v "Successfully converted" > temp.csv
awk -F',' '{ filename=$4 "_ctm_20090302.csv"; $4=""; print $0 >> filename }' temp.csv
for file in *_ctm_20090302.csv; do
    bzip2 "$file"
done
bzip2 -dk MSFT_ctm_20090302.csv.bz2
#MSFT_ctm_20090302.csv is created, but it has no headers
head -n 2 temp.csv > header.txt
cat header.txt MSFT_ctm_20090302.csv > trades_data.csv

./variables.py
#By running variables.py, the trade sign algorithm, the creation of bar variables, and the computation of variables are executes for the stock files.
