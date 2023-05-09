import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


concentrations = [0.0025,	0.005,	0.0075,	0.01,	0.02,	0.03,	0.04,	0.05]
conductivites = [0.098028913,	0.13348776,	0.165816804,	0.208447468,	0.351272239,	0.582802454,	0.753164069,	0.948385096]


#plt.plot(concentrations, conductivites, color='black')
plt.xlabel("[NaCL] in M")
plt.ylabel("conductivity in S/m")
for i in range(len(conductivites)):
    plt.scatter(concentrations[i], conductivites[i], color='black')

gradient, intercept, r_value, p_value, slope_std_error = stats.linregress(concentrations, conductivites)

predicted_conductivity = gradient * np.array(concentrations) + intercept
pred_error = np.array(conductivites) - predicted_conductivity
degrees_of_freedom = len(concentrations) - 2
residual_std_error = np.sqrt(np.sum(pred_error**2) / degrees_of_freedom)


def prediction (x):
    return gradient * x + intercept


def determine_molarity_for_conductivity(desired_conductivity: float) -> float:
    return (desired_conductivity-intercept)/gradient

plt.plot(np.array(concentrations), prediction(np.array(concentrations)), color='blue')

with open("C:\\Users\\Chris\\OneDrive\\Desktop\\fitted_conductivities.txt", "w") as file:

    file.write("residual error of fitting = " + str(residual_std_error) + "\n")
    file.write("m = " + str(gradient) + "\n")
    file.write("c = " + str(intercept) + "\n")
    file.write("molarity to achieve a conductivity of 0.30603 S/m:" + str(determine_molarity_for_conductivity(0.30603)) + "M" + "\n")

plt.savefig("C:\\Users\\Chris\\OneDrive\\Desktop\\fitted_conductivities.svg")
