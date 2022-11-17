#!/usr/bin/env python3

## Script to take a .faa from JGI and make it NCBI/BLAST readable

import sys

in_file = '/Users/laboratory/Documents/Fritz_Laylin_Lab/formins/files/protein_sets/Mortierella_elongata_AG-77/Morel2_GeneCatalog_proteins_20151120.aa.fasta'

#in_file = sys.argv[1]
#out_file = sys.argv[2]

with open(in_file, 'r') as file_obj:
    for line in file_obj:
        line = line.rstrip()
        if '>' in line:
            descriptors = line.split('|')
            print(f'>{descriptors[           
