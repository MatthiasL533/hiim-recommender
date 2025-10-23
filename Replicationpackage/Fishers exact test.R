dat <- data.frame(
  "Correct" = c(4, 10),
  "Wrong" = c(1, 5),
  row.names = c("AI", "Humans"),
  stringsAsFactors = FALSE
)
colnames(dat) <- c("AI", "Humans")

dat

mosaicplot(dat,
           main = "Mosaic plot",
           color = TRUE
)

chisq.test(dat)$expected

test <- fisher.test(dat)
test