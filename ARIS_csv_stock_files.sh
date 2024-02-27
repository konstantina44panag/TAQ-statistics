#(cat csv_stock_files.slurm ):
#!/bin/bash -l

####################################
#     SLURM Job Submission Script  #
#                                  #
# Submit script: sbatch submit_job_new.slurm #
#                                  #
####################################

#SBATCH --job-name=process_new_sas_file    # Job name
#SBATCH --output=process_new_sas_file.%j.out # Stdout (%j expands to jobId)
#SBATCH --error=process_new_sas_file.%j.err # Stderr (%j expands to jobId)
#SBATCH --ntasks=1                    # Number of tasks(processes)
#SBATCH --nodes=1                     # Number of nodes requested
#SBATCH --ntasks-per-node=1           # Tasks per node
#SBATCH --cpus-per-task=1             # Threads per task
#SBATCH --time=01:00:00               # Walltime
#SBATCH --mem=6G                      # Memory per NODE
#SBATCH --partition=compute           # Partition
#SBATCH --account=pa240201            # Replace with your system project

# Set up the environment
if [ -z "${SLURM_CPUS_PER_TASK+x}" ]; then
    export OMP_NUM_THREADS=1
else
    export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
fi

# Execute the task script
srun bash /work/pa24/kpanag/scripts/csv_stock_files.sh

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


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

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
First I requested 3 GB memory , I got the error of inadequate memory,
The second time I requested 6 GB memory, and again not adequate!


cat process_new_sas_file.1594750.err
slurmstepd: error: Step 1594750.0 exceeded memory limit (6776728 > 6291456), being killed
slurmstepd: error: Exceeded job memory limit
srun: Job step aborted: Waiting up to 32 seconds for job step to finish.
slurmstepd: error: *** STEP 1594750.0 ON node008 CANCELLED AT 2024-02-27T11:22:33 ***
srun: error: node008: task 0: Killed
srun: Terminating job step 1594750.0
slurmstepd: error: Exceeded job memory limit

[kpanag@login02 kpanag]$ cat process_new_sas_file.1594665.err
slurmstepd: error: Step 1594665.0 exceeded memory limit (4442388 > 3145728), being killed
slurmstepd: error: Exceeded job memory limit
srun: Job step aborted: Waiting up to 32 seconds for job step to finish.
slurmstepd: error: *** STEP 1594665.0 ON node015 CANCELLED AT 2024-02-27T10:53:29 ***
srun: error: node015: task 0: Killed
srun: Terminating job step 1594665.0
