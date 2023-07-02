import collections
import json
import os
import pickle
import statistics

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy import ndimage

NR_CROPPED = 2  # number of data points cropped from the end of the signal after interpolation to correct artefacts


def normalize_values(d):
    mu = statistics.mean(d)
    sigma = statistics.stdev(d)
    for i, el in enumerate(d):
        d[i] = (el - mu) / sigma
    return d


def normalize_values_space_standardized(impedance, cumulative_displacement):
    x = np.linspace(0, cumulative_displacement[-1], len(impedance)*5)
    impedance_per_position = np.interp(x, cumulative_displacement[1:], impedance)
    mu = statistics.mean(impedance_per_position)
    sigma = statistics.stdev(impedance_per_position)

    impedance_normalized = []
    for i, el in enumerate(impedance):
        impedance_normalized.append((el - mu) / sigma)
    return impedance_normalized

def plot_impedance_over_em():
    setup = "main branch old setup"
    for COREGISTRATION_NR in [str(x) for x in range(1, 11)]:
        impedance = np.load("C:\\Users\\Chris\\OneDrive\\Desktop\\tilt_phantom\\"  +setup + "\\sample_" + COREGISTRATION_NR + "\\data_bioelectric_sensors\\impedance_normalized_filtered_" + COREGISTRATION_NR + ".npy")
        em = np.load("C:\\Users\\Chris\\OneDrive\\Desktop\\tilt_phantom\\"  +setup + "\\sample_" + COREGISTRATION_NR + "\\data_bioelectric_sensors\\em_interpolated_" + COREGISTRATION_NR + ".npy")

        fig, ax = plt.subplots()
        ax.set_ylabel("z-score")
        ax.set_xlabel("em cumulative displacement")

        #ax.axvline(x=80, color='purple', label="iliaka aorta")
        #ax.axvline(x=120, color='r', label="middle branch")
        #ax.axvline(x=180, color='g', label="renal branch")

        plt.title(setup + COREGISTRATION_NR + "")

        d = {}

        for i, el in enumerate(em[1:]):
            if el in d.keys():
                d[el].append(impedance[i])
            else:
                d[el] = [impedance[i]]

        for key in d.keys():
            d[key] = np.mean(d[key])

        # the particle filter expects the position/impedance-prediction values to be sorted ascending by position
        od = collections.OrderedDict(sorted(d.items()))

        ax.plot(od.keys(), od.values())
        positions = []
        for key in od.keys():
            positions.append({"centerline_position": key, "reference_signal": od[key]})

        reference = {}
        reference["signal_per_centerline_position"] = positions

        jo = json.dumps(reference, indent=4)

        with open("C:\\Users\\Chris\\OneDrive\\Desktop\\tilt_phantom\\"  +setup + "\\sample_" + COREGISTRATION_NR + "\\reference_for_cross_validation\\impedance per groundtruth" + COREGISTRATION_NR + ".json", "w") as outfile:
            outfile.write(jo)

        plt.savefig("C:\\Users\\Chris\\OneDrive\\Desktop\\tilt_phantom\\"  +setup + "\\sample_" + COREGISTRATION_NR + "\\reference_for_cross_validation\\impedance per groundtruth" + COREGISTRATION_NR + ".svg")
        plt.clf()

def interpolate_em_on_bioelectric():
    BASE_PATH = "C:\\Users\\Chris\\OneDrive\\Desktop\\tilt_phantom\\side branch new setup\\"

    for COREGISTRATION_NR in ["6"]:
    #for COREGISTRATION_NR in [str(x) for x in range(1, 11)]:
        print("interpolate em on bioelectric " + COREGISTRATION_NR)

        os.chdir(BASE_PATH + "sample_"
                 + COREGISTRATION_NR + "\\data_bioelectric_sensors\\")

        em_timestamp_path = BASE_PATH + "sample_" \
                            + COREGISTRATION_NR + "\\em_groundtruth\\coregistration_" + COREGISTRATION_NR + "_em.csv"

        FILE = "coregistration_" + COREGISTRATION_NR + "_sampling_corrected.npz"

        data = np.load(FILE)

        df = pd.read_csv(em_timestamp_path, sep="\t")
        df2 = df.iloc[:, 16:17]
        raw_timestamps = df2.to_numpy()
        em = np.load(BASE_PATH + "sample_"
                     + COREGISTRATION_NR + "\\em_groundtruth\\displacement_from_origin.npy")
        timestamps_em = []
        for i in range(1, len(raw_timestamps)):
            timestamps_em.append(raw_timestamps[i][0])

        begin_em = 0
        while timestamps_em[begin_em] < data["mean_times_of_fft_windows_chAB"][0]:
            begin_em += 1
        end_em = begin_em
        while timestamps_em[end_em] < data["mean_times_of_fft_windows_chAB"][-1]:
            end_em += 1
        print("begin em" + str(begin_em))
        print("end em" + str(end_em))
        cumulative_displacements = data["windows_x_translation"] * (-1)
        impedance = data["fft_magnitude_BminA"]
        displacements = []

        # generate new x axis, cumualtive displacement em has a zero value , displacement and impedance starts one later

        em_interpolated = np.interp(data["mean_times_of_fft_windows_chAB"], timestamps_em[begin_em:end_em],
                                    em[begin_em:end_em])

        # em needs one value more than bioelectric impedance and displacement values
        em_interpolated = np.insert(em_interpolated, 0, em_interpolated[0])

        for i in range(1, len(cumulative_displacements)):
            displacements.append(cumulative_displacements[i] - cumulative_displacements[i - 1])

        # remove last 2 values, since the last values often deviate due to some signal error
        em_interpolated = em_interpolated[:-NR_CROPPED]
        impedance = impedance[:-NR_CROPPED]
        displacements = displacements[:-NR_CROPPED]
        cumulative_displacements = cumulative_displacements[:-NR_CROPPED]
        impedance_normalized = normalize_values_space_standardized(
            impedance=impedance, cumulative_displacement=cumulative_displacements)
        impedance_normalized_filtered = ndimage.gaussian_filter1d(impedance_normalized, 2)

        fig, ax = plt.subplots()
        # the starting point of cumulative interpolated is set to the first value of the em signal in the filter
        # to visualize whether em and cumulative start simultaneously, cumulative interpolated is also set
        # to the first em value
        ax.plot(cumulative_displacements + em_interpolated[0], label="cumulative interpolated")
        ax.plot(em_interpolated, label="em interpolated")

        """
        groundtruth and cumulative start at 0, displacements and impedance with 1, the first update step
        therefore, em_interpolated[1] corresponds to impedance[0] => to correct that in the figure, the first value is
        doubled
        """

        ax.plot(np.insert(displacements, 0, displacements[0]),
                label="displacements interpolated")

        ax.set_xlabel("update steps ")
        ax.set_ylabel("displacement along centerline [mm]")

        ax2 = ax.twinx()

        ax2.plot(np.insert(impedance_normalized, 0, impedance_normalized[0]), color="black",
                 label="impedance interpolated")
        ax2.plot(np.insert(impedance_normalized_filtered, 0, impedance_normalized[0]),
                 color="purple",
                 label="impedance interpolated smoothed")
        ax2.set_ylabel("z-value impedance")
        ax.legend()
        ax2.legend()

        plt.savefig("check_validity_" + COREGISTRATION_NR + ".svg")
        np.save("em_interpolated_" + COREGISTRATION_NR, em_interpolated)
        np.save("impedance_" + COREGISTRATION_NR, impedance)
        np.save("displacements_" + COREGISTRATION_NR, displacements)
        np.save("cumulative_displacements_interpolated_" + COREGISTRATION_NR, cumulative_displacements)
        np.save("impedance_normalized_" + COREGISTRATION_NR, impedance_normalized)
        np.save("impedance_normalized_filtered_" + COREGISTRATION_NR,
                impedance_normalized_filtered)

        print("length em interpolated = " + str(len(em_interpolated)))
        print("length impedance = " + str(len(impedance)))
        print("length displacements = " + str(len(displacements)))
        print("length cumulative displacements = " + str(len(cumulative_displacements)))
        plt.clf()


def interpolate_em_and_bioelectric():
    BASE_PATH = "C:\\Users\\Chris\\OneDrive\\Desktop\\tilt_phantom\\side branch new setup\\"

    # for COREGISTRATION_NR in [str(x) for x in range(1, 11)]:
    for COREGISTRATION_NR in ["3"]:
        os.chdir(BASE_PATH + "sample_"
                 + COREGISTRATION_NR + "\\data_bioelectric_sensors\\")

        em_timestamp_path = BASE_PATH + "sample_" \
                            + COREGISTRATION_NR + "\\em_groundtruth\\coregistration_" + COREGISTRATION_NR + "_em.csv"

        FILE = "coregistration_" + COREGISTRATION_NR + "_sampling_corrected.npz"

        data = np.load(FILE)

        df = pd.read_csv(em_timestamp_path, sep="\t")
        df2 = df.iloc[:, 16:17]
        raw_timestamps = df2.to_numpy()
        em = np.load(BASE_PATH + "sample_"
                     + COREGISTRATION_NR + "\\em_groundtruth\\displacement_from_origin.npy")
        timestamps_em = []
        for i in range(1, len(raw_timestamps)):
            timestamps_em.append(raw_timestamps[i][0])

        begin_em = 0
        while timestamps_em[begin_em] < data["mean_times_of_fft_windows_chAB"][0]:
            begin_em += 1
        end_em = begin_em
        while timestamps_em[end_em] < data["mean_times_of_fft_windows_chAB"][-1]:
            end_em += 1
        print("begin em" + str(begin_em))
        print("end em" + str(end_em))
        cumulative_displacements = data["windows_x_translation"]
        impedance = data["fft_magnitude_BminA"]

        # generate new x axis, cumualtive displacement em has a zero value , displacement and impedance starts one later
        x_bioelectric = np.linspace(data["mean_times_of_fft_windows_chAB"][0],
                                    data["mean_times_of_fft_windows_chAB"][-1], 149)
        x_em = np.linspace(timestamps_em[begin_em], timestamps_em[end_em], 150)

        em_interpolated = np.interp(x_em, timestamps_em[begin_em:end_em], em[begin_em:end_em])

        cumulative_interpolated = np.interp(x_bioelectric, data["mean_times_of_fft_windows_chAB"],
                                            cumulative_displacements[1:])
        impedance_interpolated = np.interp(x_bioelectric, data["mean_times_of_fft_windows_chAB"], impedance)
        cumulative_interpolated = np.insert(cumulative_interpolated, 0, 0)
        displacements_interpolated = []
        for i in range(1, len(cumulative_interpolated)):
            displacements_interpolated.append(cumulative_interpolated[i] - cumulative_interpolated[i - 1])

        displacements_interpolated = list(np.array(displacements_interpolated) * (-1))
        cumulative_interpolated = list(np.array(cumulative_interpolated) * (-1))

        # remove last 2 values, since the last values often deviate due to some signal error
        em_interpolated = em_interpolated[:-NR_CROPPED]
        impedance_interpolated = impedance_interpolated[:-NR_CROPPED]
        displacements_interpolated = displacements_interpolated[:-NR_CROPPED]
        cumulative_interpolated = cumulative_interpolated[:-NR_CROPPED]
        impedance_interpolated_normalized = np.array(normalize_values(list(impedance_interpolated)))
        impedance_interpolated_normalized_filtered = ndimage.gaussian_filter1d(impedance_interpolated_normalized, 5)

        fig, ax = plt.subplots()
        # the starting point of cumulative interpolated is set to the first value of the em signal in the filter
        # to visualize whether em and cumulative start simultaneously, cumulative interpolated is also set
        # to the first em value
        ax.plot(cumulative_interpolated + em_interpolated[0], label="cumulative interpolated")
        ax.plot(em_interpolated, label="em interpolated")

        """
        groundtruth and cumulative start at 0, displacements and impedance with 1, the first update step
        therefore, em_interpolated[1] corresponds to impedance[0] => to correct that in the figure, the first value is
        doubled
        """
        ax.plot(np.insert(displacements_interpolated, 0, displacements_interpolated[0]),
                label="displacements interpolated")

        ax.set_xlabel("update steps ")
        ax.set_ylabel("displacement along centerline [mm]")

        ax2 = ax.twinx()

        ax2.plot(np.insert(impedance_interpolated_normalized, 0, impedance_interpolated_normalized[0]), color="black",
                 label="impedance interpolated")
        ax2.plot(np.insert(impedance_interpolated_normalized_filtered, 0, impedance_interpolated_normalized[0]),
                 color="purple",
                 label="impedance interpolated smoothed")
        ax2.set_ylabel("z-value impedance")
        ax.legend()
        ax2.legend()

        plt.savefig("check_validity_" + COREGISTRATION_NR + ".svg")
        np.save("em_interpolated_" + COREGISTRATION_NR, em_interpolated)
        np.save("impedance_interpolated_" + COREGISTRATION_NR, impedance_interpolated)
        np.save("displacements_interpolated_" + COREGISTRATION_NR, displacements_interpolated)
        np.save("cumulative_displacements_interpolated_" + COREGISTRATION_NR, cumulative_interpolated)
        np.save("impedance_interpolated_normalized_" + COREGISTRATION_NR, impedance_interpolated_normalized)
        np.save("impedance_interpolated_normalized_filtered_" + COREGISTRATION_NR,
                impedance_interpolated_normalized_filtered)

        print(len(em_interpolated))
        print(len(impedance_interpolated))
        print(len(displacements_interpolated))
        plt.clf()


if __name__ == "__main__":

    #interpolate_em_on_bioelectric()
    plot_impedance_over_em()

