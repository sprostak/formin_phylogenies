# Goal is to get a program that will create a MBBH file that includes the %ID and the bit score from the fwd BLAST results to send to Lil:
#import regex module

import re

#########################BEGIN USER INPUT#######################################

# define the fwd, rev and new MBBH files
fwd_results = "/Users/fritzlaylinlab/Documents/Prostak/local_blast/Fungal_Homologs_Actin/model_to_Umaydis/model_to_Umaydis_fresults.txt"
rev_results = "/Users/fritzlaylinlab/Documents/Prostak/local_blast/Fungal_Homologs_Actin/model_to_Umaydis/model_to_Umaydis_rresults.txt"
new_MBBH_file = open('/Users/fritzlaylinlab/Documents/Prostak/local_blast/Fungal_Homologs_Actin/model_to_Umaydis/model_to_Umaydis_MBBH_id.txt', 'w')

#########################END USER INPUT########################################

# open the forward and reserve results files to read through
fwd_results_file = open(fwd_results)
rev_results_file = open(rev_results)

# write the column headers in the new mbbh file
new_MBBH_file.write("subjectID,queryID,%ID,bit_score" + "\n")
# close the file then open it for appending
new_MBBH_file.close

#########################BEGIN USER INPUT#######################################

new_MBBH_file = open('/Users/fritzlaylinlab/Documents/Prostak/local_blast/Fungal_Homologs_Actin/model_to_Umaydis/model_to_Umaydis_MBBH_id.txt', 'a')

#########################END USER INPUT########################################


# create empty dictionaries for the forward and reverse results, as well as for the query Id and Types, %ID, and Bit-score
df = {}
dr = {}
type_dict = {}
percent_dict = {}
bit_dict = {}


for line in fwd_results_file:
	elements = re.split("\t|__", line)
	query_ID = elements[0]
	query_type = elements[1]
	subject_id = elements[2]
	percent_id = elements[3]
	bit_score = elements[-1]
	if query_ID not in df.keys():
		df[query_ID] = subject_id  # this will pick the first hit and write it into the df dict
		type_dict[query_ID] = query_type # this will write the queryID and its type into a dict
		percent_dict[subject_id] = percent_id # this will write the subjectID and the %ID to the query into a dict
		bit_dict[subject_id] = bit_score.rstrip("\n") #this will write the subjectID and the bit score to the query into a dict

print("4/6 dicts filled")

# gather top hits for each query in the rev results into the dr dictionary
for line in rev_results_file:
	elements = re.split("\t", line)
	query_ID = elements[0]
	subject_ID = elements[1]
	if query_ID not in dr.keys():
		dr[query_ID] = subject_ID # this will pick the first hit and write it into the dr dict

print("5/6 dicts filled")

# close the fwd and rev results files 
fwd_results_file.close()
rev_results_file.close()

# create the empty MBBH dictionary
MBBH = {}
for IDf in df.keys():
	valuef = df[IDf]
	if valuef in dr.keys():
		if IDf == dr[valuef]: # this indicates that if there is a MBBH, the match will be added to the MBBH dictionary
			MBBH[valuef] = IDf

print("6/6 dicts filled!")


# write the MBBHs from the dict into the MBBH file, keeping the type associated with the original query, and the %ID and bit_scor from the fresults
for k,v in MBBH.items():
	for qID,qType in type_dict.items():
		for sID,percent in percent_dict.items():
			for id,bit in bit_dict.items():
				if qID == v and k == sID and k == id:
					new_MBBH_file.write(k + "," + v + "__" + qType + "," + percent + "," + bit + "\n")
			
print("new MBBH file complete!")			

			