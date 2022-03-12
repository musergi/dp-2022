# Exercise 2.1 holiii que tal?
library(sdcMicro)
data("free1")
df <- as.data.frame(free1)

#Section a
selected_attr <- attributes(df)$names[1:4]
print(selected_attr)
# CAT CAT NUM CAT

# Section b
subdf <- df[,selected_attr]
combinations <- table(subdf)
combination_count <- prod(dim(combinations))
print(combination_count)

# Section c
subdf <- df[,c("REGION", "SEX")]
contingency <- table(subdf)
is_not_k2 <- contingency == 1
k2_violations <- sum(contingency[is_not_k2])
is_not_k3 <- (contingency > 0) & (contingency < 3)
k3_violations <- sum(contingency[is_not_k3])
print(k2_violations)
print(k3_violations)

subdf <- df[,selected_attr]
contingency <- table(subdf)
is_not_k2 <- contingency == 1
k2_violations <- sum(contingency[is_not_k2])
is_not_k3 <- (contingency > 0) & (contingency < 3)
k3_violations <- sum(contingency[is_not_k3])
print(k2_violations)
print(k3_violations)

# Section d
freq <- freqCalc(df, keyVars = c("REGION", "SEX"))
print(freq)


freq <- freqCalc(df, keyVars = selected_attr)
print(freq)

# Exercise 2.2

# Section a
sdcObj <- createSdcObj(df, keyVars = selected_attr)

# Section b
print(sdcObj)

# Section c
print(slotNames(sdcObj))

# Section d
print(sdcObj@risk$global$risk)
print(sdcObj@risk$global$risk_pct)
print(sdcObj@risk$global$risk_ER)

# Section e
sdcObj <- varToFactor(sdcObj, selected_attr)

# Exercise 3.1

# Section a
l <- levels(sdcObj@manipKeyVars$REGION)
north <- l[1:45]
south <- l[46:90]
east <- l[91:135]
west <- l[136:182]
sdcObj <- groupAndRename(sdcObj, var = "REGION", before = north, after = c("NORTH"))
sdcObj <- groupAndRename(sdcObj, var = "REGION", before = south, after = c("SOUTH"))
sdcObj <- groupAndRename(sdcObj, var = "REGION", before = east, after = c("EAST"))
sdcObj <- groupAndRename(sdcObj, var = "REGION", before = west, after = c("WEST"))

# Section b
print(sdcObj)

# Section c
sdcObj <- varToNumeric(sdcObj, var = c("AGE"))
sdcObj <- globalRecode(sdcObj,
    column = "AGE",
    breaks=c(0, 14, 25, 64, 74),
    labels = c("CHILDREN", "YOUNG", "ADULTS", "SENIOR"))

# Section d
print(sdcObj)

# Exercise 3.2

# Section a
sdcObj <- createSdcObj(df, keyVars = selected_attr)

# Exercise 3.3

# Section a
tab <- table(df[,"MARSTAT"])
print(tab)
norm_prob <- matrix(tab)[,1] / sum(matrix(tab)[,1])
shift <- function(v) {
  n <- length(v)
  y <- rep(0, n)
  for(i in 1:n) {
    y[(i) %% n + 1] = v[i]
  }
  return(y)
}
rem <- diag(0.1 * min(norm_prob) /norm_prob)
m <- diag(4) - rem + t(apply(rem, 1, shift))
postProb <- m %*% matrix(tab)

# Section d
inputdata <- varToFactor(obj=df, var=c("SEX","REGION","AGE","MARSTAT"))
## Set up sdcMicro object
sdcObj <- createSdcObj(dat=inputdata,
                       keyVars=c("REGION","SEX","AGE"),
                       numVars=NULL,
                       weightVar=NULL,
                       hhId=NULL,
                       strataVar=NULL,
                       pramVars=c("MARSTAT"),
                       excludeVars=NULL,
                       seed=0,
                       randomizeRecords=FALSE,
                       alpha=c(1))
sdcObj <- pram(sdcObj, variables=c("MARSTAT"), pd=0.8, alpha=0.5)
P <- sdcObj@pram$params$MARSTAT$Rs
e <- eigen(t(P))
idx <- abs(e$values - 1.0) < 1e-12
res <- e$vectors[,idx] / sum(e$vectors[,idx])