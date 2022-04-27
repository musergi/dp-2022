# created using sdcMicro 5.6.1
library(sdcMicro)

obj <- NULL
if (!exists("testdatadf")) {
  stop('object "testdatadf" is missing; make sure it exists.`', call. = FALSE)
}
obj$inputdata <- readMicrodata(path="testdatadf", type="rdf", convertCharToFac=FALSE, drop_all_missings=FALSE)
inputdata <- obj$inputdata

## Convert a numeric variable to factor (each distinct value becomes a factor level)
inputdata <- varToFactor(obj=inputdata, var=c("urbrur","roof","walls","water","electcon","relat","sex","age","hhcivil"))
## Set up sdcMicro object
sdcObj <- createSdcObj(dat=inputdata,
	keyVars=c("urbrur","roof","walls","water","electcon","relat","sex","age","hhcivil"), 
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
opts$filename <- "testdatadf"
sdcObj <- set.sdcMicroObj(sdcObj, type="options", input=list(opts))


## Local suppression to obtain k-anonymity
sdcObj <- kAnon(sdcObj, importance=c(1,6,3,7,4,8,2,9,5), combs=NULL, k=c(5))