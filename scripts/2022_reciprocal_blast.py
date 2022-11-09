#!usr/bin/env python3

## Taking my old Reciprocal_BLAST.py script and cleaning it up a little
## Import needed modules

import Bio
from Bio.Blast.Applications import NcbiblastpCommandline
import re
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

################################################################################
# define your fwd and rev queries, databases, results files, protein sequence file and format, MBBH file

query_f = 
db_f = 
results_f =


query_r_accs = 
query_r_seqs =
db_r =
results_r =

protein_file =
prot_file_format = 'fasta'

MBBH_file =


################################################################################

# set up the commands to run forward blastp through python, using the blastp_cline object
fblastp_cline = NcbiblastpCommandline(seg = "yes", query= query_f, db= db_f, evalue=0.001, word_size=3, 
										outfmt=6, out= results_f)
fblastp_cline 

fblastp_cline()  # run the forward blastp
print("Forward BLAST done!")
