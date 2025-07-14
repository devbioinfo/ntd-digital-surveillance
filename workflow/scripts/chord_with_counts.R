suppressPackageStartupMessages(library(circlize))

# Data frame
df <- data.frame(
  Source = c("YouTube", "YouTube", "YouTube", "Google News", "Google News", "Google News"),
  Target = c("dengue", "filariasis", "chikungunya", "dengue", "filariasis", "chikungunya"),
  Value = c(71, 68, 2, 102, 38, 44)
)

# Colors
grid.col <- c(
  "YouTube" = "#1f77b4",
  "Google News" = "#ff7f0e",
  "dengue" = "#e377c2",
  "filariasis" = "#1f3d7a",
  "chikungunya" = "#9467bd"
)

# Start PNG output
png("output/figures/ntd_chord_diagram.png", width=1200, height=1200, res=300)

# Create chord diagram
chordDiagram(
  df,
  grid.col = grid.col,
  transparency = 0.2,
  annotationTrack = "grid",
  preAllocateTracks = 1,
  directional = 1,
  direction.type = c("arrows", "diffHeight"),
  link.arr.type = "big.arrow",
  link.sort = TRUE,
  link.decreasing = TRUE
)

# Add sector labels
circos.trackPlotRegion(
  track.index = 1,
  panel.fun = function(x, y) {
    sector.name = get.cell.meta.data("sector.index")
    xlim = get.cell.meta.data("xlim")
    ylim = get.cell.meta.data("ylim")
    circos.text(
      mean(xlim),
      ylim[1] + 0.1,
      sector.name,
      facing = "clockwise",
      niceFacing = TRUE,
      adj = c(0, 0.5),
      cex = 0.7
    )
  },
  bg.border = NA
)

# Title and caption
title("Cross-Platform Mentions of NTDs (YouTube and Google News)", cex.main=0.7, line=-1)
mtext("Data from Jan 2019 - Dec 2023", side=1, line=2, cex=0.8, adj=1)


# Close PNG device
dev.off()
