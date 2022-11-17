#!/usr/bin/env python3

## script to pull protein seqs and accs from a pfam domain database .tsv

domain_file = "/Users/laboratory/Documents/Fritz_Laylin_Lab/formins/files/protein-matching-PF02181.tsv"
pfam_seqs = "/Users/laboratory/Documents/Fritz_Laylin_Lab/formins/files/protein-matching-PF02181.fasta"
taxids = "/Users/laboratory/Documents/Fritz_Laylin_Lab/formins/files/interpro_taxIDs_early_fungi.txt"

out_file= "/Users/laboratory/Documents/Fritz_Laylin_Lab/formins/files/fh2_matches_from_pfam.fa"
error_file = "/Users/laboratory/Documents/Fritz_Laylin_Lab/formins/files/taxids_not_in_fh2_pfam.txt"


## Define function for getting a list of keys from dictionary which has the given value
## function from https://thispointer.com/python-how-to-find-keys-by-value-in-dictionary/
def getKeysByValue(dictOfElements, valueToFind):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item  in listOfItems:
        if item[1] == valueToFind:
            listOfKeys.append(item[0])
    return  listOfKeys


## put all the sequences containing the pfam domain of interest into a dictionary
fa_dict = {}

with open(pfam_seqs, 'r') as fa_obj:
	for line in fa_obj:
		if '>' in line:
			gene_id = line.rstrip('\n')	
			gene_id_list = gene_id.rsplit()
			id_list = gene_id_list[0].lstrip('>')
			gene_acc = id_list.rsplit('|')[0]
			fa_dict[gene_acc] = ''
		else:
			seq = line.rstrip('\n')
			fa_dict[gene_acc] += seq

print(f'''
Seqs containing the pfam domain added to a dict!''')

## add the taxIDs and accs of proteins with the domain of interest into a dictionary
pfam_dict ={}

with open(domain_file, 'r') as db_obj:
	for line in db_obj:
		line = line.rstrip()
		seq_entry = line.split('\t')
		acc = seq_entry[0]
		taxid = seq_entry[3]
		if acc not in pfam_dict:
			pfam_dict[acc] = taxid
			
print(f'''
Accs and TaxIDs containing the pfam domain added to a dict!''')

## use the dictionaries created to pull accs of seqs corresponding to the taxIDs of interest into a dict
matched_dict = {}

with open(taxids, 'r') as taxid_obj:	
	for line in taxid_obj:
		line = line.rstrip()
		matched_dict[line] = ''
		matched_accs = getKeysByValue(pfam_dict, line)
		#print(f'''
#the accs for {line} are: {matched_accs}
#		''')
		matched_dict[line] = matched_accs

print(f'''
Accs of sequences containing the pfam domain of interest per TaxID added to a dict!''')

## use the dict of species sorted accs containing the domain of interest to create a fasta file of seqs
## add TaxIDs not in the dictionary to a list and print that out

not_found = []

with open(out_file, 'w') as file_obj:
	for k,v in matched_dict.items():
		if k not in pfam_dict.values():
			not_found.append(k)
		for acc in v:
			if acc in fa_dict:
				file_obj.write(f'>{acc}	taxid	{k}\n{fa_dict[acc]}\n')

print(f'''
Seqs containing pfam domain of interest added to specified fasta file!''')

with open(error_file, 'w') as err_obj:
	for taxid in not_found:
		err_obj.write(f'''{taxid}\n''')

print(f'''
TaxIDs not found printed to error file
''')





