#group
library(ggplot2)
library(reshape)

library(ggplot2) #for ggplot use plotting
library(reshape) #for combining multiple variables
raw<-read.csv("highandlownew.csv", sep=",") #Reads the data in each comma
mz<- melt(raw,id="Speed") #Formats the data frame to rely on Person as Y axis

# for switching the order of variables present in the plot
#mz$Speed<-factor(mz$Person, levels=c("Experiment Group","Control Group"))
# pass in our Data Frame var mm and feed which data to graph
p<- ggplot(mz, aes(x=Speed,y=value, colour=variable, shape=variable)) 
p<- p + geom_line(linetype=2) + geom_point(size = 4)
p<- p + scale_fill_manual("legend", labels=c("Low Packets", "High Packets"))
p<- p + labs(title="")
p<- p + xlab("Middlebox to Reciever Link Capacity (Mbps)")
p<- p + ylab("Aggregate Loss Rate (%)")
#p<- p + theme(panel.border=element_blank(),panel.grid.major=element_blank(),axis.line.x = element_line(color = "black"), axis.line.y = element_line(color="black"), text=element_text(size=25, family = "Times"))
p<- p + theme_bw() + theme(legend.title=element_blank(), legend.background=element_rect(color = "black"), axis.text.x = element_text(face = "bold", margin = margin(0,0,0,0)), axis.title.y=element_text(margin = margin(0,30,0,0)))
p <- p + theme(axis.line.x = element_line(color = "black"), axis.line.y = element_line(color="black"), text=element_text(size=25, family = "Helvetica"),axis.title.x=element_text(margin = margin(30,0,0,0)))
p<- p + scale_y_continuous(limit=c(0,100), expand = c(0,0), breaks=seq(10,100,10))
p <- p + coord_cartesian(xlimit=c(0,100))
p <- p + scale_x_continuous(breaks=seq(0,100,10), expand=c(0,0))
p
ggsave(filename = "highandlowloss.pdf", plot = last_plot(), width=297,height=210,units="mm")