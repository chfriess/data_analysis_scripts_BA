import math
import statistics

import numpy as np
from matplotlib import pyplot as plt



def predict_impedance_from_diameter(diameter):
    # expects diameter in mm, converts it to m
    diameter = diameter / 1000
    circumference = diameter * math.pi
    csa = ((diameter / 2) ** 2) * math.pi
    sensor_distance = 3 / 1000
    tissue_conductivity = 0.30709
    blood_conductivity = 0.7
    return 1000 * ((csa * blood_conductivity) / sensor_distance + tissue_conductivity * circumference) ** (-1)


def calculate_csa(diameter):
    return (diameter / 2) ** 2 * math.pi


def normalize_values(data) -> list:
    mu = statistics.mean(data)
    sigma = statistics.stdev(data)
    for i, el in enumerate(data):
        data[i] = (el - mu) / sigma
    return data


sample_nr = "44"

"""
ref_path = "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom_data_testing\\" + "reference_from_iliaca.npy"
imp_path = "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom_data_testing\\sample_" + sample_nr + "\\data_sample_" + sample_nr + "\\impedance_interpolated_" + sample_nr + ".npy"
grtruth_path = "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom_data_testing\\sample_" + sample_nr + "\\data_sample_" + sample_nr + "\\em_interpolated_" + sample_nr + ".npy"

base_path = "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom_data_testing\\sample_" + sample_nr + "\\results_sample_" + sample_nr + "\\"
"""
base_path = "C:\\Users\\Chris\\OneDrive\\Desktop\\plastic coregistration data\\04_06_2023_BS\\coregistration_" + sample_nr + "\\results_sample_" + sample_nr + "\\"

ref_path = "C:\\Users\\Chris\\OneDrive\\Desktop\\plastic coregistration data\\04_06_2023_BS\\" + "diameters_for_plastic_from_iliaca.npy"
imp_path = "C:\\Users\\Chris\\OneDrive\\Desktop\\plastic coregistration data\\04_06_2023_BS\\coregistration_" + sample_nr + "\\data_bioelectric_sensors" + "\\impedance_from_iliaca.npy"
grtruth_path = "C:\\Users\\Chris\\OneDrive\\Desktop\\plastic coregistration data\\04_06_2023_BS\\coregistration_" + sample_nr + "\\data_bioelectric_sensors" + "\\groundtruth_shifted_from_iliaca.npy"

offset_groundtruth_bioelectric = -3
grtruth = np.load(grtruth_path)
grtruth = list(np.array(grtruth) + offset_groundtruth_bioelectric)
kernel_size = 10
kernel = np.ones(kernel_size) / kernel_size

impedance_raw = np.load(imp_path)
# impedance = normalize_values(impedance_raw)
impedance = impedance_raw
ref_raw = np.load(ref_path)

ref = np.array([predict_impedance_from_diameter(x) for x in ref_raw])


ref = np.convolve(ref, kernel, mode='same')

ref_at_gtruth = []

for el in grtruth:
    n = round(el)
    if n >= len(ref):
        n = len(ref) - 1
    ref_at_gtruth.append(ref[n])

posest = np.load(base_path + "best cluster means.npy")
err = np.load(base_path + "best cluster variances.npy")

posest_2 = np.load(base_path + "second best cluster means.npy")
err_2 = np.load(base_path + "second best cluster variances.npy")

x = [p for p in range(len(grtruth))]
y = [l for l in range(len(posest))]

fig, ax = plt.subplots()

ax.plot(x, grtruth, color="black", label="groundtruth")
ax.plot(y, posest, color="blue", label="first cluster")
ax.errorbar(y, posest, yerr=err, ls="None", color="blue", capsize=2, elinewidth=0.5, capthick=0.5)
ax.scatter(y, posest, color="blue", s=2)

ax.plot(y, posest_2, color="green", label="second cluster")
ax.errorbar(y, posest_2, yerr=err_2, ls="None", color="green", capsize=2, elinewidth=0.5, capthick=0.5)
ax.scatter(y, posest_2, color="green", s=2)
plt.legend()

ax.set_xlabel("update steps ")
ax.set_ylabel("displacement along centerline [mm]")

ax2 = ax.twinx()
ax2.plot(impedance, color="#fabda6", label="impedance", alpha=0.5)
ax2.plot(ref_at_gtruth, color="#35177a", label="reference", alpha=0.5)
ax2.set_ylabel("z-value")

plt.legend()
plt.show()
# plt.savefig("groundtruth vs. pf estimate.svg")


plt.figure(1)
alphas = np.load(base_path + "alpha estimates.npy")
fig2, ax3 = plt.subplots()
ax3.plot(impedance, color="#fabda6", label="impedance")
ax3.set_xlabel("update steps ")
ax3.set_ylabel("z-value")

ax4 = ax3.twinx()
ax4.plot(alphas, color="green", label="alpha")
ax4.set_ylabel("alpha")
plt.legend()
plt.show()
