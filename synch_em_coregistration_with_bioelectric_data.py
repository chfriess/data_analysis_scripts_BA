import numpy as np
import pandas as pd

COREGISTRATION_NR = "20"

DESTINATION = "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom coregistration data\\06_05_2023_BS\\coregistration_" + COREGISTRATION_NR + "\\em_groundtruth\\groundtruth_"+COREGISTRATION_NR+"_cropped.npy"

if __name__ == '__main__':
    em_groundtruth_raw = np.load(
        "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom coregistration data\\06_05_2023_BS\\coregistration_" + COREGISTRATION_NR + "\\em_groundtruth\\displacement_from_origin.npy")

    timestamps_bioelectric = pd.read_csv(
        "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom coregistration data\\06_05_2023_BS\\coregistration_" + COREGISTRATION_NR + "\\data_bioelectric_sensors\\coregistration_20_alpha_br12__export.npy__magnitudes_and_timestamps.csv")
    t_bio = timestamps_bioelectric[' timestamps'].tolist()


    timestamps_em = pd.read_csv(
        "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom coregistration data\\06_05_2023_BS\\coregistration_" + COREGISTRATION_NR + "\\coregistration_20_em.csv", sep='\t')
    t_em = timestamps_em.iloc[:,16].tolist()



    print(t_em)
    

