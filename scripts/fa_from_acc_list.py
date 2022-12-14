#!usr/bin/env python 3

import re

in_file = "/Users/laboratory/Documents/Fritz_Laylin_Lab/formins/files/blasts_20221117/fh2_hit_accs.txt"
db = "/Users/laboratory/Documents/Fritz_Laylin_Lab/formins/files/protein_sets/early_fungi_prots.fa"
out_file = '/Users/laboratory/Documents/Fritz_Laylin_Lab/formins/files/blasts_20221117/fh2_hit_seqs_20221117.fa'

db_dict = {}

with open(db, 'r') as db_file:
	for line in db_file:
		if '>' in line:
			gene_id = line.rstrip('\n')	
			gene_id_list = gene_id.rsplit()
			gene_acc = gene_id_list[0].lstrip('>')
			db_dict[gene_acc] = ''
		else:
			seq = line.rstrip('\n')
			db_dict[gene_acc] += seq

print(f'\nDatabase Dict Populated!!')

hit_dict = {}

with open(in_file, 'r') as file_obj:
	for line in file_obj:
		line = line.rstrip()
		if line in db_dict.keys():
			hit_dict[line] = db_dict[line]

print(f'\nHit Dict Populated!!\n')


with open(out_file, 'w') as file_out:
	for acc, seq in hit_dict.items():
		file_out.write(f'>{acc}\n{seq}\n')
		