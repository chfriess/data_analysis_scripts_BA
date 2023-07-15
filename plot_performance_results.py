import pickle

import numpy as np
from matplotlib import pyplot as plt

TYPE = "ERRORS"

fig, ax = plt.subplots()

models = ["AHISTORIC", "SLIDING_DTW"]
colors = ["black", "blue"]
for i in range(2):

    destination_path = "C:\\Users\\Chris\\OneDrive\\Desktop\\result_tilt_side_old\\performance\\" + models[i] + "\\"

    if TYPE == "EXECTIME":
        average_performance = pickle.load(open("C:\\Users\\Chris\\OneDrive\\Desktop\\result_tilt_side_old\\performance\\" + models[
            i] + "\\performance per particle number.pkl", 'rb'))
        stdev_performance = np.load(destination_path + "stdev performance per particle number.npy")

        ax.scatter(average_performance.keys(), average_performance.values(), color=colors[i])
        ax.plot(average_performance.keys(), average_performance.values(), color=colors[i], label=models[i])
        ax.errorbar(average_performance.keys(), average_performance.values(), yerr=stdev_performance, ls="None",
                    color=colors[i], capsize=2, elinewidth=0.5, capthick=0.5)
        ax.set_ylabel("average time per execution step [s]")
        ax.set_xlabel("number of particles")
        plt.title("Average execution time of update step")
    elif TYPE == "ERRORS":
        average_error = pickle.load(open(
            "C:\\Users\\Chris\\OneDrive\\Desktop\\result_tilt_side_old\\performance\\" + models[i] + "\\errors per particle number.pkl",
            'rb'))
        stdev_error = np.load(destination_path + "stdev error per particle number.npy")

        plt.figure(1)
        ax.scatter(average_error.keys(), average_error.values(), color=colors[i])
        ax.plot(average_error.keys(), average_error.values(), color=colors[i], label=models[i])
        ax.errorbar(average_error.keys(), average_error.values(), yerr=stdev_error, ls="None",
                    color=colors[i], capsize=2, elinewidth=0.5, capthick=0.5)
        ax.set_ylabel("average rms error from grountruth [mm]")
        ax.set_xlabel("number of particles")
        plt.title("Average error from groundtruth")

plt.legend()
plt.show()
plt.savefig("C:\\Users\\Chris\\OneDrive\\Desktop\\result_tilt_side_old\\performance\\" + "performance_"+TYPE+".svg")
