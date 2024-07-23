# PARALLEL BLAST
## Description
This guide outlines the process of splitting a large FASTA file into smaller chunks and running BLAST searches on each chunk in parallel using GNU Parallel. 

### Steps:
1. **Install Biopython**: Required for handling FASTA files.

  ```bash
  pip install biopython
  ```
2. **Split the FASTA File**: A Python script (`split_fasta_by_contigs.py`) splits the input FASTA file into smaller files, each containing a specified number of contigs.
Use the following command to split your input FASTA file (input.fasta) into chunks of 30 contigs each (This value is used depending on cpus assigned in slurm)

  ```bash
  python split_fasta_by_contigs.py input.fasta query_chunk 30
  ```

3. **Run BLAST with GNU Parallel**: Execute BLAST searches on the split files concurrently using GNU Parallel, improving efficiency and reducing overall processing time.

  ```bash
  ls query_chunk* | parallel "blastn -query {} -task megablast -db nt -outfmt '6 qseqid staxids bitscore std sscinames sskingdoms stitle' -culling_limit 10 -num_threads 8 -evalue 1e-3 -out {.}.out"
  ```

4. **Merge Results**: Combine the BLAST output from each chunk into a single file for comprehensive analysis.

  ```bash
  cat query_chunk_*.out > combined_results.out
  ```

### SLURM Configuration:
When executing this process on a SLURM cluster, configure the number of threads according to the number of generated chunks to ensure efficient resource use. For example, if the input FASTA file contains 110 contigs and you split it into chunks of 30 contigs each, you will get 4 chunk files. To run each file with 8 threads, set the total CPUs in the SLURM job to 8*4=32.

Explanation:
1. Input FASTA File: 110 contigs
2. Chunk Size: 30 contigs per file
3. Number of Chunks: 4 (as 110 contigs / 30 contigs per file = approximately 4 files)
4. Threads per Chunk: 8
5. Total CPUs in SLURM Job: 8 threads * 4 chunks = 32 CPUs

```slurm
#!/bin/bash -e
#SBATCH --account=acc_id
#SBATCH --job-name=blastn
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=32
#SBATCH --mem=80G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=<email>
#SBATCH --output Blastn_%j.out    # save the output into a file
#SBATCH --error Blastn_%j.err     # save the error output into a file

# purge all other modules that may be loaded, and might interfare
module purge

## load tools
module load BLASTDB/2024-07 BLAST/2.13.0-GCC-11.3.0 Parallel/20220922 Python

##Install biopython
pip install biopython

##Split fasta
python split_fasta_by_contigs.py input.fasta query_chunk 30

##Run nBLAST with GNU Parallel
ls query_chunk* | parallel "blastn -query {} -task megablast -db nt -outfmt '6 qseqid staxids bitscore std sscinames sskingdoms stitle' -culling_limit 10 -num_threads 8 -evalue 1e-3 -out {.}.out"

##Merge
cat query_chunk_*.out > blast_combined_results.out
```
