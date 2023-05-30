import pandas as pd
from scipy import stats
from statsmodels.stats.anova import AnovaRM

number_of_anovas = 1

def post_hoc_test_RM_bonferroni(group_one: str, group_two: str, nr_of_comparisons: int, alpha: float):
    level_of_significance = alpha / nr_of_comparisons
    post_hoc_result = stats.ttest_rel(assumptions[group_one], assumptions[group_two])
    is_significant = post_hoc_result[1] < level_of_significance
    print(group_one + " vs. " + group_two+ ": " + str(post_hoc_result) +
          " |  is significant with level " + str(level_of_significance) + ": " + str(is_significant))
    print("\n")


df = pd.read_csv("C:\\Users\\Chris\\OneDrive\\Desktop\\stats_playground_agar.csv")
assumptions = pd.read_csv("C:\\Users\\Chris\\OneDrive\\Desktop\\stats_playground_visualization.csv")
print("Descriptive statistics: ")
print(assumptions.describe())
print("\n\n")

print("Testing the assumptions:")
print("Testing normal distribution of the samples: ")
shapiro_test_ahistoric = stats.shapiro(assumptions["ahistoric"])
print("shapiro test for ahistoric: " + str(shapiro_test_ahistoric ))
shapiro_test_sliding_dtw = stats.shapiro(assumptions["sliding_dtw"])
print("shapiro test for sliding_dtw: " + str(shapiro_test_sliding_dtw))
shapiro_test_displacement = stats.shapiro(assumptions["displacement"])
print("shapiro test for displacement: " + str(shapiro_test_displacement))
shapiro_test_alpha_displacement = stats.shapiro(assumptions["alpha_displacement"])
print("shapiro test for alpha_displacement: " + str(shapiro_test_alpha_displacement ))
print("\n")

print("testing homogeneity of variance of the four groups: ")
levene = stats.levene(assumptions["ahistoric"], assumptions["sliding_dtw"], assumptions["displacement"], assumptions["alpha_displacement"])
print(levene)



print("\nConduction the repeated measures anova for the four samples: ")
anovaRM = AnovaRM(data=df, depvar="rms", subject="sample", within=["measurement"]).fit()
print(anovaRM)
if anovaRM.anova_table["Pr > F"][0] < 0.05/number_of_anovas:
    print("ANOVA was significant with level of significance" + str(0.05/number_of_anovas))
    # Bonferroni corrected post hoc significance level


    print("\nConduction the poshoc tests as related-sample t-tests with bonferroni corrected p-value: ")
    for i in range(len(assumptions.columns)-1):
        for j in range(i, len(assumptions.columns)):
            post_hoc_test_RM_bonferroni(assumptions.columns[i], assumptions.columns[j], 6, 0.05)

