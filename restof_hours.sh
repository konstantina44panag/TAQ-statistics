print_memory_usage() {
    pid=$$
    memory_usage=$(ps -p $pid -o rss=)
    echo "Memory usage of the script: ${memory_usage} KB"
}
num_cores=$(nproc)
#scp panagopkonst@memos1.troias.offices.aueb.gr:/taq93-23/taq2005taq05ad/cq_20050301.sas7bdat.* .              371mb
#scp panagopkonst@memos1.troias.offices.aueb.gr:/taq93-23/taq2005taq05ad/div_200503.sas7bdat.* .               28kb
#scp panagopkonst@memos1.troias.offices.aueb.gr:/taq93-23/taq2005taq05ad/mast_200503.sas7bdat.* .              219kb

#FOR CQ
time(
gzip -dc cq_20050301.sas7bdat.gz > temp.sas7bdat
print_memory_usage 
memory_per_core=$((memory_usage / num_cores))
echo "Memory usage per core: ${memory_per_core} KB"
sas7bdat_to_csv temp.sas7bdat | grep -v "Successfully converted" > temp.csv
print_memory_usage
memory_per_core=$((memory_usage / num_cores))
echo "Memory usage per core: ${memory_per_core} KB"
awk -F',' '{ print $0 >> $1 "_cq_20050301.csv" }' temp.csv
print_memory_usage
memory_per_core=$((memory_usage / num_cores))
echo "Memory usage per core: ${memory_per_core} KB"
for file in *_cq_20050301.csv; do
    gzip "$file"
done 
)2>&1 | tee cpu_time4.txt
print_memory_usage
memory_per_core=$((memory_usage / num_cores))
echo "Memory usage per core: ${memory_per_core} KB"
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
print_memory_usage 
memory_per_core=$((memory_usage / num_cores))
echo "Memory usage per core: ${memory_per_core} KB"
sas7bdat_to_csv temp.sas7bdat | grep -v "Successfully converted" > temp.csv
print_memory_usage
memory_per_core=$((memory_usage / num_cores))
echo "Memory usage per core: ${memory_per_core} KB"
awk -F',' '{ print $0 >> $1 "_div_200503.csv" }' temp.csv
print_memory_usage
memory_per_core=$((memory_usage / num_cores))
echo "Memory usage per core: ${memory_per_core} KB"
for file in *_div_200503.csv; do
    gzip "$file"
done
)2>&1 | tee cpu_time5.txt
print_memory_usage
memory_per_core=$((memory_usage / num_cores))
echo "Memory usage per core: ${memory_per_core} KB"
grep "user\|sys" cpu_time5.txt
#real    0m2.298s
#user    0m1.418s
#sys     0m1.110s
#cpu hours: 2.528s
#Approximation for total hours needed:
total_size=$(ssh panagopkonst@memos1.troias.offices.aueb.gr 'find ../../taq93-23/taq* -type f -name "div*" -exec du -b {} +' | awk '{ sum += $1 } END { print sum }')
total_size_mb=$(echo "$total_size / (1024 * 1024)" | bc)
result=$(echo "$total_size_mb * 2.528 / 0.0273 " | bc)
hours=$(echo "$result / 3600" | bc -l)
echo $hours    #0.07694444444444444444

#FOR MAST
time(
gzip -dc mast_200503.sas7bdat.gz > temp.sas7bdat
print_memory_usage 
memory_per_core=$((memory_usage / num_cores))
echo "Memory usage per core: ${memory_per_core} KB"
sas7bdat_to_csv temp.sas7bdat | grep -v "Successfully converted" > temp.csv
print_memory_usage
memory_per_core=$((memory_usage / num_cores))
echo "Memory usage per core: ${memory_per_core} KB"
awk -F',' '{ print $0 >> $1 "_mast_200503.csv" }' temp.csv
print_memory_usage
memory_per_core=$((memory_usage / num_cores))
echo "Memory usage per core: ${memory_per_core} KB"
for file in *_mast_200503.csv; do
    gzip "$file"
done
)2>&1 | tee cpu_time6.txt
memory_per_core=$((memory_usage / num_cores))
echo "Memory usage per core: ${memory_per_core} KB"
grep "user\|sys" cpu_time6.txt

#real    0m11.326s
#user    0m8.237s
#sys     0m3.568s
#cpu hours: 11.805s
#Approximation for total hours needed:
total_size=$(ssh panagopkonst@memos1.troias.offices.aueb.gr 'find ../../taq93-23/taq* -type f -name "mast*" -exec du -b {} +' | awk '{ sum += $1 } END { print sum }')
total_size_mb=$(echo "$total_size / (1024 * 1024)" | bc)
result=$(echo "$total_size_mb * 11.805 / 0.2139 " | bc)
hours=$(echo "$result / 3600" | bc -l)
echo $hours    #18.53416666666666666666
