import csv

#SAMPLES = ["20", "25", "27", "29"]
#PATH = "C:\\Users\\Chris\\OneDrive\\Desktop\\test\\"

with open(PATH + "statistics_for_AnovaRM.csv", 'w', newline='') as sheet:
    writer = csv.writer(sheet, delimiter=',')
    writer.writerow(["sample", "measurement", "rms"])

    for i, sample in enumerate(SAMPLES):
        ahistoric_path = PATH + "sample_" + sample + "\\" + "AHISTORIC" + "\\" + sample + "_rms.txt"
        dtw_path = PATH + "sample_" + sample + "\\" + "SLIDING_DTW" + "\\" + sample + "_rms.txt"
        with open(ahistoric_path, 'r') as file:
            lines = file.readlines()
            writer.writerow([i + 1, "ahistoric", float(lines[1])])

        with open(dtw_path) as file:
            lines = file.readlines()
            writer.writerow([i + 1, "sliding_dtw", float(lines[1])])
            writer.writerow([i + 1, "displacement", float(lines[4])])
            writer.writerow([i + 1, "alpha_displacement", float(lines[7])])

with open(PATH + "statistics_for_post_hoc_tests.csv", 'w', newline='') as sheet:
    writer = csv.writer(sheet, delimiter=',')
    writer.writerow(["ahistoric", "sliding_dtw", "displacement", "alpha_displacement"])

    for i, sample in enumerate(SAMPLES):
        row = []
        ahistoric_path = PATH + "sample_" + sample + "\\" + "AHISTORIC" + "\\" + sample + "_rms.txt"
        dtw_path = PATH + "sample_" + sample + "\\" + "SLIDING_DTW" + "\\" + sample + "_rms.txt"
        with open(ahistoric_path, 'r') as file:
            lines = file.readlines()
            row.append(float(lines[1]))

        with open(dtw_path, 'r') as file:
            lines = file.readlines()

            row.append(float(lines[1]))
            row.append(float(lines[4]))
            row.append(float(lines[7]))
        writer.writerow(row)
