import os
import statistics

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

OFFSET_EM = -23  # distance between em-electrode and bioelectric electrode
NR_CROPPED = 2  # number of data points cropped from the end of the signal after interpolation to correct artefacts

def normalize_values(d: list) -> list:
    mu = statistics.mean(d)
    sigma = statistics.stdev(d)
    for i, el in enumerate(d):
        d[i] = (el - mu) / sigma
    return d


if __name__ == "__main__":

    BASE_PATH = "C:\\Users\\Chris\\OneDrive\\Desktop\\tilt_phantom\\side branch new setup\\"

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
        cumulative_interpolated = np.interp(x_bioelectric, data["mean_times_of_fft_windows_chAB"], cumulative_displacements[1:])
        impedance_interpolated = np.interp(x_bioelectric, data["mean_times_of_fft_windows_chAB"], impedance)
        cumulative_interpolated = np.insert(cumulative_interpolated, 0, 0)
        displacements_interpolated = []
        for i in range(1, len(cumulative_interpolated)):
            displacements_interpolated.append(cumulative_interpolated[i] - cumulative_interpolated[i - 1])

        displacements_interpolated = list(np.array(displacements_interpolated) * (-1))
        cumulative_interpolated = list(np.array(cumulative_interpolated) * (-1))

        # correct the offset between em sensor and bioelectric sensor
        em_interpolated += OFFSET_EM

        #remove last 2 values, since the last values often deviate due to some signal error
        em_interpolated = em_interpolated[:-NR_CROPPED]
        impedance_interpolated = impedance_interpolated[:-NR_CROPPED]
        displacements_interpolated = displacements_interpolated[:-NR_CROPPED]
        cumulative_interpolated = cumulative_interpolated[:-NR_CROPPED]
        impedance_interpolated_normalized = np.array(normalize_values(list(impedance_interpolated)))

        fig, ax = plt.subplots()
        ax.plot(cumulative_interpolated, label="cumulative interpolated")
        ax.plot(em_interpolated, label="em interpolated")

        """
        groundtruth and cumulative start at 0, displacements and impedance with 1, the first update step
        therefore, em_interpolated[1] corresponds to impedance[0] => to correct that in the figure, the first value is
        doubled
        """
        ax.plot(np.insert(displacements_interpolated, displacements_interpolated[0]),
                label="displacements interpolated")

        ax.set_xlabel("update steps ")
        ax.set_ylabel("displacement along centerline [mm]")

        ax2 = ax.twinx()

        ax2.plot(np.insert(impedance_interpolated_normalized, impedance_interpolated_normalized[0]),
                 label="impedance interpolated")
        ax2.set_ylabel("z-value impedance")

        plt.legend()
        plt.show()

        plt.savefig("check_validity_" + COREGISTRATION_NR + ".svg")
        np.save("em_interpolated_" + COREGISTRATION_NR, em_interpolated)
        np.save("impedance_interpolated_" + COREGISTRATION_NR, impedance_interpolated)
        np.save("displacements_interpolated_" + COREGISTRATION_NR, displacements_interpolated)
        np.save("cumulative_displacements_interpolated_" + COREGISTRATION_NR, cumulative_interpolated)
        np.save("impedance_interpolated_normalized_" + COREGISTRATION_NR, impedance_interpolated_normalized)

        print(len(em_interpolated))
        print(len(impedance_interpolated))
        print(len(displacements_interpolated))
        plt.clf()
