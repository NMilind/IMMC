setwd("~/Desktop/IMMC/data")
rm(list=ls())

timezone <- read.csv("timezone.csv", header=F)
names(timezone) <- c("zone.id", "time.standard", "start.time", "gmt.offset", "dst")
timezone <- timezone[,c("zone.id", "time.standard", "gmt.offset", "dst")]
timezone <- unique(timezone)

zone <- read.csv("zone.csv", header=F)
names(zone) <- c("zone.id", "abbreviation", "zone.name")

zonenames <- c()
for (i in 1:nrow(timezone)) {
  zonenames <- c(zonenames, as.character(zone[timezone[i,1],3]))
}

timezone["zone.names"] <- zonenames

write.csv(file="processed.timezone.csv", timezone, row.names=F, col.names=F)