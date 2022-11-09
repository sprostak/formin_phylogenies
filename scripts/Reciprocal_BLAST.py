# Goal is to get a reciprocal BLAST program to run on the command line with local databases
# Import Biopython and the command line BLAST module for biopython
# Import regex module

import Bio
from Bio.Blast.Applications import NcbiblastpCommandline
import re 

################################################################################
# define your fwd and rev queries, databases, and results files

query_f = "/Users/fritzlaylinlab/Documents/Prostak/local_blast/Model_actin_reg_seqs.txt"
db_f =  "/Users/fritzlaylinlab/Documents/blastdb/Ustilago_maydis/U_maydis_protdb"
results_f = "/Users/fritzlaylinlab/Documents/Prostak/local_blast/Fungal_Homologs_Actin/model_to_Umaydis_fresults.txt"


query_r_accs = "/Users/fritzlaylinlab/Documents/Prostak/local_blast/Fungal_Homologs_Actin/model_to_Umaydis_raccs.txt"
query_r_seqs = "/Users/fritzlaylinlab/Documents/Prostak/local_blast/Fungal_Homologs_Actin/model_to_Umaydis_rseqs.txt"
db_r =  "/Users/fritzlaylinlab/documents/blastdb/Model_orgs/Model_orgs_protdb"
results_r = "/Users/fritzlaylinlab/Documents/Prostak/local_blast/Fungal_Homologs_Actin/model_to_Umaydis_rresults.txt"

################################################################################


# set up the commands to run forward blastp through python, using the blastp_cline object
fblastp_cline = NcbiblastpCommandline(seg = "yes", query= query_f, db= db_f, evalue=0.001, word_size=3, 
										outfmt=6, out= results_f)
fblastp_cline 

fblastp_cline()  # run the forward blastp
print("Forward BLAST done!")

# open the forward query and forward results files for reading and reverse query file for writing
query_f_file = open(query_f)
results_f_file = open(results_f)
query_r_accs_file = open(query_r_accs, "w")


# create empty dict for rev query accs
accs_dict ={}

# create a loop that will gather the results that have an e-value of 0.0 or <0.05, gathering their acc#s and their matched forward queries 
results_f_list = list(results_f_file)  # make the forward results file into a list

for result in results_f_list:
	result_line = result.rstrip('\n').split('	')  # for each element this creates a new list where the elements are now the values that populated each column for each line of results
	if int(float(result_line[-2])) == 0.0:
		if str(result_line[1]) not in accs_dict.keys(): # will only add the acc if its not already in the dictionary, reducing repeats, values=0 because the values don't matter in this case
			accs_dict[result_line[1]] = 0
	elif int(float(result_line[-2])) <= 0.05:
		if str(result_line[1]) not in accs_dict.keys():
			accs_dict[result_line[1]] = 0

# write the accs from the dictionary into the accs file
for k in accs_dict.keys():
	query_r_accs_file.write(k + "\n")


print("Reverse query accs gathered!")

# close the forward results file and the reverse query file so they can be reopened later for reading
results_f_file.close()
query_r_accs_file.close()

# gather the sequences for the reverse queries from the local db
# import the seq record modules for gathering the sequences for the a
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

################################################################################
# define the protein sequence file from which you are gathering the sequences and the format the seqs are in

protein_file =  "/Users/fritzlaylinlab/documents/blastdb/Ustilago_maydis/Ustilago_maydis_protein.faa"
prot_file_format = 'fasta'

################################################################################

query_r_accs_file = open(query_r_accs).readlines()
results_file = open(query_r_seqs, 'w') 


protein_list = list(SeqIO.parse(protein_file, prot_file_format))
# create the nested loop for finding the Acc#s matching seq
for protein in protein_list:
	for acc in query_r_accs_file:
		if acc.rstrip('\n') == protein.id:
			results_file.write('>'+ protein.id + '\n')
			results_file.write(str(protein.seq) + '\n')


print('Reverse query seqs gathered!')

# set up the command to run reverse blastp through python, using the blastp_cline object
rblastp_cline = NcbiblastpCommandline(seg = "yes", query= query_r_seqs, db= db_r, evalue=0.001, word_size=3, 
										outfmt=6, out= results_r)
rblastp_cline 

rblastp_cline()  # run the reverse blastp
print("Reverse BLAST done!")

# now that there are forward and reverse results, we need to find out if the top hits match

################################################################################
# open a MBBH results file for writing in to

MBBH_file = open('/Users/fritzlaylinlab/Documents/Prostak/local_blast/Fungal_Homologs_Actin/model_to_Umaydis_MBBH.txt', 'w')

################################################################################

# open the forward and reserve results files to read through
results_f_file = open(results_f)
results_r_file = open(results_r)

# create empty dictionaries for the forward and reverse results, as well as for the query Id and Types
df = {}
dr = {}
type_dict = {}

# gather top hits for each query in the fwd results into the df dictionary
for line in results_f_file:
	elements = re.split("\t|__", line)
	query_ID = elements[0]
	query_type = elements[1]
	subject_ID = elements[2]
	if query_ID not in df.keys():
		df[query_ID] = subject_ID  # this will pick the first hit
		type_dict[query_ID] = query_type


# gather top hits for each query in the rev results into the dr dictionary
for line in results_r_file:
	elements = re.split("\t", line)
	query_ID = elements[0]
	subject_ID = elements[1]
	if query_ID not in dr.keys():
		dr[query_ID] = subject_ID # this will pick the first hit

# close the fwd and rev results files 
results_f_file.close()
results_r_file.close()

# create the empty MBBH dictionary
MBBH = {}
for IDf in df.keys():
	valuef = df[IDf]
	if valuef in dr.keys():
		if IDf == dr[valuef]: # this indicates that if there is a MBBH, the match will be added to the MBBH dictionary
			MBBH[valuef] = IDf

print("MBBH dict complete!")
print(MBHH)