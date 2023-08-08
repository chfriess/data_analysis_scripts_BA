import pandas as pd
from matplotlib import pyplot as plt
from scipy import stats
from statsmodels.stats.anova import AnovaRM


def post_hoc_test_RM_bonferroni(group_one: str, group_two: str, nr_of_comparisons: int, alpha: float):
    level_of_significance = alpha / nr_of_comparisons
    post_hoc_result = stats.ttest_rel(df_post_hoc[group_one], df_post_hoc[group_two])
    is_significant = post_hoc_result[1] < level_of_significance
    return str(group_one + " vs. " + group_two + ": " + str(post_hoc_result) +
               " |  is significant with level " + str(level_of_significance) + ": " + str(is_significant) + "\n")


PATH = ""  # ENTER SOURCE PATH BEGINNING

df_anova = pd.read_csv(PATH + "statistics_for_AnovaRM.csv")
df_post_hoc = pd.read_csv(PATH + "statistics_for_post_hoc_tests.csv")
DESTINATION = PATH
df_post_hoc.boxplot(fontsize=9)
plt.ylabel("rms-deviation from groundtruth [mm]", fontsize=9)
plt.savefig(DESTINATION + "boxplot.svg")

with open(DESTINATION + "statistical_evaluation.txt", 'w') as f:
    f.write("Descriptive statistics: ")
    f.write(str(df_post_hoc.describe()))
    f.write("\n\n")

    f.write("Testing the assumptions:")
    f.write("Testing normal distribution of the samples: ")
    shapiro_test_ahistoric = stats.shapiro(df_post_hoc["ahistoric"])
    f.write("\nshapiro test for ahistoric: " + str(shapiro_test_ahistoric))
    shapiro_test_sliding_dtw = stats.shapiro(df_post_hoc["sliding_dtw"])
    f.write("\nshapiro test for sliding_dtw: " + str(shapiro_test_sliding_dtw))
    shapiro_test_displacement = stats.shapiro(df_post_hoc["displacement"])
    f.write("\nshapiro test for displacement: " + str(shapiro_test_displacement))
    shapiro_test_alpha_displacement = stats.shapiro(df_post_hoc["alpha_displacement"])
    f.write("\nshapiro test for alpha_displacement: " + str(shapiro_test_alpha_displacement))
    f.write("\n")

    f.write("testing homogeneity of variance of the four groups: ")
    levene = stats.levene(df_post_hoc["ahistoric"], df_post_hoc["sliding_dtw"], df_post_hoc["displacement"],
                          df_post_hoc["alpha_displacement"])
    f.write(str(levene))

    f.write("\nConduction the repeated measures anova for the four samples: ")
    anovaRM = AnovaRM(data=df_anova, depvar="rms", subject="sample", within=["measurement"]).fit()
    f.write(str(anovaRM))
    if anovaRM.anova_table["Pr > F"][0] < 0.05:
        f.write("ANOVA was significant with level of significance" + str(0.05))
        # Bonferroni corrected post hoc significance level

        f.write("\nConduction the poshoc tests as related-sample t-tests with bonferroni corrected p-value: \n")
        for i in range(len(df_post_hoc.columns) - 1):
            for j in range(i, len(df_post_hoc.columns)):
                if i != j:
                    f.write(post_hoc_test_RM_bonferroni(df_post_hoc.columns[i], df_post_hoc.columns[j], 6, 0.05))

plt.clf()
