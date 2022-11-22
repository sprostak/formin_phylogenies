
# script to remove columns of a protein alignment based on a % occupancy threshold


import pandas as pd
import re

aln_file = '/Users/laboratory/Documents/Fritz_Laylin_Lab/formins/files/hmmalign_20221122/20221122_prots_with_fh2_aligned_clipped.fa'
removed_file = '/Users/laboratory/Documents/Fritz_Laylin_Lab/formins/files/hmmalign_20221122/columns_removed.txt' 
out_file = '/Users/laboratory/Documents/Fritz_Laylin_Lab/formins/files/hmmalign_20221122/20221122_prots_with_fh2_for_tree.fa'


## define the fasta parser function to put the seq and any gaps inserted into a list associated with geneID
def fastaparse(file):
	db_dict = {}
	with open(file, 'r') as db_file:
		for line in db_file:
			line = line.strip()
			if '>' in line:
				gene_id = line.rstrip('\n')	
				db_dict[gene_id] = ''
			else:
				seq = line.rstrip('\n')
				db_dict[gene_id] += seq		## associates the sequence with the geneID in the database dict
	return db_dict

## define a function to convert a list to a string
def listToString(l):
    # initialize an empty string
    str1 = ""
    # traverse in the string
    for ele in l:
        str1 += ele
    # return string
    return str1

aln_dict_string = fastaparse(aln_file)
aln_dict_list = {}


## make a new alignment dictionary where the values are the sequence in list form for the given gene
for gene, seq in aln_dict_string.items():
	seq_list = [*seq]
	if gene not in aln_dict_list:
		aln_dict_list[gene] = seq_list

aln_df = pd.DataFrame(aln_dict_list.values(), index = aln_dict_list.keys())

print(f'''
Alignment added to dataframe''')

with open(removed_file, 'w') as f:
	for (columnName, columnData) in aln_df.items():
		column_len = len(columnData.values)			## count the number of positions in the column
		column = listToString(columnData.values)	## convert the column to a string
		gap_count = column.count('-')				## count the number of gaps in the column
		occ = column_len - gap_count				## calculate the number of amino acids in the column
		occ_pct = (occ/column_len)*100				## calculate the percent occupancy in the column
		if occ_pct < 80 :							## test if %occ is less than 80% then deleted column from dataframe
			f.write(f'{columnName} occupancy is less than 80%  ({occ_pct}%)\n')
			del aln_df[columnName]


print(f'''
Columns with less than 80% occupancy added to columns_removed.txt 
Columns with less than 80% occupancy removed from alignment''')

## add the new alignment to a fasta file

with open(out_file, 'w') as file_obj:
	for row in aln_df.itertuples():
		geneID = row[0]
		seq = listToString(row[1:])
		file_obj.write(f'{geneID}\n{seq}\n')
	
	
print(f'''
Clipped alignment written to file
''')