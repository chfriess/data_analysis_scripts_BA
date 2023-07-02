import json
import math
import statistics

import numpy as np
from matplotlib import pyplot as plt



"""
REF_PATH = "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom_data_testing" + "reference_from_iliaca.npy"
IMP_PATH = "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom_data_testing\\sample_" + sample_nr \
           + "\\data_sample_" + sample_nr + "\\impedance_from_iliaca.npy"
GRTRUTH_PATH = "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom_data_testing\\sample_" + sample_nr + \
                                               "\\data_sample_" + sample_nr + "\\groundtruth_from_iliaca.npy"

BASE_PATH = PATH + "sample_" + sample_nr + "\\" + str(measurement_model) + "\\"
"""

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







grtruth = np.load(GRTRUTH_PATH)
grtruth = grtruth[1:]
kernel_size = 10
kernel = np.ones(kernel_size) / kernel_size

impedance = np.load(IMP_PATH)
ref_at_grtruth = []
if REF_PATH.endswith('.json'):
    with open(REF_PATH, "r") as infile:
        map_to_read = json.load(infile)
        vessel = map_to_read['signal_per_centerline_position']

        for el in grtruth:
            if el <= vessel[0]["centerline_position"]:
                ref_at_grtruth.append(vessel[0]["reference_signal"])
            elif el >= vessel[-1]["centerline_position"]:
                ref_at_grtruth.append(vessel[-1]["reference_signal"])
            else:
                index = 0
                while el > vessel[index]["centerline_position"]:
                    index += 1
                x = [vessel[index - 1]["centerline_position"], vessel[index]["centerline_position"]]
                y = [vessel[index - 1]["reference_signal"], vessel[index]["reference_signal"]]
                ref_at_grtruth.append(np.interp(el, x, y))


else:
    ref = np.load(REF_PATH)
    for el in grtruth:
        n = round(el)
        if n >= len(ref):
            n = len(ref) - 1
        ref_at_grtruth.append(ref[n])

posest = np.load(BASE_PATH + "best cluster means.npy")
err = np.load(BASE_PATH + "best cluster variances.npy")



posest_2 = np.load(BASE_PATH + "second best cluster means.npy")
err_2 = np.load(BASE_PATH + "second best cluster variances.npy")

x = [p for p in range(len(grtruth))]
x = list(np.array(x) * 0.23)
y = [l for l in range(len(posest))]
y = list(np.array(y) * 0.23)

fig, ax = plt.subplots()

ax.plot(x, grtruth, color="black", label="groundtruth")
ax.plot(y, posest, color="blue", label="first cluster")
ax.errorbar(y, posest, yerr=err, ls="None", color="blue", capsize=2, elinewidth=0.5, capthick=0.5)
ax.scatter(y, posest, color="blue", s=2)

ax.plot(y, posest_2, color="green", label="second cluster")
ax.errorbar(y, posest_2, yerr=err_2, ls="None", color="green", capsize=2, elinewidth=0.5, capthick=0.5)
ax.scatter(y, posest_2, color="green", s=2)

"""
bi_1 = 0
bi_2 = 0
bi_3 = 0
for i, el in enumerate(grtruth):
    if el >= 80:
        bi_1 = i
        break
for i, el in enumerate(grtruth):
    if el >= 116:
        bi_2 = i
        break

for i, el in enumerate(grtruth):
    if el >= 175:
        bi_3 = i
        break


ax.axvline(x = bi_1, color = 'purple', label="iliaka aorta")
ax.axvline(x = bi_2, color = 'r', label="middle branch")
ax.axvline(x = bi_3, color = 'g', label="renal branch")
"""

plt.legend()

ax.set_xlabel("time [s] ")
ax.set_ylabel("displacement along centerline [mm]")

#ax2 = ax.twinx()
#ax2.plot(impedance, color="#fabda6", label="impedance", alpha=0.5)
#ax2.plot(ref_at_grtruth, color="#35177a", label="reference", alpha=0.5)
#ax2.set_ylabel("z-value")

plt.legend()
#plt.show()
plt.savefig(BASE_PATH + "groundtruth vs. pf estimate new.svg")


plt.figure(1)
alphas = np.load(BASE_PATH + "alpha estimates.npy")
fig2, ax3 = plt.subplots()

z = [l for l in range(len(impedance))]
z = list(np.array(z) * 0.23)

a = [l for l in range(len(ref_at_grtruth))]
a = list(np.array(a) * 0.23)

ax3.plot(z, impedance, color="#fabda6", label="impedance")
ax3.plot(a, ref_at_grtruth, color="#35177a", label="reference")
ax3.set_xlabel("time [s] ")
ax3.set_ylabel("z-value")
plt.legend(loc='upper left')

ax4 = ax3.twinx()
ax4.plot(y, alphas, color="green", label="alpha")
ax4.set_ylabel("alpha")
plt.legend(loc='upper right')
#plt.show()
plt.savefig(BASE_PATH + "alpha per update step new.svg")



plt.clf()