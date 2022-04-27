# created using sdcMicro 5.6.1
library(sdcMicro)
data(testdata)
testdatadf<-as.data.frame(testdata)

#categorical vars must be factors
inputdata <- varToFactor(obj=testdatadf, var=c("urbrur","roof","walls","water","electcon","relat","sex","age","hhcivil"))

#defining the sdcObject
sdcObj <- createSdcObj(
  dat=inputdata,
  keyVars=c("urbrur","roof","walls","water","electcon","relat","sex","age","hhcivil"),
  weightVar=c("sampling_weight"),
  hhId=c("ori_hid"),
)

#obtaining the household risk from the object
hh_rk <- sdcObj@risk$individual[sdcObj@origData$ori_hid==1,"hier_risk"]
cat("The household risk for hh_id=1 is:",hh_rk[1])
