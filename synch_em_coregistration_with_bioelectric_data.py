import numpy as np
import pandas as pd

if __name__ == '__main__':
    for COREGISTRATION_NR in [str(x) for x in range(25, 36)]:
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

        starting_point = 0
        for i in range(len(t_em)):
            if t_em[i] > t_bio[0]:
                starting_point = i
                break

        em_groundtruth_cropped = []

        for i in range(starting_point, starting_point + len(t_bio) * 3, 3):
            em_groundtruth_cropped.append(em_groundtruth_raw[i])

        if (len(em_groundtruth_cropped) != len(t_bio)):
            raise ValueError("after cropping length of groundtruth must be equal to length of bioelectric signal")

        np.save(DESTINATION, np.array(em_groundtruth_cropped))
