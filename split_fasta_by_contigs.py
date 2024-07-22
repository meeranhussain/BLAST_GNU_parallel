from Bio import SeqIO
import sys
import os

def split_fasta_by_contigs(input_fasta, output_prefix, contigs_per_file):
    contig_count = 0
    file_count = 1
    output_file = f"{output_prefix}_{file_count}.fasta"
    output_handle = open(output_file, "w")

    for record in SeqIO.parse(input_fasta, "fasta"):
        if contig_count >= contigs_per_file:
            output_handle.close()
            file_count += 1
            output_file = f"{output_prefix}_{file_count}.fasta"
            output_handle = open(output_file, "w")
            contig_count = 0

        SeqIO.write(record, output_handle, "fasta")
        contig_count += 1

    output_handle.close()
    print(f"FASTA file split into {file_count} files.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python split_fasta_by_contigs.py <input_fasta> <output_prefix> <contigs_per_file>")
        sys.exit(1)

    input_fasta = sys.argv[1]
    output_prefix = sys.argv[2]
    contigs_per_file = int(sys.argv[3])

    split_fasta_by_contigs(input_fasta, output_prefix, contigs_per_file)
