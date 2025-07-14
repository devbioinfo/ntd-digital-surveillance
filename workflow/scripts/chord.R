install.packages("circlize")
library(circlize)

# Example data:
mat <- matrix(c(
  300, 500, 90, 4,
  650, 150, 80, 15
), nrow=2, byrow=TRUE)
rownames(mat) <- c("YouTube", "Google News")
colnames(mat) <- c("dengue", "filariasis", "chikungunya", "kala-azar")

chordDiagram(mat, transparency=0.2, grid.col=c("dodgerblue","orangered","limegreen","goldenrod","gray30","purple"))
