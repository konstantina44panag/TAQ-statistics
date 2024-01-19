#scp panagopkonst@memos1.troias.offices.aueb.gr:/taq93-23/taq_msec2009/m200903/complete_nbbo_20090302.sas7bdat.* .    1043mb
#scp panagopkonst@memos1.troias.offices.aueb.gr:/taq93-23/taq_msec2009/m200903/ctm_20090302.sas7bdat.* .               458mb           
#scp panagopkonst@memos1.troias.offices.aueb.gr:/taq93-23/taq_msec2009/m200903/mastm_20090302.sas7bdat.* .             343kb

#FOR COMPLETE_NBBO
time(
gzip -dc complete_nbbo_20090302.sas7bdat.gz > temp.sas7bdat
sas7bdat_to_csv temp.sas7bdat | grep -v "Successfully converted" > temp.csv
awk -F',' '{ print $0 >> $3 "_complete_nbbo_20090302.csv" }' temp.csv
for file in *_complete_nbbo_20090302.csv; do
    gzip "$file"
done
) 2>&1 | tee cpu_time1.txt
grep "user\|sys" cpu_time1.txt

#real    53m43.532s
#user    51m13.504s
#sys     1m6.117s
#cpu hours: 52m19.621s
#52m19.621s = 3139.621s
#Approximation for total hours needed:
total_size=$(ssh panagopkonst@memos1.troias.offices.aueb.gr 'find ../../taq93-23/taq_msec*/m* -type f -name "complete_nbbo*" -exec du -b {} +' | awk '{ sum += $1 } END { print sum }')
total_size_mb=$(echo "$total_size / (1024 * 1024)" | bc)
result=$(echo "$total_size_mb * 3139.621 / 1043" | bc)
hours=$(echo "$result / 3600" | bc)
echo $hours    #4415 hours


#FOR CTM
time(
gzip -dc ctm_20090302.sas7bdat.gz > temp.sas7bdat
sas7bdat_to_csv temp.sas7bdat | grep -v "Successfully converted" > temp.csv
awk -F',' '{ print $0 >> $4 "_ctm_20090302.csv" }' temp.csv
for file in *_ctm_20090302.csv; do
    gzip "$file"
done
) 2>&1 | tee cpu_time2.txt
grep "user\|sys" cpu_time2.txt

#real    18m20.806s
#user    17m44.405s
#sys     0m21.103s
#cpu hours: 18m5.508s
#18m5.508s = 1085.508
#Approximation for total hours needed:
total_size=$(ssh panagopkonst@memos1.troias.offices.aueb.gr 'find ../../taq93-23/taq_msec*/m* -type f -name "ctm*" -exec du -b {} +' | awk '{ sum += $1 } END { print sum }')
total_size_mb=$(echo "$total_size / (1024 * 1024)" | bc)
result=$(echo "$total_size_mb * 1085.508 / 458" | bc)
hours=$(echo "$result / 3600" | bc)
echo $hours  #2122 hours

#FOR MASTM
time(
gzip -dc mastm_20090302.sas7bdat.gz > temp.sas7bdat
sas7bdat_to_csv temp.sas7bdat | grep -v "Successfully converted" > temp.csv
awk -F',' '{ print $0 >> $2 "_mastm_20090302.csv" }' temp.csv
for file in *_mastm_20090302.csv; do
    gzip "$file"
done
)2>&1 | tee cpu_time3.txt
grep "user\|sys" cpu_time3.txt
#real    0m21.568s
#user    0m12.578s
#sys     0m4.826s
#cpu hours: 0m17.404s
#Approximation for total hours needed:
total_size=$(ssh panagopkonst@memos1.troias.offices.aueb.gr 'find ../../taq93-23/taq_msec*/m* -type f -name "mastm*" -exec du -b {} +' | awk '{ sum += $1 } END { print sum }')
total_size_mb=$(echo "$total_size / (1024 * 1024)" | bc)
result=$(echo "$total_size_mb * 17.404 / 0.33 " | bc)
hours=$(echo "$result / 3600" | bc -l)
echo $hours      #18


#scp panagopkonst@memos1.troias.offices.aueb.gr:/taq93-23/taq2005taq05ad/cq_20050301.sas7bdat.* .              371mb
#scp panagopkonst@memos1.troias.offices.aueb.gr:/taq93-23/taq2005taq05ad/div_200503.sas7bdat.* .               28kb
#scp panagopkonst@memos1.troias.offices.aueb.gr:/taq93-23/taq2005taq05ad/mast_200503.sas7bdat.* .              219kb

#FOR CQ
time(
gzip -dc cq_20050301.sas7bdat.gz > temp.sas7bdat
sas7bdat_to_csv temp.sas7bdat | grep -v "Successfully converted" > temp.csv
awk -F',' '{ print $0 >> $1 "_cq_20050301.csv" }' temp.csv
for file in *_cq_20050301.csv; do
    gzip "$file"
done 
)2>&1 | tee cpu_time4.txt
grep "user\|sys" cpu_time4.txt

#real    19m52.157s
#user    19m20.567s
#sys     0m29.745s
#cpu hours: 19m50.312s
#1190.312s
#Approximation for total hours needed:
total_size=$(ssh panagopkonst@memos1.troias.offices.aueb.gr 'find ../../taq93-23/taq* -type f -name "cq*" -exec du -b {} +' | awk '{ sum += $1 } END { print sum }')
total_size_mb=$(echo "$total_size / (1024 * 1024)" | bc)
result=$(echo "$total_size_mb * 1190.312 / 371 " | bc)
hours=$(echo "$result / 3600" | bc -l)
echo $hours    #377.1725

#FOR DIV
time(
gzip -dc div_200503.sas7bdat.gz > temp.sas7bdat
sas7bdat_to_csv temp.sas7bdat | grep -v "Successfully converted" > temp.csv
awk -F',' '{ print $0 >> $1 "_div_200503.csv" }' temp.csv
for file in *_div_200503.csv; do
    gzip "$file"
done
)2>&1 | tee cpu_time5.txt
print_memory_usage
grep "user\|sys" cpu_time5.txt

#real    0m2.298s
#user    0m1.418s
#sys     0m1.110s
#cpu hours: 2.528s
#Approximation for total hours needed:
total_size=$(ssh panagopkonst@memos1.troias.offices.aueb.gr 'find ../../taq93-23/taq* -type f -name "div*" -exec du -b {} +' | awk '{ sum += $1 } END { print sum }')
total_size_mb=$(echo "$total_size / (1024 * 1024)" | bc)
result=$(echo "$total_size_mb * 2.528 / 0.0273 " | bc)
echo $result    #277sec

#FOR MAST
time(
gzip -dc mast_200503.sas7bdat.gz > temp.sas7bdat
sas7bdat_to_csv temp.sas7bdat | grep -v "Successfully converted" > temp.csv
awk -F',' '{ print $0 >> $1 "_mast_200503.csv" }' temp.csv
for file in *_mast_200503.csv; do
    gzip "$file"
done
)2>&1 | tee cpu_time6.txt
grep "user\|sys" cpu_time6.txt

#real    0m11.326s
#user    0m8.237s
#sys     0m3.568s
#cpu hours: 11.805s
#Approximation for total hours needed:
total_size=$(ssh panagopkonst@memos1.troias.offices.aueb.gr 'find ../../taq93-23/taq* -type f -name "mast_*" -exec du -b {} +' | awk '{ sum += $1 } END { print sum }')
total_size_mb=$(echo "$total_size / (1024 * 1024)" | bc)
result=$(echo "$total_size_mb * 11.805 / 0.2139 " | bc)
echo $result    #2373sec

#TOTAL CPU HOURS: 7000 
#TOTAL CPU HOURS PER CORE: 28000
