# script to add species information to the identifier of a fasta sequence


seq_file = "/Users/laboratory/Documents/Fritz_Laylin_Lab/formins/files/fastas/early_fungi_prots_with_fh2.fa"
prot_db = "/Users/laboratory/Documents/Fritz_Laylin_Lab/formins/files/protein_sets/early_fungi_prots.fa"
out_file = "/Users/laboratory/Documents/Fritz_Laylin_Lab/formins/files/fastas/early_fungi_prots_with_fh2_detailed.fa"

## define the fasta parser function
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
				db_dict[gene_id] += seq
	return db_dict




## add protein database to dictionary

protdb_dict = fastaparse(prot_db)

print(f'\nDatabase Dict Populated!!')

## put the sequences you want to add more detail to the gene_id into a new dict

seq_dict = fastaparse(seq_file)


print(f'\nSequence Dict Poulated!!')


with open(out_file, 'w') as desc_file:
	for acc_id in seq_dict:
		acc_list = acc_id.rsplit('\t')
		acc = acc_list[0]						## store the found seq acc into the acc variable
		for gene_id in protdb_dict:
			gene = gene_id.rsplit('[')
			gene_desc = gene[0].rsplit()
			gene_acc = gene_desc[0]				## store the gene acc from the db in the gene_acc variable
			sp_name = gene[-1].rstrip(']')		## store the species associated with the gene_acc in the sp_name variable
			if acc == gene_acc:					## test is the acc of interest matches the gene_acc
				desc_file.write(f'>{acc} {sp_name}\n{seq_dict[acc]}\n')			## write the fasta format to the out file, including the species name associated with the acc
			
print(f'\nResults file written!!')		
	