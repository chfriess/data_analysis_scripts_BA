import copy
import json
import pickle
import scipy.stats as stats

import numpy as np

SAMPLES = ["20", "25", "30", "31", "34"]


TRAJECTORY = "MAIN"
DESTINATION = "C:\\Users\\Chris\\OneDrive\\Desktop\\branch_pruning_agar_I\\"  # ENTER DESTINATION PATH
branch_accuracy = {"AHISTORIC": [], "SLIDING_DTW": []}


TOTAL = len(SAMPLES) * (len(SAMPLES)-1)
LAST_CORRECT = {"AHISTORIC": 0, "SLIDING_DTW": 0}

for sample_nr in SAMPLES:
    for SETUP in ["AHISTORIC", "SLIDING_DTW"]:
        groundtruth = np.load("") #  enter groundtruth path

        groundtruth = groundtruth[1:]
        positions_path = "" #  enter path to positions.json file of that is the output of the vessel navigator
        with open(positions_path, "r") as infile:
            positions = json.load(infile)

        if len(positions) != len(groundtruth):
            raise ValueError("position estimates and groundtruth must feature same length")

        branch_per_update_step = [0 for _ in range(len(groundtruth))]

        #  ENTER CORRECT BRANCH ESTIMATE PER UPDATE STEP IN branch_per_update_step LIST
        print(groundtruth)
        for i, el in enumerate(groundtruth):
            if el < 90:
                branch_per_update_step[i] = 0
            elif 90 <= el < 100:
                branch_per_update_step[i] = 1
            elif 100 <= el < 120:
                branch_per_update_step[i] = 2
            elif 120 <= el < 130:
                branch_per_update_step[i] = 3
            elif 130 <= el < 200:
                branch_per_update_step[i] = 4
            else:
                branch_per_update_step[i] = 5

        number_of_correct_branch_estimations = 0
        est = []


        for i, el in enumerate(branch_per_update_step):
            est.append(positions[str(i)][1])
            if el == 5 or el == 6 and positions[str(i)][1] == 5 or positions[str(i)][1] == 6:
                number_of_correct_branch_estimations += 1
            elif positions[str(i)][1] == el:
                number_of_correct_branch_estimations += 1




        print(SETUP + " sample nr: " + sample_nr + " correct estimates " + str(number_of_correct_branch_estimations))
        branch_accuracy[SETUP].append(number_of_correct_branch_estimations / len(positions))
        print(branch_per_update_step)
        print(est)
        print("\n\n")

with open(DESTINATION + "agar_I_" + "_branch_accuracy.pkl", 'wb') as f:
    pickle.dump(branch_accuracy, f)

result = stats.ttest_rel(branch_accuracy["AHISTORIC"], branch_accuracy["SLIDING_DTW"])

with open(DESTINATION + "agar_I_" + "_statistics.txt", 'w') as f:
    f.write("mean AHISTORIC: " + str(np.mean(branch_accuracy["AHISTORIC"])) + "\n")
    f.write("stdev AHISTORIC: " + str(np.std(branch_accuracy["AHISTORIC"])) + "\n")
    f.write("mean SLIDING_DTW: " + str(np.mean(branch_accuracy["SLIDING_DTW"])) + "\n")
    f.write("stdev SLIDING_DTW: " + str(np.std(branch_accuracy["SLIDING_DTW"])) + "\n")
    f.write("t-test related AHISTORIC vs. SLIDING_DTW: " + str(result))

