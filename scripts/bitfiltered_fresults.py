# Goal is to write a program that will pull all fwd hits with a bit score >100 into a new file 
#import regex module

import re

#########################BEGIN USER INPUT#######################################

# define the fwd BLAST results file and open the filtered bit score file for writing
fwd_results = "/Users/fritzlaylinlab/Documents/Prostak/local_blast/Fungal_Homologs_Actin/model_to_Sjaponicus/model_to_Sjaponicus_fresults.txt"
filtered_file = open("/Users/fritzlaylinlab/Documents/Prostak/local_blast/Fungal_Homologs_Actin/model_to_Sjaponicus/model_to_Sjaponicus_fresults_bitfiltered.txt", "w")
#########################END USER INPUT########################################

# open the forward results file to read through
fwd_results_file = open(fwd_results)

# write the column headers in the new mbbh file
filtered_file.write("subjectID	queryID	%ID	length	mismatch	gap_open	query_start	query_end	sub_start	sub_end	bit_score" + "\n")
# close the file then open it for appending
filtered_file.close

#########################BEGIN USER INPUT#######################################

filtered_file= open('/Users/fritzlaylinlab/Documents/Prostak/local_blast/Fungal_Homologs_Actin/model_to_Sjaponicus/model_to_Sjaponicus_fresults_bitfiltered.txt', 'a')

#########################END USER INPUT########################################


for line in fwd_results_file:
	elements = re.split("\t|__", line)
	bit_score = float(elements[-1])  #define the bit_score object, making it a float so it can be manipulated later
	if bit_score >= 100:
		filtered_file.write(line)