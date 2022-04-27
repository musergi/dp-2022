slotNames(sdcObj)
str(sdcObj@originalRisk)
risk <- sdcObj@originalRisk$individual[,"risk"]
mean(risk)
mean(sdcObj@risk$individual[,"risk"])