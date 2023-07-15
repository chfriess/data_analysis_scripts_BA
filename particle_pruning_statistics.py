import copy
import json
import pickle
import scipy.stats as stats

import numpy as np

SAMPLES = ["2", "3", "5", "6", "7", "8", "9", "10"]


TRAJECTORY = "SIDE"
DESTINATION = "C:\\Users\\Chris\\OneDrive\\Desktop\\pruning\\"
branch_accuracy = {"AHISTORIC": [], "SLIDING_DTW": []}


TOTAL = len(SAMPLES) * (len(SAMPLES)-1)
LAST_CORRECT = {"AHISTORIC": 0, "SLIDING_DTW": 0}

for ref_nr in SAMPLES:
    TESTS = copy.deepcopy(SAMPLES)
    TESTS.remove(ref_nr)
    for sample_nr in TESTS:
        for SETUP in ["AHISTORIC", "SLIDING_DTW"]:

            groundtruth = np.load("C:\\Users\\Chris\\OneDrive\\Desktop\\tilt_phantom\\side branch old setup\\sample_" \
                                  + sample_nr + "\\data_bioelectric_sensors\\em_interpolated_" \
                                  + sample_nr + ".npy")

            groundtruth = groundtruth[1:]
            positions_path = "C:\\Users\\Chris\\OneDrive\\Desktop\\result_tilt_side_old\\cross_validation_pruning\\" + SETUP + "\\vs_" + ref_nr + "\\positions_" + sample_nr + ".json"
            #positions_path = "C:\\Users\\Chris\\OneDrive\\Desktop\\result_tilt_main_old\\sample_" + sample_nr + "\\" + SETUP + "\\positions_" + sample_nr + ".json"
            with open(positions_path, "r") as infile:
                positions = json.load(infile)

            if len(positions) != len(groundtruth):
                raise ValueError("position estimates and groundtruth must feature same length")

            branch_per_update_step = [0 for _ in range(len(groundtruth))]
            if TRAJECTORY == "SIDE":
                for i, el in enumerate(groundtruth):
                    if el < 80:
                        branch_per_update_step[i] = 0
                    elif 80 <= el < 190:
                        branch_per_update_step[i] = 1
                    elif el >= 190:
                        branch_per_update_step[i] = 3


            elif TRAJECTORY == "MAIN":
                for i, el in enumerate(groundtruth):
                    if el < 80:
                        branch_per_update_step[i] = 0
                    elif 80 <= el < 190:
                        branch_per_update_step[i] = 1
                    elif el >= 190:

                        branch_per_update_step[i] = 2

            number_of_correct_branch_estimations = 0
            est = []
            for i, el in enumerate(branch_per_update_step):
                est.append(positions[str(i)][1])
                if positions[str(i)][1] == el:
                    number_of_correct_branch_estimations += 1
            if branch_per_update_step[-1] == positions[str((len(positions)-1))][1]:
                LAST_CORRECT[SETUP] += 1
            print(SETUP + " sample nr: " + sample_nr + " correct estimates " + str(number_of_correct_branch_estimations))
            branch_accuracy[SETUP].append(number_of_correct_branch_estimations / len(positions))
            print(branch_per_update_step)
            print(est)
            print("\n\n")

with open(DESTINATION + TRAJECTORY + "_branch_accuracy.pkl", 'wb') as f:
    pickle.dump(branch_accuracy, f)

result = stats.ttest_rel(branch_accuracy["AHISTORIC"], branch_accuracy["SLIDING_DTW"])

with open(DESTINATION + TRAJECTORY + "_statistics.txt", 'w') as f:
    f.write("mean AHISTORIC: " + str(np.mean(branch_accuracy["AHISTORIC"])) + "\n")
    f.write("stdev AHISTORIC: " + str(np.std(branch_accuracy["AHISTORIC"])) + "\n")
    f.write("mean SLIDING_DTW: " + str(np.mean(branch_accuracy["SLIDING_DTW"])) + "\n")
    f.write("stdev SLIDING_DTW: " + str(np.std(branch_accuracy["SLIDING_DTW"])) + "\n")
    f.write("t-test related AHISTORIC vs. SLIDING_DTW: " + str(result))

print(LAST_CORRECT)
print(TOTAL)