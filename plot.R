library(ggplot2)
df <- read.csv(file="output.csv",sep="\t",head=F)
ggplot(subset(df,df$V1 == "unrelated"),aes(V3*100,color=V1,group=V2)) + geom_density() + scale_color_discrete("related?") + scale_x_continuous("% ID") + theme_minimal()
ggsave("STRlike.pdf", height = 210, width = 297, units = "mm")
