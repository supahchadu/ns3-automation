library(ggplot2)
library(reshape)
raw<-read.csv("SampleData.csv")
p <- ggplot(raw, aes(x=factor(Person), fill=factor(ExperimentGroup))) 
p <- p + geom_bar(position=position_dodge(width = .8)) 
p <- p + facet_wrap(~ControlGroup)
p