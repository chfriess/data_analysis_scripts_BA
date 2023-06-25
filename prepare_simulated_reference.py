import json
import math

import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage

BASE_PATH = "C:\\Users\\Chris\\OneDrive\\Desktop\\Bachelorarbeit\\simulated_reference\\"
SIGNAL_NAME = "catheter_trajectory_original_simulated_signal_longercut_0p95_npz"
CENTERLINE_NAME = "original centerline.json"
DESTINATION_FILENAME = "smoothed_simulated_reference_agar"


def project_signal_index_on_centerline_index(signal_index: int) -> int:
    return signal_index * 10 + 168


def distance_3D(x1: np.ndarray, x2: np.ndarray):
    return math.sqrt(((x2[0] - x1[0]) ** 2) + ((x2[1] - x1[1]) ** 2) + ((x2[2] - x1[2]) ** 2))


data = np.load(BASE_PATH + SIGNAL_NAME)
signal = data['simulated_diff_signal']
el_distances = data['det_el_distances']

signal = ndimage.gaussian_filter1d(signal, 2)

signal_compensated = signal / el_distances
cumulative_distances_of_centerline_points = [0]
signal_per_centerline_position = []

with open(BASE_PATH + CENTERLINE_NAME, "r") as infile:
    centerline = json.load(infile)
    centerline_points = centerline["markups"][0]["controlPoints"]

    for i in range(1, len(centerline_points)):
        point_one = np.array(centerline_points[i]["position"])
        point_two = np.array(centerline_points[i - 1]["position"])
        next_p2p_distance = distance_3D(point_one, point_two)
        next_point_position = cumulative_distances_of_centerline_points[i-1] + next_p2p_distance
        cumulative_distances_of_centerline_points.append(next_point_position)


for i, signal_value in enumerate(signal_compensated):
    centerline_index = project_signal_index_on_centerline_index(i)
    centerline_position = cumulative_distances_of_centerline_points[centerline_index]
    next_position_reference_pair = {"centerline_position": centerline_position, "reference_signal": signal_value}
    signal_per_centerline_position.append(next_position_reference_pair)

print(cumulative_distances_of_centerline_points)


reference = {"signal_per_centerline_position": signal_per_centerline_position}
jo = json.dumps(reference, indent=4)

with open(BASE_PATH + DESTINATION_FILENAME + ".json", "w") as outfile:
    outfile.write(jo)
