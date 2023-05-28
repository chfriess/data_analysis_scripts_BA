import math
import statistics

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.signal import stft, find_peaks


def moving_average(interval, window_size):
    window = np.ones(int(window_size)) / float(window_size)
    return np.convolve(interval, window, 'same')


def find_signal_deviations_with_moving_average(signal):
    signal_moving_average = list(moving_average(signal, 5))

    std_signal = np.std(signal_moving_average)
    events = []
    indices = []
    for i in range(len(signal)):
        if signal[i] > std_signal + std_signal:
            events.append(signal[i])
            indices.append(i)
    return indices, events


def find_signal_deviations_stft(signal):
    f, t, Zxx = stft(signal, nperseg=1000)
    plt.pcolormesh(t, f, np.abs(Zxx), vmin=0, vmax=2, shading='gouraud')

    plt.show()


def find_point_of_first_upstroke(signal) -> int:
    signal_derivative = np.gradient(signal)

    signal_rolling_variance = pd.Series(signal_derivative).rolling(window=10, center=False).std().to_numpy()

    offset = 0
    for i, el in enumerate(signal_rolling_variance):
        if not math.isnan(el):
            offset = i
            break

    std = np.std(signal_rolling_variance[offset:offset + 10]) * 10

    n = 0
    for i in range(offset + 1, len(signal_rolling_variance)):
        if signal_rolling_variance[i] - signal_rolling_variance[i - 1] > std:
            n = i - 1
            break
    return n


if __name__ == '__main__':
    for COREGISTRATION_NR in [str(x) for x in range(30, 31)]:
        DESTINATION = "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom coregistration data\\06_05_2023_BS\\coregistration_" + COREGISTRATION_NR + "\\em_groundtruth\\groundtruth_" + COREGISTRATION_NR + "_cropped.npy"
        em_groundtruth_raw = np.load(
            "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom coregistration data\\06_05_2023_BS\\coregistration_" + COREGISTRATION_NR + "\\em_groundtruth\\displacement_from_origin.npy")

        timestamps_bioelectric = pd.read_csv(
            "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom coregistration data\\06_05_2023_BS\\coregistration_" + COREGISTRATION_NR + "\\data_bioelectric_sensors\\coregistration_" + COREGISTRATION_NR + "__magnitudes_and_timestamps.csv")
        t_bio = timestamps_bioelectric[' timestamps'].tolist()

        timestamps_em = pd.read_csv(
            "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom coregistration data\\06_05_2023_BS\\coregistration_" + COREGISTRATION_NR + "\\coregistration_" + COREGISTRATION_NR + "_em.csv",
            sep='\t')
        t_em = timestamps_em.iloc[:, 16].tolist()
        cumulative_displacement = np.load(
            "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom coregistration data\\06_05_2023_BS\\coregistration_" + COREGISTRATION_NR + "\\data_bioelectric_sensors\\cumulative displacements sample" + COREGISTRATION_NR + ".npy")
        cumulative_displacement = cumulative_displacement[:len(cumulative_displacement) - 5]

        displacement_upstroke = find_point_of_first_upstroke(cumulative_displacement)
        em_upstroke = find_point_of_first_upstroke(em_groundtruth_raw)
        em_start = em_upstroke-(displacement_upstroke*3)

        em_before_start = em_groundtruth_raw[em_start:em_upstroke:3]
        em_after_start = em_groundtruth_raw[em_upstroke+1:em_upstroke+1+(len(cumulative_displacement)-displacement_upstroke)*3:3]

        em_cropped = np.append(em_before_start,em_after_start)

        plt.plot(cumulative_displacement+em_groundtruth_raw[0], color="green")
        plt.plot(em_cropped, color="blue")
        plt.axvline(x=displacement_upstroke, color='r', label="timestamp synchronization point")

        """

        starting_point = 0
        for i in range(len(t_em)):
            if t_em[i] > t_bio[0]:
                starting_point = i
                break

        x = [z for z in range(starting_point, starting_point+len(cumulative_displacement))]
        em_groundtruth_cropped = []
        for i in range(starting_point, starting_point + len(t_bio) * 3, 3):
            em_groundtruth_cropped.append(em_groundtruth_raw[i])

        if (len(em_groundtruth_cropped) != len(t_bio)):
            raise ValueError("after cropping length of groundtruth must be equal to length of bioelectric signal")


        #print(len(em_groundtruth_raw))
        #print(len(timestamps_em))

        plt.plot(em_groundtruth_raw[:2000], label="cumulative em groundtruth")

        plt.axvline(x=starting_point, color='r', label="timestamp synchronization point")
        plt.plot(x, cumulative_displacement, label="cumulative displacement")
        plt.ylabel("position along centerline in mm")
        plt.xlabel("update step")
        plt.legend()
        plt.show()

        #plt.plot(em_groundtruth_cropped, color="red")

        #np.save(DESTINATION, np.array(em_groundtruth_cropped))
"""
