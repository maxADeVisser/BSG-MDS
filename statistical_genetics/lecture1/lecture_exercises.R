data_path <- "/Users/maxvisser/Downloads/JapaneseSTRs.rda"
data <- load(data_path)
df <- as.data.frame(data)
print(head(df))