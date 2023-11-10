library(genetics)
library(dplyr)

### Load the data
# Specify the file path to your .raw data file
file_path_SNP <- "/Users/maxvisser/Documents/UPC/BSG-MDS/statistical_genetics/practical1/TSICHR22RAW.raw"
df <- read.table(file_path_SNP, header = TRUE)

# Fitler out non-genetic informations columns
df <- df[,7:ncol(df)]

### 1 How many variants are there in this database? What percentage of the data is missing?
print(ncol(df))
print("Percentages missing data:")
n_missing = sum(is.na(df))
total_data_points = ncol(df) * nrow(df)
perc_missing = (n_missing / total_data_points)*100
print("Number of variants in the dataset:")
print(perc_missing)

### 2 Calculate the percentage of monomorphic variants. 
# Exclude all monomorphics from the database for all posterior computations of the practical. 
# How many variants do remain in your database?

# Remove all the columns that are monomorphic (constant) for marker variant rs8138488_C
variant <- df$rs8138488_C
genotype_count = unique(variant)
print("Genotype counts:")
print(genotype_count)

n_allele_occurences <- table(variant) # values count
print(n_allele_occurences)

allele_AA_count <- length(which(df$rs8138488_C==0))
allele_AB_count <- length(which(df$rs8138488_C==1))
allele_BB_count <- length(which(df$rs8138488_C==2))

minor_allele_count = min(allele_AA_count, allele_AB_count, allele_BB_count) # 2 is the minor allele (that is BB)
print("Minor Allele count:")
print(minor_allele_count)

# calculate allele frequencies:
allele_AA_freq <- allele_AA_count / nrow(df)
allele_AB_freq <- allele_AB_count / nrow(df)
allele_BB_freq <- allele_BB_count / nrow(df)

maf = min(allele_AA_freq, allele_AB_freq, allele_BB_freq)
print(maf)




maf <- function(sequence) {
  # Count the frequency of each unique number in the sequence
  counts <- table(sequence)
  
  # Find the minimum frequency (least occurring number)
  least_frequency <- min(counts)
  
  return(least_frequency)
}

result <- apply(df, 2, maf)





