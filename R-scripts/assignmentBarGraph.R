library(ggplot2)
library(reshape)
raw<-read.csv("SampleData.csv",sep = ",")
raw[,1]<-factor(raw[,1],levels=c("first","second"),ordered = FALSE)
raw[,2]<-factor(raw[,2],levels=c("first","second"),ordered = FALSE)
raw=raw[,c(1,2)]
freq=table(col(raw),as.matrix(raw))
theNames=c("ExperimentalGroup","ControlGroup")
data=data[,c(1,2)]
data=data.frame(cbind(freq),theNames)
data.m <- melt(data, id.vars='theNames')
p<-ggplot(data.m, aes(theNames,value)) + geom_bar(aes(fill = variable), position = "dodge", stat = "identity")
p<- p + labs(title="Assignment")
p<- p + xlab("Groups")
p<- p + ylab("Y-Axis")
p
ggsave(filename = "assignment.pdf", plot = last_plot())