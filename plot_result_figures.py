import json
import math
import statistics

import numpy as np
from matplotlib import pyplot as plt

REF_PATH = ""  # ENTER REFERENCE PATH AS .npy FILE
IMP_PATH = ""  # ENTER IMPEDANCE PATH AS .npy FILE
GRTRUTH_PATH = ""  # ENTER GROUNDTRUTH PATH AS .npy FILE

BASE_PATH = ""

FILENAME = ""  # ENTER FILE NR


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

posest = np.load(BASE_PATH + "best cluster means " + FILENAME + ".npy")
err = np.load(BASE_PATH + "best cluster variances " + FILENAME + ".npy")

posest_2 = np.load(BASE_PATH + "second best cluster means " + FILENAME + ".npy")
err_2 = np.load(BASE_PATH + "second best cluster variances " + FILENAME + ".npy")

x = [p * 0.0806 for p in range(len(grtruth))]
# x = list(np.array(x) * 0.0806)
y = [l * 0.0806 for l in range(len(posest))]
# y = list(np.array(y) * 0.0806)

fig, ax = plt.subplots()

ax.plot(x, grtruth, color="black", label="groundtruth")
ax.plot(y, posest, color="blue", label="first cluster")
ax.errorbar(y, posest, yerr=err, ls="None", color="blue", capsize=2, elinewidth=0.5, capthick=0.5)
ax.scatter(y, posest, color="blue", s=2)

ax.plot(y, posest_2, color="green", label="second cluster")
ax.errorbar(y, posest_2, yerr=err_2, ls="None", color="green", capsize=2, elinewidth=0.5, capthick=0.5)
ax.scatter(y, posest_2, color="green", s=2)

plt.legend()

ax.set_xlabel("time [s] ")
ax.set_ylabel("displacement along centerline [mm]")

z = [l * 0.0806 for l in range(len(impedance))]
a = [l * 0.0806 for l in range(len(ref_at_grtruth))]

ax2 = ax.twinx()
ax2.plot(z, impedance, color="#fabda6", label="impedance", alpha=0.5)
ax2.plot(a, ref_at_grtruth, color="#35177a", label="reference", alpha=0.5)
ax2.set_ylabel("z-value")

plt.legend()
plt.savefig(BASE_PATH + "groundtruth vs. pf estimate new.svg")

plt.figure(1)
alphas = np.load(BASE_PATH + "alpha estimates " + FILENAME + ".npy")
fig2, ax3 = plt.subplots()

ax3.plot(z, impedance, color="#fabda6", label="impedance")
ax3.plot(a, ref_at_grtruth, color="#35177a", label="reference")
ax3.set_xlabel("time [s] ")
ax3.set_ylabel("z-value")
plt.legend(loc='upper left')

ax4 = ax3.twinx()
ax4.plot(y, alphas, color="green", label="alpha")
ax4.set_ylabel("alpha")
plt.legend(loc='upper right')
plt.savefig(BASE_PATH + "alpha per update step new.svg")

plt.clf()
