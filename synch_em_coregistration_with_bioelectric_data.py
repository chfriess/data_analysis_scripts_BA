import math
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def simulate_timestamps_of_cumulative_displacement(signal_length: int) -> np.ndarray:
    return np.cumsum(np.array(range(signal_length)) * 0.08)


def load_timestamps_of_em_signal(path: str) -> np.ndarray:
    pass


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
    for COREGISTRATION_NR in [str(x) for x in [25]]:
        DESTINATION = "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom coregistration data\\06_05_2023_BS\\coregistration_" \
                      + COREGISTRATION_NR + "\\em_groundtruth\\groundtruth_" + COREGISTRATION_NR + "_cropped.npy"
        EM_PATH = "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom coregistration data\\06_05_2023_BS\\coregistration_" \
                  + COREGISTRATION_NR + "\\em_groundtruth\\displacement_from_origin.npy"
        em_groundtruth_raw = np.load(EM_PATH)
        cumulative_displacement = np.load(
            "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom coregistration data\\06_05_2023_BS\\coregistration_"
            + COREGISTRATION_NR + "\\data_bioelectric_sensors\\cumulative displacements sample"
            + COREGISTRATION_NR + ".npy")
        #prune the last two signal points, as they measure nonsense

        displacements = np.load(
            "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom coregistration data\\06_05_2023_BS\\coregistration_"
            + COREGISTRATION_NR + "\\data_bioelectric_sensors\\displacements_sample"
            + COREGISTRATION_NR + ".npy")
        impedance = np.load(
            "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom coregistration data\\06_05_2023_BS\\coregistration_"
            + COREGISTRATION_NR + "\\data_bioelectric_sensors\\impedance_sample"
            + COREGISTRATION_NR + ".npy")
        cumulative_displacement = cumulative_displacement[:len(cumulative_displacement) - 2]
        displacements = displacements[:len(displacements)-2]
        impedance = impedance[:len(impedance)-2]


        #find the points of the first upstroke, then prune the prior signal
        displacement_upstroke = find_point_of_first_upstroke_displacement(cumulative_displacement)
        em_upstroke = find_point_of_first_upstroke_em(em_groundtruth_raw)

        """
        The cumulative displacements contains one value more than the displacement and impedance values;
        the displacement_upstroke is the point in the cumulative displacement signal before the steep signal increase,
        therefore the point after the displacement_upstroke is the first displacement and impedance measurement
        included; since displacements and impedance are 1 value shorter than cumulative, displacement_upstroke must
        not be incremented by 1 to acheive this
        """
        displacements_cropped = displacements[displacement_upstroke:]
        impedance_cropped = impedance[displacement_upstroke:]
        em_cropped = em_groundtruth_raw[em_upstroke:]

        print(len(impedance_cropped))
        print(len(cumulative_displacement[displacement_upstroke:]))
        """
        plt.plot(cumulative_displacement[displacement_upstroke:] + em_groundtruth_raw[0], color="green")
        plt.plot(em_groundtruth_raw[em_upstroke:], color="blue")
        plt.show()

        
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
        """