# Deskriptiv statistik for sample label data

# Indlæser data
library(tidyverse)
df <- read.csv("labeling_info_trial.csv", sep = ";", header = TRUE)
df_filt <- na.omit(df)
df_filt <- df_filt[,2:5 ]

# Create a new dataframe for plotting
df_points <- data.frame(
  x = c(df_filt$X1, df_filt$X2),
  y = c(df_filt$Y1, df_filt$Y2),
  type = rep(c("(X1,Y1)", "(X2,Y2)"), each = nrow(df_filt))
)

# Plot using ggplot2
ggplot(df_points, aes(x = x, y = y, color = type)) +
  geom_point(size = 3) +
  labs(title = "Label data plot",
       x = "X Coordinate",
       y = "Y Coordinate",
       color = "Point Type") +
  theme_minimal()