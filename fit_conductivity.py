import matplotlib.pyplot as plt
from scipy import stats


concentrations = [0.0025,	0.005,	0.0075,	0.01,	0.02,	0.03,	0.04,	0.05]
conductivites = [0.098028913,	0.13348776,	0.165816804,	0.208447468,	0.351272239,	0.582802454,	0.753164069,	0.948385096]


#plt.plot(concentrations, conductivites, color='black')
plt.xlabel("[NaCL] in M")
plt.ylabel("conductivity in S/m")
for i in range (len(conductivites)):
    plt.scatter(concentrations[i], conductivites[i], color='black')
plt.show()
