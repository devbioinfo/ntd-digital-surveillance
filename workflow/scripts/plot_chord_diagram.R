# Load library
library(circlize)

# Read data
df <- read.csv("output/figures/ntd_platform_keywords.csv")

# Optionally adjust spelling consistency
df$Target <- gsub("kala[ -]?azar", "Kala-azar", df$Target, ignore.case = TRUE)

# Set colors
grid_colors <- c(
  "YouTube" = "#1f77b4",
  "Google News" = "#ff7f0e",
  "Dengue" = "#2ca02c",
  "Chikungunya" = "#d62728",
  "Filariasis" = "#9467bd",
  "Kala-azar" = "#8c564b"
)

# PNG output
png("output/figures/ntd_chord_diagram.png", width=1200, height=1200, res=300)

# PNG output
png("output/figures/ntd_chord_diagram.png", width=1200, height=1200, res=300)

# Draw chord diagram
chordDiagram(
  df,
  grid.col = grid_colors,
  transparency = 0.2,
  annotationTrack = c("grid", "name"),
  preAllocateTracks = list(track.height = 0.1)
)

# Title with smaller font
title("Cross-Platform Mentions of NTDs (YouTube and Google News)", cex.main=0.8)

dev.off()

