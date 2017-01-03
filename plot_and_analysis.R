hama_out <- read.csv("C:\Users\Adeesha Ekanayake\Dropbox\Marcy\Behavior Class\BehaviorClass\hama_out.csv", header=TRUE)
sav_out <- read.csv("C:\Users\Adeesha Ekanayake\Dropbox\Marcy\Behavior Class\BehaviorClass\sav_out.csv", header=TRUE)


hama.df <- hama_out
sav.df <- sav_out


pop.sizes.df <- data.frame("Taxon" = c(rep("H", times = 1000), rep("S", times = 998)), 
                           "PopSizes" = c(hama.df$Pop_Size, sav.df$Pop_Size))
library(ggplot2)
p <- ggplot(data = pop.sizes.df, aes(x=Taxon, y = PopSizes)) + 
  geom_dotplot(binaxis = 'y', stackdir = 'center', binwidth = 15)
p + geom_segment(aes(x=0.75, y = 650, xend=1.25, yend=650, colour = Taxon), colour = "coral3", 
                 size = 2, linetype = "1111") +
  geom_segment(aes(x=1.75, y = 540, xend = 2.25, yend = 540, colour = Taxon), colour = "dodgerblue1", 
               size = 2, linetype = "1111") +
  theme(panel.background = element_rect(fill = "white"), 
        axis.text = element_text(size = 12), 
        panel.grid.major.y = element_line(color = "gray80"),
        panel.grid.minor.y = element_line(color = "gray90"),
        panel.grid.major.x = element_line(color = "white"),
        panel.grid.minor.x = element_line(color = "white"),
        panel.border = element_rect(color = "black", size = 3, fill = NA),
        plot.title = element_text(size = rel(1.75)),
        axis.title.y = element_text(size = rel(1.25)),
        axis.title.x = element_text(size = rel(1.25))) +
  scale_x_discrete(labels = c("Hamadryas", "Savanna")) + 
  scale_y_continuous(minor_breaks = seq(0,1500,100)) + 
  
  labs(
    y = "Population",
    title = "Population Sizes Were Acceptable in Simulated Populations") 

mean(pop.sizes.df[1:1000,2])

mean(pop.sizes.df[1001:length(pop.sizes.df$Taxon), 2])

sex.ratio.df <- data.frame("Taxon" = c(rep("H", times = 1000), rep("S", times = 998)), 
                           "SexRatio" = c(hama.df$Ad_Sex_Ratio, sav.df$Ad_Sex_Ratio))
library(ggplot2)
p <- ggplot(data = sex.ratio.df, aes(x=Taxon, y = SexRatio)) + 
  geom_dotplot(binaxis = 'y', stackdir = 'center', binwidth = 0.02)
p + geom_segment(aes(x=0.75, y = 1.77, xend=1.25, yend=1.77, colour = Taxon), colour = "coral3", 
                 size = 2, linetype = "1111") +
  geom_segment(aes(x=1.75, y = 2, xend = 2.25, yend = 2, colour = Taxon), colour = "dodgerblue1", 
               size = 2, linetype = "1111") +
  theme(panel.background = element_rect(fill = "white"), 
        axis.text = element_text(size = 12), 
        panel.grid.major.y = element_line(color = "gray80"),
        panel.grid.minor.y = element_line(color = "gray90"),
        panel.grid.major.x = element_line(color = "white"),
        panel.grid.minor.x = element_line(color = "white"),
        panel.border = element_rect(color = "black", size = 3, fill = NA),
        plot.title = element_text(size = rel(1.75)),
        axis.title.y = element_text(size = rel(1.25)),
        axis.title.x = element_text(size = rel(1.25))) +
  scale_x_discrete(labels = c("Hamadryas", "Savanna")) + 
  scale_y_continuous(minor_breaks = seq(0,3,0.1), limits = c(0.95, 3)) + 
  
  labs(
    y = "Females Per Male",
    title = "Adult Sex Ratios Were Realistic in Simulated Populations") 

mean(sex.ratio.df[1:1000,2])

mean(sex.ratio.df[1001:length(pop.sizes.df$Taxon), 2])

hama.df.sire <- hama.df[,5:length(hama.df[1,])]
sav.df.sire <- sav.df[,5:length(sav.df[1,])]

hama.df.sire <- data.frame(hama.df.sire, "sums" = rep(0, times=length(hama.df.sire[,1])))

for (i in 1:length(hama.df.sire[,1])){
  hama.df.sire[i,"sums"] <- sum(hama.df.sire[i,])
}

for (i in 1:length(hama.df.sire[1,])){
  this_row <- hama.df.sire[,i]
  this_row <- sort(this_row)
  hama.df.sire[1001,i] <- mean(this_row)
  hama.df.sire[1002,i] <- this_row[26]
  hama.df.sire[1003,i] <- this_row[975]
}

for (i in 2:87){
  offspring_col <- sum(hama.df.sire[1:1000,i]) * (i-1)
  hama.df.sire[1004,i] <- offspring_col
}


sav.df.sire <- data.frame(sav.df.sire, "sums" = rep(0, times=length(sav.df.sire[,1])))

for (i in 1:length(sav.df.sire[,1])){
  sav.df.sire[i,"sums"] <- sum(sav.df.sire[i,])
}

for (i in 1:length(sav.df.sire[1,])){
  this_row <- sav.df.sire[,i]
  this_row <- sort(this_row)
  sav.df.sire[1001,i] <- mean(this_row)
  sav.df.sire[1002,i] <- this_row[26]
  sav.df.sire[1003,i] <- this_row[975]
}

for (i in 2:(length((sav.df.sire[1,])) - 1)){
  offspring_col <- sum(sav.df.sire[1:998,i]) * (i-1)
  sav.df.sire[1004,i] <- offspring_col
}

colnames(hama.df.sire) <- 0:(length(hama.df.sire[1,]) - 1)
colnames(sav.df.sire) <- 0:(length(sav.df.sire[1,]) - 1)

hama.df.sire.rotated <- data.frame("N_Offspring" = 0, "N_Males" = 0)
row <- 1

for (i in 1:length(hama.df.sire[1,])){
  for (j in 1:length(hama.df.sire[,1])){
    hama.df.sire.rotated[row,1] <- i-1
    hama.df.sire.rotated[row,2] <- hama.df.sire[j, i]
    row <- row + 1
  }
}

to_remove <- c()
for (i in 1:length(hama.df.sire.rotated[,1])){
  if (hama.df.sire.rotated[[i,2]] == 0){
    to_remove = c(to_remove, i)
  } 
}
hama.df.sire.rotated <- hama.df.sire.rotated[-to_remove,]

sav.df.sire.rotated <- data.frame("N_Offspring" = 0, "N_Males" = 0)
row <- 1

for (j in 1:length(sav.df.sire[,1])){
  for (i in 1:length(sav.df.sire[1,])){
    sav.df.sire.rotated[row,1] <- i-1
    sav.df.sire.rotated[row,2] <- sav.df.sire[j, i]
    row <- row + 1
    print(row)
  }
}

to_remove <- c()
for (i in 1:length(sav.df.sire.rotated[,1])){
  if (sav.df.sire.rotated[[i,2]] == 0){
    to_remove = c(to_remove, i)
  } 
}
sav.df.sire.rotated <- sav.df.sire.rotated[-to_remove,]

library(ggplot2)
p <- ggplot(hama.df.sire.rotated, aes(x=factor(N_Offspring), y=N_Males)) + 
  geom_dotplot(binaxis='y', stackdir='center', binwidth = 1)

p + #stat_summary(fun.data=mean_se, 
  #             geom="errorbar", color="coral3", width=1, lwd = 1) +
  
  stat_summary(fun.y=mean, geom="point", color="coral3", size = 1.5, shape = 18) +
  
  theme(panel.background = element_rect(fill = "white"), 
        axis.text = element_text(size = 10), 
        panel.grid.major = element_line(color = "gray80"),
        panel.grid.minor = element_line(color = "white"),
        panel.border = element_rect(color = "black", size = 1, fill = NA),
        plot.title = element_text(size = rel(1)),
        axis.title.y = element_text(size = rel(0.8)),
        axis.title.x = element_text(size = rel(0.8))) + 
  scale_x_discrete(breaks = seq(0, 50, 5), limits = 0:50) +
  scale_y_discrete(breaks = seq(0, 2500, 500), limits = -50:2500) +
  
  labs(
    x = "N Offspring born",
    y = "Males who had that many offspring",
    title = "Male Lifetime Repro Success: Hamadryas")

p <- ggplot(sav.df.sire.rotated, aes(x=factor(N_Offspring), y=N_Males)) + 
  geom_dotplot(binaxis='y', stackdir='center', binwidth = 1)

p + #stat_summary(fun.data=mean_se, 
  #             geom="errorbar", color="coral3", width=1, lwd = 1) +
  
  stat_summary(fun.y=mean, geom="point", color="dodgerblue1", size = 1.5, shape = 18) +

  
  theme(panel.background = element_rect(fill = "white"), 
        axis.text = element_text(size = 10), 
        panel.grid.major = element_line(color = "gray80"),
        panel.grid.minor = element_line(color = "white"),
        panel.border = element_rect(color = "black", size = 1, fill = NA),
        plot.title = element_text(size = rel(1)),
        axis.title.y = element_text(size = rel(0.8)),
        axis.title.x = element_text(size = rel(0.8))) +
  scale_x_discrete(breaks = seq(0, 50, 5), limits = 0:50) +
  scale_y_discrete(breaks = seq(0, 2500, 500), limits = -100:2500) + 
  labs(
    x = "N Offspring born",
    y = "Males who had that many offspring",
    title = "Male Lifetime Repro Success: Savanna")


colnames(hama.df.sire.rotated) = c("N_Offspring", "N_Males", "Taxa")
sav.df.sire.rotated <- data.frame(sav.df.sire.rotated, "Taxa" = rep(x="S", times = length(sav.df.sire.rotated[,1])))

both_taxa_sire <- rbind(hama.df.sire.rotated, sav.df.sire.rotated)

p <- ggplot(both_taxa_sire, aes(x=factor(N_Offspring), y=N_Males, fill = Taxa)) + 
  geom_dotplot(binaxis='y', stackdir='center', binwidth = 10, shape=1)

p + 
  theme(panel.background = element_rect(fill = "white"), 
        axis.text = element_text(size = 10), 
        panel.grid.major = element_line(color = "gray80"),
        panel.grid.minor = element_line(color = "white"),
        panel.border = element_rect(color = "black", size = 1, fill = NA),
        plot.title = element_text(size = rel(1)),
        axis.title.y = element_text(size = rel(0.8)),
        axis.title.x = element_text(size = rel(0.8))) +
  scale_x_discrete(breaks = seq(0, 50, 5), limits = 0:50) +
  scale_y_discrete(breaks = seq(0, 2500, 500), limits = -100:2500) + 
  labs(
    x = "N Offspring born",
    y = "Males who had that many offspring",
    title = "Male Lifetime Repro Success, Both Taxa")



sav.summary <- data.frame("Offspring" = 0:368, "MeanMales" = as.numeric(sav.df.sire[1001,]), "LLCI" = as.numeric(sav.df.sire[1002,]), "ULCI" = as.numeric(sav.df.sire[1003,]), "Taxa" = rep("S", times=369))
ham.summary <- data.frame("Offspring" = 0:87, "MeanMales" = as.numeric(hama.df.sire[1001,]), "LLCI" = as.numeric(hama.df.sire[1002,]), "ULCI" = as.numeric(hama.df.sire[1003,]), "Taxa" = rep("H", times = 88))

sav.summary <- sav.summary[-369,]
ham.summary <- ham.summary[-88,]

both_taxa_sire <- rbind(ham.summary, sav.summary)

p <- ggplot(both_taxa_sire, aes(x=Offspring, y=MeanMales, colour = factor(Taxa)))

p + geom_point(size = 2)+
  geom_line() +
  geom_line(aes(x=Offspring, y=LLCI, colour = factor(Taxa)), linetype = 2) +
  geom_line(aes(x=Offspring, y=ULCI, colour = factor(Taxa)), linetype = 2) +
  theme(panel.background = element_rect(fill = "white"), 
        axis.text = element_text(size = 10), 
        panel.grid.major = element_line(color = "gray80"),
        panel.grid.minor.y = element_line(color = "gray90"),
        panel.grid.minor.x = element_line(color = "white"),
        panel.border = element_rect(color = "black", size = 1, fill = NA),
        plot.title = element_text(size = rel(2)),
        axis.title.y = element_text(size = rel(0.8)),
        axis.title.x = element_text(size = rel(0.8))) +
  scale_x_continuous(breaks = seq(0,30,5), limits = c(0,30)) +
  ylim(0, 2100) + 
  labs(
    x = "N Offspring born",
    y = "N Males",
    title = "Mean Male Lifetime Repro Success for Both Taxa")

library(ggplot2)

limits <- aes(ymax = ULCI, ymin = LLCI)

labels <- 

p <- ggplot(both_taxa_sire, 
            aes(x=factor(Offspring), y=MeanMales, fill=factor(Taxa)))
p + geom_bar(stat="identity", position = "dodge") + 
  scale_x_discrete(limits = c("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", 
                              "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                              "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"), labels = c("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", 
     
                                                                             "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                                                                                "21", "22", "23", "24", "25", "26", "27", "28", "29", "30")) +
  geom_errorbar(limits, width = 0, position = position_dodge(width = 0.9)) +
  theme(panel.background = element_rect(fill = "white"), 
        axis.text = element_text(size = 12), 
        panel.grid.major = element_line(color = "gray90"),
        panel.grid.minor.y = element_line(color = "gray90"),
        panel.grid.minor.x = element_line(color = "white"),
        panel.border = element_rect(color = "black", size = 1, fill = NA),
        plot.title = element_text(size = rel(2)),
        axis.title.y = element_text(size = rel(1.5)),
        axis.title.x = element_text(size = rel(1.5))) +
  scale_fill_manual(values = c("#C56E39", "#558ED5")) +
  labs(
    x = "N Offspring born",
    y = "N Males",
    title = "Mean Male Lifetime Repro Success for Both Taxa",
    fill = "Taxon"
  )

loglimits <- aes(ymax = log(ULCI), ymin = log(LLCI))

p <- ggplot(both_taxa_sire, 
            aes(x=factor(Offspring), y=log(MeanMales), fill=factor(Taxa)))
p + geom_bar(stat="identity", position = "dodge") + 
  scale_x_discrete(limits = c("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", 
                              "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                              "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"), labels = c("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", 
                                                                                                      
                                                                                                      "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                                                                                                      "21", "22", "23", "24", "25", "26", "27", "28", "29", "30")) +
  scale_y_continuous(limits = c(0, 8)) +
  geom_errorbar(loglimits, width = 0, position = position_dodge(width = 0.9)) +
  theme(panel.background = element_rect(fill = "white"), 
        axis.text = element_text(size = 12), 
        panel.grid.major = element_line(color = "gray90"),
        panel.grid.minor.y = element_line(color = "gray90"),
        panel.grid.minor.x = element_line(color = "white"),
        panel.border = element_rect(color = "black", size = 1, fill = NA),
        plot.title = element_text(size = rel(2)),
        axis.title.y = element_text(size = rel(1.5)),
        axis.title.x = element_text(size = rel(1.5))) +
  scale_fill_manual(values = c("#C56E39", "#558ED5")) +
  labs(
    x = "N Offspring born",
    y = "log(N Males)",
    title = "Log Mean Male Lifetime Repro Success for Both Taxa",
    fill = "Taxon"
  )

alberts2006 <- data.frame("Offspring" = c(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 16), 
                          "Males" = c(50, 14, 13, 4, 5, 4, 4, 1, 2, 3, 1, 1, 1))

library(ggplot2)
p <- ggplot(alberts2006, 
            aes(x=factor(Offspring), y=Males))
p + geom_bar(stat="identity", position = "dodge", fill = "dodgerblue2") +
  theme(panel.background = element_rect(fill = "white"), 
        axis.text = element_text(size = 12), 
        panel.grid.major = element_line(color = "gray90"),
        panel.grid.minor.y = element_line(color = "gray90"),
        panel.grid.minor.x = element_line(color = "white"),
        panel.border = element_rect(color = "black", size = 1, fill = NA),
        plot.title = element_text(size = rel(1.75)),
        axis.title.y = element_text(size = rel(1.5)),
        axis.title.x = element_text(size = rel(1.5))) +
  labs(
    x = "N Offspring born",
    y = "N Males",
    title = "12 Years of Paternity Data at  Amboseli, Alberts et al. 2006 ",
    fill = "Taxon"
  )
alberts.nls <- nls(Males ~ a * exp(b * Offspring), data=alberts2006, 
                   start = list(a=50, b=-2))
summary(alberts.nls)


library(easynls)
nlsplot(sav.df.sire.rotated, model=6)
savanna <- nlsfit(sav.df.sire.rotated, model=6)
nlsplot(hama.df.sire.rotated, model = 6)
hamadryas <- nlsfit(hama.df.sire.rotated, model = 6)

sav.nls <- nls(N_Males~a * exp(b * N_Offspring), 
               data=sav.df.sire.rotated,
               start = list(a=400, b=-2))

summary(sav.nls)

hama.nls <- nls(N_Males~a * exp(b * N_Offspring), 
                data=hama.df.sire.rotated,
                start = list(a=400, b=-2))
summary(hama.nls)

anova(sav.nls, hama.nls)

library(ggplot2)

multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
  library(grid)
  
  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)
  
  numPlots = length(plots)
  
  # If layout is NULL, then use 'cols' to determine layout
  if (is.null(layout)) {
    # Make the panel
    # ncol: Number of columns of plots
    # nrow: Number of rows needed, calculated from # of cols
    layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                     ncol = cols, nrow = ceiling(numPlots/cols))
  }
  
  if (numPlots==1) {
    print(plots[[1]])
    
  } else {
    # Set up the page
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))
    
    # Make each plot, in the correct location
    for (i in 1:numPlots) {
      # Get the i,j matrix positions of the regions that contain this subplot
      matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))
      
      print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                      layout.pos.col = matchidx$col))
    }
  }
}


library(ggplot2)
p1 <- ggplot(data = data.frame(X = c("A", "B", "C"), Y = c(90, 5, 5)), 
             aes(x=factor(X), y=Y)) + 
  geom_bar(stat="identity", color = "grey25") + scale_y_continuous(expand = c(0,0), limits = c(0, 100)) +
  theme(panel.background = element_rect(fill = "white"), 
        axis.text = element_text(size = 10), 
        panel.grid = element_line(color = "white"),
        panel.border = element_rect(color = "black", size = 1, fill = NA),
        plot.title = element_text(size = rel(1)),
        axis.title.y = element_text(size = rel(.9)),
        axis.title.x = element_text(size = rel(.9))) +
  labs(
    x = "Males",
    y = "% reproduction obtained",
    title = "High Reproductive Skew"
  )
  
p2 <- ggplot(data = data.frame(X = 0:20, Y = c(90, 30, 18, 11, 6, 5, 4,3,3,3,3,3,3,3,3,3,3,3,3,3,3)), 
             aes(x = X, y = Y)) + 
  geom_line(color = "grey25", size = 1.5) + scale_y_continuous(breaks = NULL, expand = c(0,0), limits = c(0, 100)) + scale_x_continuous(breaks = NULL, expand = c(0,0)) +
  theme(panel.background = element_rect(fill = "white"), 
        axis.text = element_blank(), 
        panel.grid = element_line(color = "white"),
        panel.border = element_rect(color = "black", size = 1, fill = NA),
        plot.title = element_text(size = rel(1)),
        axis.title.y = element_text(size = rel(.9)),
        axis.title.x = element_text(size = rel(.9))) +
  labs(
    x = "N Offspring",
    y = "N Males",
    title = "High Variance in LRS"
  )
  



  
p4 <- ggplot(data = data.frame(X=0:17, Y = c(50, 47, 44, 41, 38, 35, 32, 29, 26, 23, 20, 17, 14, 11, 8, 5, 2, 0)), 
             aes(x=X, y=Y)) + 
  geom_line(color = "grey25", size = 1.5) + scale_y_continuous(breaks = NULL, limits = c(0, 100), expand = c(0,0)) + scale_x_continuous(breaks = NULL, expand = c(0,0), limits = c(0, 20)) +
  theme(panel.background = element_rect(fill = "white"), 
        axis.text = element_blank(), 
        panel.grid = element_line(color = "white"),
        panel.border = element_rect(color = "black", size = 1, fill = NA),
        plot.title = element_text(size = rel(1)),
        axis.title.y = element_text(size = rel(.9)),
        axis.title.x = element_text(size = rel(.9))) +
  labs(
    x = "N Offspring",
    y = "N Males",
    title = "Low Variance in LRS"
  )

# p3 <- multiplot(p3, p3, p3)

takeover.df <- data.frame(X = c("A", "B", "C", "B", "C", "A", "C", "B", "A"), 
                          Y = rep(times = 3, x = c(90, 5, 5)), 
                          Alpha = c("A","A","A","B","B","B","C","C","C"))

p3 <- ggplot(data = takeover.df, 
             aes(x=factor(X), y=Y)) + 
  geom_bar(stat="identity") + scale_y_continuous(breaks = c(0, 100), expand = c(0,0), limits = c(0, 110)) +
  facet_grid(Alpha ~ .) +
  theme(panel.background = element_rect(fill = "white"), 
        strip.background = element_blank(),
        strip.text = element_text(c("2003-2007", "2007-2008", "2009-2013")), 
        axis.text = element_text(size = 10), 
        panel.grid = element_line(color = "white"),
        panel.border = element_rect(color = "black", size = 1, fill = NA),
        plot.title = element_text(size = rel(1)),
        axis.title.y = element_text(size = rel(.9)),
        axis.title.x = element_text(size = rel(.9))) +
  labs(
    x = "Males",
    y = "% reproduction obtained",
    title = "High Reproductive Skew"
  )


multiplot(p1, p2, p3, p4, cols=2)

library(reshape2)

hama_rhp <- melt(hama_rhp, id.vars = "Age")

colnames(sav_rhp) <- c("Age", "Type1", "Type2", "Type3", "Type4", "Type5")
sav_rhp <- sav_rhp[-1,]

sav_rhp <- melt(sav_rhp, id.vars = "Age")
sav_rhp$Age <- as.numeric(as.character(sav_rhp$Age))
sav_rhp$value <- as.numeric(as.character(sav_rhp$value))
add <- data.frame(Age = c(rep(5.0, 5), rep(5.5, 5), rep(6.0, 5), rep(6.5, 5)), 
                  variable = rep(c("Type1", "Type2", "Type3", "Type4", "Type5"), 4), 
                  value = rep(0.0, 20))
sav_rhp <- rbind(sav_rhp, add)


library(ggplot2)
rhp1 <- ggplot(data = hama_rhp, aes(x = Age, y = value, group = variable, colour = variable)) + geom_line(size = 1.5) + 
  scale_color_manual(values = c("#C56E39",  "#fd8d3c", "#d94701","#fdbe85")) +
  scale_y_continuous(limits = c(0, 110), expand = c(0,0)) + 
  scale_x_continuous(expand = c(0,0), limits = c(5, 21)) +
  theme(panel.background = element_rect(fill = "white"), 
        panel.grid = element_line(color = "white"),
        panel.border = element_rect(color = "black", size = 1, fill = NA),
        plot.title = element_text(size = rel(2)),
        axis.title.y = element_text(size = rel(1.5)),
        axis.title.x = element_text(size = rel(1.5)),
        axis.text = element_text(size = rel(1)),
        legend.position = "none") +
  labs(
    x = "Age in years",
    y = "Resource holding potential score",
    title = "A.    Hamadryas RHP Curves"
  )



rhp2 <- ggplot(data = sav_rhp, aes(x = Age, y = value, group = variable, colour = variable)) + geom_line(size = 1.5) + 
  scale_color_manual(values = c("#045a8d", "#2b8cbe", "#74a9cf", "#a6bddb", "#d0d1e6")) +
  scale_y_continuous(limits = c(0, 110), expand = c(0,0)) + 
  scale_x_continuous(expand = c(0,0), limits = c(5, 21)) +
  theme(panel.background = element_rect(fill = "white"), 
        panel.grid = element_line(color = "white"),
        panel.border = element_rect(color = "black", size = 1, fill = NA),
        plot.title = element_text(size = rel(2)),
        axis.title.y = element_text(size = rel(1.5)),
        axis.title.x = element_text(size = rel(1.5)),
        axis.text = element_text(size = rel(1)),
        legend.position = "none") +
  labs(
    x = "Age in years",
    y = "Resource holding potential score",
    title = "B.      Savanna RHP Curves"
  )

multiplot(rhp1, rhp2, cols=2)

