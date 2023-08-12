import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.stats import t

concentrations = [0.0025, 0.005, 0.0075, 0.01, 0.02, 0.03, 0.04, 0.05]
conductivites = [0.098028913, 0.13348776, 0.165816804, 0.208447468, 0.351272239, 0.582802454, 0.753164069, 0.948385096]


def prediction(gradient,
               value,
               intercept):
    return gradient * value + intercept


def determine_molarity_for_conductivity(desired_conductivity,
                                        gradient,
                                        intercept,
                                        ):
    return (desired_conductivity - intercept) / gradient


if __name__ == "__main__":
    fit = stats.linregress(concentrations, conductivites)

    t = abs(t.ppf(0.025, len(concentrations) - 2))

    plt.xlabel("[NaCL] in M")
    plt.ylabel("conductivity in S/m")

    plt.scatter(concentrations[0], conductivites[0], color='black', label="conductivity measurements")
    for i in range(1, len(conductivites)):
        plt.scatter(concentrations[i], conductivites[i], color='black')

    plt.plot(np.array(concentrations),
             prediction(gradient=fit.slope, value=np.array(concentrations), intercept=fit.intercept), color='blue',
             label="linear regression line")

    plt.plot(np.array(concentrations),
             prediction(gradient=fit.slope + t * fit.stderr, value=np.array(concentrations),
                        intercept=fit.intercept + t * fit.intercept_stderr), color='grey', linestyle="dotted",
             label="confidence interval regression lines")

    plt.plot(np.array(concentrations),
             prediction(gradient=fit.slope - t * fit.stderr, value=np.array(concentrations),
                        intercept=fit.intercept - t * fit.intercept_stderr), color='grey', linestyle="dotted")

    x1 = prediction(gradient=fit.slope + t * fit.stderr, value=np.array(concentrations),
                    intercept=fit.intercept + t * fit.intercept_stderr)

    x2 = prediction(gradient=fit.slope - t * fit.stderr, value=np.array(concentrations),
                    intercept=fit.intercept - t * fit.intercept_stderr)

    plt.fill_between(np.array(concentrations), x1, x2, color="grey", alpha=0.3)
    plt.legend()

    with open("fitted_conductivities.txt", "w") as file:
        file.write("lin regress results = " + str(fit) + "\n")

        file.write("Confidence interval slope = " + str(fit.slope) + "+/-" + str(t * fit.stderr) + "\n")
        file.write(
            "Confidence interval intercept = " + str(fit.intercept) + "+/-" + str(t * fit.intercept_stderr) + "\n")

        file.write("molarity to achieve a conductivity of 0.30603 S/m:" + str(
            determine_molarity_for_conductivity(0.30603, gradient=fit.slope, intercept=fit.intercept)) + "M" + "\n")

        file.write(
            "molarity to achieve a conductivity of 0.30603 S/m with lower bound confidence interval parameters:" + str(
                determine_molarity_for_conductivity(0.30603, gradient=fit.slope - t * fit.stderr,
                                                    intercept=fit.intercept - t * fit.intercept_stderr)) + "M" + "\n")

        file.write(
            "molarity to achieve a conductivity of 0.30603 S/m with upper bound confidence interval parameters:" + str(
                determine_molarity_for_conductivity(0.30603, gradient=fit.slope + t * fit.stderr,
                                                    intercept=fit.intercept + t * fit.intercept_stderr)) + "M" + "\n")

    plt.savefig("fitted_conductivities.svg")
