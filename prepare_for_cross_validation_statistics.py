import copy
import csv

SAMPLES = []  # SAMPLES
PATH = ""  # ENTER PATH TO SOURCE FOLDER

with open(PATH + "statistics_for_AnovaRM.csv", 'w', newline='') as sheet:
    writer = csv.writer(sheet, delimiter=',')
    writer.writerow(["sample", "measurement", "rms"])

    for j, ref_nr in enumerate(SAMPLES):
        TESTS = copy.deepcopy(SAMPLES)
        TESTS.remove(ref_nr)
        for i, sample_nr in enumerate(TESTS):
            offset = j * len(TESTS)
            ahistoric_path = PATH + "AHISTORIC\\vs_" + ref_nr + "\\" + sample_nr + "_rms.txt"
            dtw_path = PATH + "SLIDING_DTW\\vs_" + ref_nr + "\\" + sample_nr + "_rms.txt"
            with open(ahistoric_path, 'r') as file:
                lines = file.readlines()
                writer.writerow([offset + i + 1, "ahistoric", float(lines[1])])

            with open(dtw_path) as file:
                lines = file.readlines()
                writer.writerow([offset + i + 1, "sliding_dtw", float(lines[1])])
                writer.writerow([offset + i + 1, "displacement", float(lines[4])])
                writer.writerow([offset + i + 1, "alpha_displacement", float(lines[7])])

with open(PATH + "statistics_for_post_hoc_tests.csv", 'w', newline='') as sheet:
    writer = csv.writer(sheet, delimiter=',')
    writer.writerow(["ahistoric", "sliding_dtw", "displacement", "alpha_displacement"])

    for j, ref_nr in enumerate(SAMPLES):
        TESTS = copy.deepcopy(SAMPLES)
        TESTS.remove(ref_nr)
        for i, sample_nr in enumerate(TESTS):
            row = []
            offset = j * len(TESTS)
            ahistoric_path = PATH + "AHISTORIC\\vs_" + ref_nr + "\\" + sample_nr + "_rms.txt"
            dtw_path = PATH + "SLIDING_DTW\\vs_" + ref_nr + "\\" + sample_nr + "_rms.txt"
            with open(ahistoric_path, 'r') as file:
                lines = file.readlines()
                row.append(float(lines[1]))

            with open(dtw_path, 'r') as file:
                lines = file.readlines()

                row.append(float(lines[1]))
                row.append(float(lines[4]))
                row.append(float(lines[7]))
            writer.writerow(row)
