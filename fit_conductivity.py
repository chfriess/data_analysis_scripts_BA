import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

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
    print(np.__version__)
    fit = stats.linregress(concentrations, conductivites)

    print(fit.intercept_stderr)

    plt.xlabel("[NaCL] in M")
    plt.ylabel("conductivity in S/m")
    for i in range(len(conductivites)):
        plt.scatter(concentrations[i], conductivites[i], color='black')
    plt.plot(np.array(concentrations),
             prediction(gradient=fit.slope, value=np.array(concentrations), intercept=fit.intercept), color='blue')

    with open("fitted_conductivities.txt", "w") as file:
        file.write("lin regress results = " + str(fit) + "\n")

        file.write("molarity to achieve a conductivity of 0.30603 S/m:" + str(
            determine_molarity_for_conductivity(0.30603, gradient=fit.slope, intercept=fit.intercept, )) + "M" + "\n")

    plt.savefig("fitted_conductivities.svg")
