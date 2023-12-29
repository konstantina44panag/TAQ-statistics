scp panagopkonst@memos1.troias.offices.aueb.gr:/taq93-23/taq_msec2009/m200903/complete_nbbo_20090302.sas7bdat.* .   # 1043mb
scp panagopkonst@memos1.troias.offices.aueb.gr:/taq93-23/taq_msec2009/m200903/ctm_20090302.sas7bdat.* .             # 458mb 
scp panagopkonst@memos1.troias.offices.aueb.gr:/taq93-23/taq_msec2009/m200903/mastm_20090302.sas7bdat.* .           # 343kb
scp panagopkonst@memos1.troias.offices.aueb.gr:/taq93-23/taq2005taq05ad/cq_20050301.sas7bdat.* .             # 371mb
scp panagopkonst@memos1.troias.offices.aueb.gr:/taq93-23/taq2005taq05ad/div_200503.sas7bdat.* .              # 28kb
scp panagopkonst@memos1.troias.offices.aueb.gr:/taq93-23/taq2005taq05ad/mast_200503.sas7bdat.* .             # 219kb

#FOR COMPLETE_NBBO
scp panagopkonst@memos1.troias.offices.aueb.gr:/taq93-23/taq_msec2009/m200903/complete_nbbo_20090302.sas7bdat.* . 
time(
gzip -dc complete_nbbo_20090302.sas7bdat.gz > temp.sas7bdat
sas7bdat_to_csv temp.sas7bdat | grep -v "Successfully converted" > temp.csv
awk -F',' '{ filename=$3 "_complete_nbbo_20090302.csv"; $3=""; print $0 >> filename }' temp.csv
for file in *_complete_nbbo_20090302.csv; do
    bzip2 "$file"
done
) 2>&1 | tee cpu_time1.txt
grep "user\|sys" cpu_time1.txt
#real    59m38.762s
#user    57m4.708s
#sys     1m22.926s
#cpu seconds:3507.634

#Approximation for total hours needed:
total_size=$(ssh panagopkonst@memos1.troias.offices.aueb.gr 'find ../../taq93-23/taq_msec*/m* -type f -name "complete_nbbo*" -exec du -b {} +' | awk '{ sum += $1 } END { print sum }')
total_size_mb=$(echo "$total_size / (1024 * 1024)" | bc)
result=$(echo "$total_size_mb * 3507.634/ 1043" | bc)
hours=$(echo "$result / 3600" | bc)
echo $hours    #4933 hours

#FOR CTM
time(
gzip -dc ctm_20090302.sas7bdat.gz > temp.sas7bdat
sas7bdat_to_csv temp.sas7bdat | grep -v "Successfully converted" > temp.csv
awk -F',' '{ filename=$4 "_ctm_20090302.csv"; $4=""; print $0 >> filename }' temp.csv
for file in *_ctm_20090302.csv; do
    bzip2 "$file"
done
) 2>&1 | tee cpu_time2.txt
grep "user\|sys" cpu_time2.txt

#real    22m13.480s
#user    21m25.892s
#sys     0m46.040s
#cpu hours in seconds: 1331.932

find . -type f -regex '.*[^/]ctm.*' -exec du -b {} + | awk '{ sum += $1 } END { print sum }'
#ouput files size: 319764098

#Approximation for total hours needed:
total_size=$(ssh panagopkonst@memos1.troias.offices.aueb.gr 'find ../../taq93-23/taq_msec*/m* -type f -name "ctm*" -exec du -b {} +' | awk '{ sum += $1 } END { print sum }')
total_size_mb=$(echo "$total_size / (1024 * 1024)" | bc)
result=$(echo "$total_size_mb * 1331.932 / 458" | bc)
hours=$(echo "$result / 3600" | bc)
echo $hours  #2603


#FOR MASTM
time(
gzip -dc mastm_20090302.sas7bdat.gz > temp.sas7bdat
sas7bdat_to_csv temp.sas7bdat | grep -v "Successfully converted" > temp.csv
awk -F',' '{ filename=$2 "_mastm_20090302.csv"; $2=""; print $0 >> filename }' temp.csv
for file in *_mastm_20090302.csv; do
    bzip2 "$file"
done
)2>&1 | tee cpu_time3.txt
grep "user\|sys" cpu_time3.txt
#real    0m15.591s
#user    0m12.211s
#sys     0m3.987s
#cpu hours in seconds: 16.198
#Approximation for total hours needed:
total_size=$(ssh panagopkonst@memos1.troias.offices.aueb.gr 'find ../../taq93-23/taq_msec*/m* -type f -name "mastm*" -exec du -b {} +' | awk '{ sum += $1 } END { print sum }')
total_size_mb=$(echo "$total_size / (1024 * 1024)" | bc)
result=$(echo "$total_size_mb * 16.198 / 0.33 " | bc)
hours=$(echo "$result / 3600" | bc -l)
echo $hours      #15.88416666666666666666
 
#FOR CQ
time(
gzip -dc cq_20050301.sas7bdat.gz > temp.sas7bdat
sas7bdat_to_csv temp.sas7bdat | grep -v "Successfully converted" > temp.csv
awk -F',' '{ filename=$1 "_cq_20050301.csv"; $1=""; print $0 >> filename }' temp.csv
for file in *_cq_20050301.csv; do
    bzip2 "$file"
done 
)2>&1 | tee cpu_time4.txt
grep "user\|sys" cpu_time4.txt
#real    21m42.396s
#user    21m12.953s
#sys     0m26.023s
#cpu hours in seconds:1298.976
#Approximation for total hours needed:
total_size=$(ssh panagopkonst@memos1.troias.offices.aueb.gr 'find ../../taq93-23/taq* -type f -name "cq*" -exec du -b {} +' | awk '{ sum += $1 } END { print sum }')
total_size_mb=$(echo "$total_size / (1024 * 1024)" | bc)
result=$(echo "$total_size_mb * 1298.976 / 371 " | bc)
hours=$(echo "$result / 3600" | bc -l)
echo $hours    #411.60472222222222222222


#FOR DIV
time(
gzip -dc div_200503.sas7bdat.gz > temp.sas7bdat
sas7bdat_to_csv temp.sas7bdat | grep -v "Successfully converted" > temp.csv
awk -F',' '{ filename=$1 "_div_200503.csv"; $1=""; print $0 >> filename }' temp.csv
for file in *_div_200503.csv; do
    bzip2 "$file"
done
)2>&1 | tee cpu_time5.txt
grep "user\|sys" cpu_time5.txt
#real    0m2.201s
#user    0m1.365s
#sys     0m1.048s
#cpu hours in seconds:2.413
#Approximation for total hours needed:
total_size=$(ssh panagopkonst@memos1.troias.offices.aueb.gr 'find ../../taq93-23/taq* -type f -name "div*" -exec du -b {} +' | awk '{ sum += $1 } END { print sum }')
total_size_mb=$(echo "$total_size / (1024 * 1024)" | bc)
result=$(echo "$total_size_mb * 2.413 / 0.0273 " | bc)
hours=$(echo "$result / 3600" | bc -l)
echo $hours    #0.07361111111111111111

#FOR MAST
time(
gzip -dc mast_200503.sas7bdat.gz > temp.sas7bdat
sas7bdat_to_csv temp.sas7bdat | grep -v "Successfully converted" > temp.csv
awk -F',' '{ filename=$1 "_mast_200503.csv"; $1=""; print $0 >> filename }' temp.csv
for file in *_mast_200503.csv; do
    bzip2 "$file"
done
)2>&1 | tee cpu_time6.txt
grep "user\|sys" cpu_time6.txt
#real    0m9.406s
#user    0m7.363s
#sys     0m2.391s
#cpu hours in seconds:9.754
#Approximation for total hours needed:
total_size=$(ssh panagopkonst@memos1.troias.offices.aueb.gr 'find ../../taq93-23/taq* -type f -name "mast_*" -exec du -b {} +' | awk '{ sum += $1 } END { print sum }')
total_size_mb=$(echo "$total_size / (1024 * 1024)" | bc)
result=$(echo "$total_size_mb * 9.754 / 0.2139 " | bc)
hours=$(echo "$result / 3600" | bc -l)
echo $hours    #0.5444444444444444

#TOTAL CPU HOURS: 8000 
#TOTAL CPU HOURS PER CORE: 32000
#TOTAL OUTPUT SPACE: