import statistics

import numpy as np
from matplotlib import pyplot as plt


def normalize_values(data) -> list:
    mu = statistics.mean(data)
    sigma = statistics.stdev(data)
    for i, el in enumerate(data):
        data[i] = (el - mu) / sigma
    return data


sample_nr = "25"

ref_path = "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom_data_testing\\" + "reference_from_iliaca.npy"
imp_path = "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom_data_testing\\sample_" + sample_nr + "\\data_sample_" + sample_nr + "\\impedance_interpolated_" + sample_nr + ".npy"
grtruth_path = "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom_data_testing\\sample_" + sample_nr + "\\data_sample_" + sample_nr + "\\em_interpolated_" + sample_nr + ".npy"

base_path = "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom_data_testing\\sample_" + sample_nr + "\\results_sample_" + sample_nr + "\\"
offset_groundtruth_bioelectric = 3
grtruth = np.load(grtruth_path)
grtruth = list(np.array(grtruth) + offset_groundtruth_bioelectric)

# TODO: invert signals for that kind of testing, currently only to test
offset = abs(280 - grtruth[-1])
groundtruth_inverted = grtruth[::-1]
for i, el in enumerate(groundtruth_inverted):
    grtruth[i] = abs(groundtruth_inverted[i] - groundtruth_inverted[0]) + offset

impedance = normalize_values(np.load(imp_path))
impedance = impedance[::-1]

ref = normalize_values(np.load(ref_path))

ref_at_gtruth = []

for el in grtruth:
    ref_at_gtruth.append(ref[round(el)])

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
