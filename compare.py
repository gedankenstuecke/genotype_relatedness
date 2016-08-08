import glob
import sys
import random

# NUMBER OF DIFFERENT GENOTYPES WE WANT TO TEST

compare_n_genotypes = 20

# TESTS PER GENOTYPE COMPARISON

test_per_genotype = 100

# SNPS USED FOR EACH TEST

snps_per_test = 50


def get_random_genotypes(file_list):
	'''
	ok, that's an easy one:
	give us two genotpes from the list
	'''
	g1,g2 = random.sample(file_list,2)
	return g1,g2

def read_genotype_andme(file_handle):
	'''
	similarly simple: convert the 23andme file
	into a key/value pair w/
	keys => RSIDs
	values => sorted list of alleles

	ignore everything that's not a diploid locus
	'''
	genotype = {}
	for i in open(file_handle):
		if i[0] != "#":
			ia = i.strip().split("\t")
			rsid = ia[0]
			alleles = list(ia[-1])
			alleles.sort()
			if len(alleles) == 2:
				genotype[rsid] = alleles
	return genotype

def read_genotype_ft(file_handle):
	'''
	similarly simple: convert the ft-DNA file
	into a key/value pair w/
	keys => RSIDs
	values => sorted list of alleles

	ignore everything that's not a diploid locus
	'''
	genotype = {}
	for j,i in enumerate(open(file_handle)):
		if j > 0:
			ia = i.replace("\"","").strip().split(",")
			rsid = ia[0]
			alleles = list(ia[-1])
			alleles.sort()
			if len(alleles) == 2:
				genotype[rsid] = alleles
	return genotype


def get_distance(shared_snps,g1,g2):
	'''
	get the distance based on a random set of n SNPs
	each matching allele is scored.
	'''
	similarity = 0
	random_snps = random.sample(shared_snps,snps_per_test)
	for snp in random_snps:
		if g1[snp][0] == g2[snp][0]:
			similarity += 0.5
		if g1[snp][1] == g2[snp][1]:
			similarity += 0.5

	return (similarity/snps_per_test)

def get_distribution(shared_snps,g1h,g2h,g1,g2,relatedness):
	'''
	let's get a distribution of how well the two genotyping files match
	based on a set of XXX different SNP sets with YYY SNPs each.
	'''
	tests_performed = 0
	snps_to_test = random.sample(shared_snps,snps_per_test)
	while tests_performed < test_per_genotype:
		distance = get_distance(shared_snps,g1,g2)
		print relatedness + "\t" + g1h+"_"+g2h + "\t" + str(distance)
		tests_performed += 1

def __main__():
	'''
	ok, this is the ugly part that's not nice so far.
	'''

	# read in all the regular files that are 23andme
	folder = sys.argv[1]
	if folder[-1] != "/":
        	folder += "/"
	files_andme = glob.glob(folder+"*.23andme.*")

	# now iterate until we've compared as many files as we wanted
	i = 0
	while i < compare_n_genotypes:
		g1h,g2h = get_random_genotypes(files_andme) # randomly draw two
		genotype1 = read_genotype_andme(g1h)
		genotype2 = read_genotype_andme(g2h)
		shared_snps = list(genotype1.viewkeys() & genotype2.viewkeys())
		if len(shared_snps) >= snps_per_test:
			get_distribution(shared_snps,g1h,g2h,genotype1,genotype2,"unrelated")
			i += 1
		else:
			next

	# done, now we've compared as many (maybe) unrelated files as we wanted
	# let's do a similar thing for the related ones.
	related_folder = sys.argv[2]
	if related_folder[-1] != "/":
		related_folder += "/"
	related_files = glob.glob(related_folder + "*_23andme.txt")
	for file_andme in related_files:
		file_ftdna = file_andme.replace("_23andme.txt","_ftdna-illumina.txt")
		genotype1 = read_genotype_andme(file_andme)
		genotype2 = read_genotype_ft(file_ftdna)
		shared_snps = list(genotype1.viewkeys() & genotype2.viewkeys())
		if len(shared_snps) >= snps_per_test:
			get_distribution(shared_snps,file_andme,file_ftdna,genotype1,genotype2,"related")
		else:
			next

__main__()
