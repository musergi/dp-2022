# created using sdcMicro 5.6.1
library(sdcMicro)

obj <- NULL
if (!exists("df")) {
  stop('object "df" is missing; make sure it exists.`', call. = FALSE)
}
obj$inputdata <- readMicrodata(path="df", type="rdf", convertCharToFac=FALSE, drop_all_missings=FALSE)
inputdataB <- obj$inputdata

## Convert a numeric variable to factor (each distinct value becomes a factor level)
inputdata <- varToFactor(obj=inputdata, var=c("REGION","SEX","AGE","MARSTAT"))
## Set up sdcMicro object
sdcObj <- createSdcObj(dat=inputdata,
	keyVars=c("REGION","SEX","AGE","MARSTAT"), 
	numVars=NULL, 
	weightVar=NULL, 
	hhId=NULL, 
	strataVar=NULL, 
	pramVars=NULL, 
	excludeVars=NULL, 
	seed=0, 
	randomizeRecords=FALSE, 
	alpha=c(1))

## Store name of uploaded file
opts <- get.sdcMicroObj(sdcObj, type="options")
opts$filename <- "df"
sdcObj <- set.sdcMicroObj(sdcObj, type="options", input=list(opts))

