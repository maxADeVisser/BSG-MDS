library(genetics)
library(dplyr)

### Load the data
# Specify the file path to your .raw data file
file_path_SNP <- "/Users/maxvisser/Documents/UPC/BSG-MDS/statistical_genetics/practical1/TSICHR22RAW.raw"
df <- read.table(file_path_SNP, header = TRUE)

# Fitler out non-genetic informations columns
df <- df[,7:ncol(df)]

### 1 How many variants are there in this database? What percentage of the data is missing?
print("Percentages missing data:")
print(ncol(df))
n_missing = sum(is.na(df))
total_data_points = ncol(df) * nrow(df)
perc_missing = (n_missing / total_data_points)*100
print("Number of variants in the dataset:")
print(perc_missing)

# 1.2 Calculate the percentage of monomorphic variants. 
monomorphic <- sapply(df, function(x) length(unique(x)) == 1)
n_monomorhic <- sum(monomorphic)
monomorhic_freq <- (n_monomorhic / ncol(df))*100
print(monomorhic_freq)

# 1.2 Exclude all monomorphic
df_mono <- df[, !monomorphic]
print(length(df_mono)) # number of cols

# 1.3 
variant <- df_mono$rs8138488_C
genotype_count = table(variant)
print("Genotype counts:")
print(genotype_count)

# 1.3
n_allele_occurences <- table(variant) # values count
print(n_allele_occurences)

allele_AA_count <- length(which(df_mono$rs8138488_C==0))
allele_AB_count <- length(which(df_mono$rs8138488_C==1))
allele_BB_count <- length(which(df_mono$rs8138488_C==2))

minor_allele_count = min(allele_AA_count, allele_AB_count, allele_BB_count) # 2 is the minor allele (that is BB)
print("Minor Allele count:")
print(minor_allele_count)

# 1.3 calculate allele frequencies:
allele_AA_freq <- allele_AA_count / nrow(df_mono)
allele_AB_freq <- allele_AB_count / nrow(df_mono)
allele_BB_freq <- allele_BB_count / nrow(df_mono)

maf = min(allele_AA_freq, allele_AB_freq, allele_BB_freq)
print(maf)



maf <- function(sequence) {
  # Count the frequency of each unique number in the sequence
  counts <- table(sequence)
  n_readings = 102
  # Find the minimum frequency (least occurring number)
  least_frequency <- min(counts)
  maf = least_frequency / n_readings
  
  return(maf)
}


result <- apply(df_mono, 2, maf)
hist(result, main="Histogram of MAFs for all genetic markers", xlab="Minor Allele Frequency (MAP)", ylab="Frequency")

print(length(result[result<0.05])/length(result)*100)
print(length(result[result<0.01])/length(result)*100)



