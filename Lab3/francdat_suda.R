library(sdcMicro)
data("francdat")
francdatadf<-as.data.frame(francdat)

#categorical vars must be factors
inputdata <- varToFactor(obj=francdatadf, var=c("Key1","Key2","Key4"))

#defining the sdcObject
sdcObj <- createSdcObj(
  dat=inputdata,
  keyVars=c("Key1","Key2","Key4")
)

#obtaining the household risk from the object
s <- suda2(sdcObj)