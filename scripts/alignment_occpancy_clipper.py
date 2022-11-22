
# script to remove columns of a protein alignment based on a % occupancy threshold


import pandas as pd
import re

aln_file = '/Users/laboratory/Documents/Fritz_Laylin_Lab/formins/files/fastas/alignment_test.txt'
removed_file = '/Users/laboratory/Documents/Fritz_Laylin_Lab/formins/files/columns_removed_test.txt' 
out_file = '/Users/laboratory/Documents/Fritz_Laylin_Lab/formins/files/fastas/clipped_aln_test.txt'


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
				seq_list = [*seq]				## makes the sequence into a list where each element is an amino acid or a gap
				db_dict[gene_id] = seq_list		## associates the sequence list with the geneID in the database dict
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

aln_dict = fastaparse(aln_file)

aln_df = pd.DataFrame(aln_dict.values(), index = aln_dict.keys())

print(f'''
Alignment added to dataframe
''')

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
Columns with less than 80% occupant removed from alignment''')

## add the new alignment to a fasta file

with open(out_file, 'w') as file_obj:
	for row in aln_df.itertuples():
		geneID = row[0]
		seq = listToString(row[1:])
		file_obj.write(f'{geneID}\n{seq}\n')
	
	
print(f'''
Clipped alignment written to file
''')