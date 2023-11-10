# Once a R terminal is created with the command "R: Create R terminal",
# you can run the R script with "Shift + Cmd + S"
print("Hello, world!")
print(1 + 2)

# Create a R plot
plot(1:10, 1:10, main = "My first plot in R")

# For loop in R
# for (x in 1:10) {
#   print(x)
# }

# Create a variable in R
name <- "John"
age <- 40
print(paste(name, age))

my_var <- 30 # my_var is type of numeric
my_var <- "Sally" # my_var is now of type character (aka string)

# we can use class() to check the type of a variable
x <- 10.5
print(class(x))

# There are 3 numeric types in R
x <- 10.5 # numeric
y <- 10L # integer
z <- 1i # complex

# Type casting with as.numeric(), as.integer(), as.character()
x <- 1L # integer
y <- 2 # numeric
a <- as.numeric(x) # cast x to numeric
b <- as.integer(y) # cast y to integer

print(max(1, 2, 3, 4))
print(min(1, 2, 3, 4))
