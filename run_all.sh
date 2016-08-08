#!/bin/bash

# get folder structure

mkdir files_all
mkdir files_related

# get all opensnp files

cd files_all
wget https://opensnp.org/data/zip/opensnp_datadump.current.zip
unzip opensnp_datadump.current.zip
cd ..


# move related files (hope they have not been deleted in the meantime!)

mv files_all/user1457_file3020_yearofbirth_1961_sex_XY.ftdna-illumina.txt files_related/compare_user1457_ftdna-illumina.txt
mv files_all/user1457_file795_yearofbirth_1961_sex_XY.23andme.txt files_related/compare_user1457_23andme.txt

mv files_all/user1987_file1173_yearofbirth_unknown_sex_XY.ftdna-illumina.txt compare_user1987_ftdna-illumina.txt
mv files_all/user1987_file1174_yearofbirth_unknown_sex_XY.23andme.txt compare_user1987_23andme.txt

mv files_all/user288_file121_yearofbirth_1987_sex_XX.23andme.txt compare_user288_23andme.txt
mv files_all/user288_file122_yearofbirth_1987_sex_XX.ftdna-illumina.txt compare_user288_ftdna-illumina.txt

mv files_all/user305_file133_yearofbirth_1972_sex_XY.23andme.txt compare_user305_23andme.txt
mv files_all/user305_file134_yearofbirth_1972_sex_XY.ftdna-illumina.txt compare_user305_ftdna-illumina.txt

# ok, let's do the comparisons and plot that crap
python compare.py files_all/ files_related/ > output.csv
Rscript plot.R
