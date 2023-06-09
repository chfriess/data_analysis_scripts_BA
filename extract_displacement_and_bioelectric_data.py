import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

if __name__ == "__main__":
    BASE_PATH = "C:\\Users\\Chris\\OneDrive\\Desktop\\plastic coregistration data\\04_06_2023_BS\\"

    # for COREGISTRATION_NR in ["20", "25", "29", "30", "31", "34", "35"]:
    for COREGISTRATION_NR in ["42"]:
    #for COREGISTRATION_NR in [str(x) for x in range(40, 60)]:
        os.chdir(BASE_PATH + "coregistration_"
                 + COREGISTRATION_NR + "\\data_bioelectric_sensors\\")

        em_timestamp_path = BASE_PATH + "coregistration_" \
                            + COREGISTRATION_NR + "\\coregistration_" + COREGISTRATION_NR + "_em.csv"

        FILE = "coregistration_" + COREGISTRATION_NR + "_sampling_corrected.npz"

        data = np.load(FILE)

        df = pd.read_csv(em_timestamp_path, sep="\t")
        df2 = df.iloc[:, 16:17]
        raw_timestamps = df2.to_numpy()
        em = np.load(BASE_PATH + "coregistration_"
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

        cumulative_displacements = data["windows_x_translation"]
        impedance = data["fft_magnitude_BminA"]

        displacements = []

        for i in range(1, len(cumulative_displacements)):
            displacements.append(cumulative_displacements[i] - cumulative_displacements[i - 1])

        # generate new x axis, cumualtive displacement em has a zero value , displacement and impedance starts one later
        x_bioelectric = np.linspace(data["mean_times_of_fft_windows_chAB"][0],
                                    data["mean_times_of_fft_windows_chAB"][-1], 149)
        x_em = np.linspace(timestamps_em[begin_em], timestamps_em[end_em], 150)

        em_interpolated = np.interp(x_em, timestamps_em[begin_em:end_em], em[begin_em:end_em])
        displacements_interpolated = np.interp(x_bioelectric, data["mean_times_of_fft_windows_chAB"], displacements)
        impedance_interpolated = np.interp(x_bioelectric, data["mean_times_of_fft_windows_chAB"], impedance)

        cumulative_interpolated = [0]
        for i in range(len(displacements_interpolated)):
            cumulative_interpolated.append(displacements_interpolated[i] + cumulative_interpolated[i])

        plt.plot(cumulative_interpolated[:-2], label="cumulative interpolated")
        plt.plot(em_interpolated[:-2] - em_interpolated[0], label="em interpolated")
        plt.plot(np.array([0]) + impedance_interpolated[:-2] / 1000, label="impedance interpolated")
        plt.plot(displacements_interpolated[:-2], label="displacements interpolated")
        plt.legend()
        plt.show()

        """
        plt.savefig("check_validity_" + COREGISTRATION_NR+".svg")
        np.save("em_interpolated_" + COREGISTRATION_NR, em_interpolated[:-2])
        np.save("impedance_interpolated_" + COREGISTRATION_NR, impedance_interpolated[:-2])
        np.save("displacements_interpolated_" + COREGISTRATION_NR, displacements_interpolated[:-2])
        np.save("cumulative_displacements_interpolated_" + COREGISTRATION_NR, cumulative_interpolated[:-2])

        print(len(em_interpolated))
        print(len(impedance_interpolated))
        print(len(displacements_interpolated))
        plt.clf()
        """
