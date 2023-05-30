import math
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.signal import stft


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
    print(n)
    return n


if __name__ == '__main__':
    for COREGISTRATION_NR in [str(x) for x in [34]]:
        DESTINATION = "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom coregistration data\\06_05_2023_BS\\coregistration_" + COREGISTRATION_NR + "\\em_groundtruth\\groundtruth_" + COREGISTRATION_NR + "_cropped.npy"
        em_groundtruth_raw = np.load(
            "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom coregistration data\\06_05_2023_BS\\coregistration_" + COREGISTRATION_NR + "\\em_groundtruth\\displacement_from_origin.npy")
        cumulative_displacement = np.load(
            "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom coregistration data\\06_05_2023_BS\\coregistration_" + COREGISTRATION_NR + "\\data_bioelectric_sensors\\cumulative displacements sample" + COREGISTRATION_NR + ".npy")
        cumulative_displacement = cumulative_displacement[:len(cumulative_displacement) - 2]

        displacement_upstroke = find_point_of_first_upstroke_displacement(cumulative_displacement)

        em_upstroke = find_point_of_first_upstroke_em(em_groundtruth_raw)
        em_start = em_upstroke - (displacement_upstroke * 3)

        em_before_start = em_groundtruth_raw[em_start:em_upstroke:3]
        em_after_start = em_groundtruth_raw[
                         em_upstroke + 1:em_upstroke + 1 + (len(cumulative_displacement) - displacement_upstroke) * 3:3]

        em_cropped = np.append(em_before_start, em_after_start)

        plt.plot(cumulative_displacement + em_groundtruth_raw[0], color="green")
        plt.plot(em_cropped, color="blue")
        plt.axvline(x=displacement_upstroke, color='r', label="timestamp synchronization point")
        #plt.show()

        np.save(DESTINATION, np.array(em_cropped))
