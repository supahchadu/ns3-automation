library(ggplot2) #for ggplot use plotting
library(reshape) #for combining multiple variables
raw<-read.csv("SampleData.csv", sep=",") #Reads the data in each comma
mm<- melt(raw,id="Person") #Formats the data frame to rely on Person as Y axis

# for switching the order of variables present in the plot
mm$Person<-factor(mm$Person, levels=c("Experiment","Control"))
# pass in our Data Frame var mm and feed which data to graph
p<- ggplot(mm, aes(x=Person,y=value, group=variable)) 
p<- p + geom_bar(width=.3,aes(fill=variable),stat = "identity", position="dodge")
p<- p + scale_fill_manual("legend", labels=c("Female", "Male"),values = c("G1" = "#f9cb9c", "G2" = "#3d85c6"))
p<- p + labs(title="")
p<- p + xlab("")
p<- p + ylab("Confidence in Understanding Course Materials")
p<- p + theme(panel.background=element_blank(), axis.line.x = element_line(color = "black"), axis.line.y = element_line(color="black"), text=element_text(size=25, family = "Times"))
p<- p + theme(legend.title=element_blank(), legend.background=element_rect(color = "black"), axis.text.x = element_text(face = "bold", margin = margin(5,0,0,0)), axis.title.x=element_text(margin = margin(30,0,0,0)))
p<- p + scale_y_continuous(limit=c(0,5), expand = c(0,0))
p <- p + coord_flip()
p
ggsave(filename = "assignment.pdf", plot = last_plot(), width=210,height=297,units="mm")