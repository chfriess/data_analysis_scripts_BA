import csv

samples = ["20", "25", "27", "29", "30", "31", "34", "35"]
path = "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom_data_testing\\"


with open(path + "statistics_for_AnovaRM.csv", 'w', newline='') as sheet:
    writer = csv.writer(sheet, delimiter=',')
    writer.writerow(["sample", "measurement", "rms"])
    for i in range(len(samples)):
        ahistoric_path = "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom_data_testing\\sample_" + str(
            samples[i]) + "\\results_sample_" + str(samples[i]) + "\\ahistoric\\"
        dtw_path = "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom_data_testing\\sample_" + str(
            samples[i]) + "\\results_sample_" + str(samples[i]) + "\\sliding_dtw\\"
        with open(ahistoric_path + "phantom_sample_" + str(samples[i]) + "_rms.txt", 'r') as file:
            lines = file.readlines()

            writer.writerow([i+1, "ahistoric", float(lines[1])])

        with open(dtw_path + "phantom_sample_" + str(samples[i]) + "_rms.txt", 'r') as file:
            lines = file.readlines()

            writer.writerow([i+1, "sliding_dtw", float(lines[1])])
            writer.writerow([i+1, "displacement", float(lines[4])])
            writer.writerow([i+1, "alpha_displacement", float(lines[7])])



with open(path + "statistics_for_post_hocs_tests.csv", 'w', newline='') as sheet:
    writer = csv.writer(sheet, delimiter=',')
    writer.writerow(["ahistoric", "sliding_dtw", "displacement", "alpha_displacement"])

    for i in range(len(samples)):
        row = []
        ahistoric_path = "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom_data_testing\\sample_" + str(
            samples[i]) + "\\results_sample_" + str(samples[i]) + "\\ahistoric\\"
        dtw_path = "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom_data_testing\\sample_" + str(
            samples[i]) + "\\results_sample_" + str(samples[i]) + "\\sliding_dtw\\"
        with open(ahistoric_path + "phantom_sample_" + str(samples[i]) + "_rms.txt", 'r') as file:
            lines = file.readlines()
            row.append(float(lines[1]))

        with open(dtw_path + "phantom_sample_" + str(samples[i]) + "_rms.txt", 'r') as file:
            lines = file.readlines()

            row.append(float(lines[1]))
            row.append(float(lines[4]))
            row.append(float(lines[7]))
        writer.writerow(row)