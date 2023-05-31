import math
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def simulate_timestamps_of_cumulative_displacement(signal_length: int) -> np.ndarray:
    timestamps = []
    for i in range(signal_length):
        timestamps.append(i*0.08)
    return np.array(timestamps)


def load_timestamps_of_em_signal(path: str) -> np.ndarray:
    df = pd.read_csv(path, sep="\t")
    df2 = df.iloc[:, 16:17]
    raw_timestamps = df2.to_numpy()
    offset = raw_timestamps[0][0]
    timestamps = [0]
    for i in range(1, len(raw_timestamps)):
        timestamps.append(raw_timestamps[i][0] - offset)
    return np.array(timestamps)


def find_point_of_first_upstroke_displacement(signal) -> int:
    std = np.std(signal[:10]) * 5

    n = 0
    for i in range(1, len(signal)):
        if signal[i] - signal[i - 1] > std:
            n = i - 1
            break
    return n


def find_point_of_first_upstroke_em(signal) -> int:
    signal_derivative = np.gradient(signal)
    signal_rolling_variance = pd.Series(signal_derivative).rolling(window=10, center=False).std().to_numpy()
    offset = 0
    for i, el in enumerate(signal_rolling_variance):
        if not math.isnan(el):
            offset = i
            break

    std = np.std(signal_rolling_variance[offset:offset + 20]) * 25

    n = 0
    for i in range(offset + 1, len(signal_rolling_variance)):
        if signal_rolling_variance[i] - signal_rolling_variance[i - 1] > std:
            n = i - 1
            break
    return n


if __name__ == '__main__':
    for COREGISTRATION_NR in [str(x) for x in [35]]:
        DESTINATION = "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom data testing\\sample_"+COREGISTRATION_NR\
                      +"\\data_sample_"+COREGISTRATION_NR+"\\"
        em_groundtruth_raw = np.load("C:\\Users\\Chris\\OneDrive\\Desktop\\phantom coregistration data\\"
                                     "06_05_2023_BS\\coregistration_"
                                     + COREGISTRATION_NR + "\\em_groundtruth\\displacement_from_origin.npy")
        cumulative_displacement = np.load(
            "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom coregistration data\\06_05_2023_BS\\coregistration_"
            + COREGISTRATION_NR + "\\data_bioelectric_sensors\\cumulative displacements sample"
            + COREGISTRATION_NR + ".npy")
        # prune the last two signal points, as they measure nonsense
        displacements = np.load(
            "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom coregistration data\\06_05_2023_BS\\coregistration_"
            + COREGISTRATION_NR + "\\data_bioelectric_sensors\\displacements_sample"
            + COREGISTRATION_NR + ".npy")
        impedance = np.load(
            "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom coregistration data\\06_05_2023_BS\\coregistration_"
            + COREGISTRATION_NR + "\\data_bioelectric_sensors\\impedance_sample"
            + COREGISTRATION_NR + ".npy")
        cumulative_displacement = cumulative_displacement[:len(cumulative_displacement) - 2]
        displacements = displacements[:len(displacements) - 2]
        impedance = impedance[:len(impedance) - 2]

        em_timestamps = load_timestamps_of_em_signal(
            "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom coregistration data\\"
            "06_05_2023_BS\\coregistration_"
            + COREGISTRATION_NR + "\\coregistration_" + COREGISTRATION_NR + "_em.csv")
        # find the points of the first upstroke, then prune the prior signal
        displacement_upstroke = find_point_of_first_upstroke_displacement(cumulative_displacement)
        em_upstroke = find_point_of_first_upstroke_em(em_groundtruth_raw)

        """
        The cumulative displacements contains one value more than the displacement and impedance values;
        the displacement_upstroke is the point in the cumulative displacement signal before the steep signal increase,
        therefore the point after the displacement_upstroke is the first displacement and impedance measurement
        included; since displacements and impedance are 1 value shorter than cumulative, displacement_upstroke must
        not be incremented by 1 to acheive this
        """
        cumulative_displacement_cropped = cumulative_displacement[displacement_upstroke:]
        displacements_cropped = displacements[displacement_upstroke:]
        impedance_cropped = impedance[displacement_upstroke:]
        bioelectric_timestamps = simulate_timestamps_of_cumulative_displacement(len(displacements_cropped))


        # em signal must be cropped to measurement duration of bioelectric sensors

        em_cropped = em_groundtruth_raw[em_upstroke:]
        em_timestamps_cropped = em_timestamps[em_upstroke:]
        i = 0
        while em_timestamps_cropped[i]-em_timestamps_cropped[0] < bioelectric_timestamps[-1]:
            i += 1

        em_cropped = em_cropped[:i]



        # now interpolate the signals to be of equal length (with em groundtruth having one value more)
        a = simulate_timestamps_of_cumulative_displacement(len(cumulative_displacement_cropped))
        x_cumulative = np.linspace(a[0], a[-1], 150)
        cumulative_interpolated = np.interp(x_cumulative, a, cumulative_displacement_cropped)

        x_em = np.linspace(em_timestamps_cropped[0], em_timestamps_cropped[:i][-1], 150)
        em_interpolated = np.interp(x_em, em_timestamps_cropped[:i], em_cropped[:i])


        x_bio = np.linspace(bioelectric_timestamps[0], bioelectric_timestamps[-1], 149)
        displacements_interpolated = np.interp(x_bio, bioelectric_timestamps, displacements_cropped)
        impedance_interpolated = np.interp(x_bio, bioelectric_timestamps, impedance_cropped)

        plt.plot(em_interpolated)
        plt.plot(impedance_interpolated/1000)

        x = [0]
        for i in range(len(displacements_interpolated)):
            x.append(displacements_interpolated[i] + x[-1])

        plt.plot(x)

        print("length of em interp= " + str(len(em_interpolated)))
        print("length of disp interp= " + str(len(displacements_interpolated)))
        print("length of imp interp= " + str(len(impedance_interpolated)))

        np.save(DESTINATION + "groundtruth_interpolated.npy", em_interpolated)
        np.save(DESTINATION + "impedance_interpolated.npy", impedance_interpolated)
        np.save(DESTINATION + "displacements_interpolated.npy", displacements_interpolated)



