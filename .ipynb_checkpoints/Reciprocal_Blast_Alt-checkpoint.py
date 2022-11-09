import os
import Bio
from Bio.Blast.Applications import NcbiblastpCommandline
from Bio.Blast import NCBIXML


# define the files for the forward and reverse blast searches 
query_f = "/Users/fritzlaylinlab/Documents/Prostak/Python_Scripts/bdjam_formin_results1.txt"
db_f = "~/documents/blastdb/Bd_JEL_Seqs/ncbi_dataset/data/GCA_000149865_1/Bdjel_protdb"
results_f = "Bd_forward_results_test.xml"

query_r = "Bd_query_reverse.txt"
db_r = "~/Documents/blastdb/Bd_JAM_RefSeq/ncbi_dataset/data/GCF_000203795_1/Bdjam_refseq_prots"
results_r = "Bd_reverse_results_test.xml"

# define the blastp command and the parameters you want to run for forward and reverse
blastp_cmdf = "blastp\
		-query " + query_f + "\
	 	-db " + db_f + "\
	 	-out " + results_f + "\
	 	-outfmt 5"   # 5 outputs to .xml format

blastp_cmdr = "blastp\
		-query " + query_r + "\
	 	-db " + db_r + "\
	 	-out " + results_r + "\
	 	-outfmt 5"
	 	
# have the system run the forward command with the parameters you defined above
os.system(blastp_cmdf)
print("Forward Done")


# open the forward query and forward results files for reading and reverse query file for writing
f_query_file = open(query_f)
results_f_file = open(results_f)
r_query_file = open(query_r, "w")

# use the BLAST parser to parse the forward results file
blast_records = NCBIXML.parse(results_f_file)


# create a loop to gather the all the results with an e-value < 0.05
e_value_thresh = 0.05
for record in blast_records:
	if record.expect < e_value_thresh:
		query_r.write(record.title, record.sbjct)
	
print("Reverse querires gathered")