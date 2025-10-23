# Scores voor de willekeurige methodes (random)
random <- c(
  1.83, 1.67, 2.50, 3.67, 2.00, 2.83, 1.00, 1.00, 2.33, 2.17,
  1.67, 1.00, 2.83, 3.17, 1.17, 2.83, 1.50, 1.67, 2.83, 2.50
)

# Scores voor de LLM-aanbevelingen (average LLM recs)
LLM_recs <- c(
  3.33, 3.50, 3.17, 1.00, 2.67, 1.67, 1.50, 2.67, 3.50, 3.50,
  3.83, 3.50, 4.00, 2.83, 2.67, 2.00, 3.17, 3.50, 3.17, 3.00,
  3.67, 3.50, 3.33, 3.50, 3.67, 3.50, 2.50, 2.33, 3.67, 3.50
)

# Omdat de random-reeks 20 waarden heeft en LLM_recs 30,
# moeten we ze even lang maken om de Wilcoxon-test te doen.
# We nemen de eerste 20 LLM-scores, zodat beide vectoren lengte 20 hebben:
LLM_recs_20 <- LLM_recs[1:20]

# Wilcoxon signed-rank test (alternatief = "greater" betekent dat we testen of LLM > random)
result <- wilcox.test(LLM_recs_20, random, paired = TRUE, alternative = "greater")

# Resultaat tonen
print(result)