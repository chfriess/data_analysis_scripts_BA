import json
import math
import statistics

import numpy as np
from scipy import ndimage

BRANCH = "side"

BASE_PATH = "C:\\Users\\Chris\\OneDrive\\Desktop\\tilt_phantom\\"
SIGNAL_NAME = BRANCH + " branch old setup\\catheter_trajectory_original_simulated_signal_staticel_sidebr_0p7vs0p05_npz"
CENTERLINE_NAME = "catheter_trajectory_main.json"
DESTINATION_FILENAME = BRANCH + " branch old setup\\smoothed_standardised_simulated_reference_agar_sbos07005"


def normalize_values(d: list) -> list:
    mu = statistics.mean(d)
    sigma = statistics.stdev(d)
    for i, el in enumerate(d):
        d[i] = (el - mu) / sigma
    return d


def project_signal_index_on_centerline_index(signal_index: int) -> int:
    if BRANCH == "side":
        return signal_index * 10 + 169
    if BRANCH == "main":
        return signal_index * 10 + 179


def distance_3D(x1: np.ndarray, x2: np.ndarray):
    return math.sqrt(((x2[0] - x1[0]) ** 2) + ((x2[1] - x1[1]) ** 2) + ((x2[2] - x1[2]) ** 2))


data = np.load(BASE_PATH + SIGNAL_NAME)
signal = data['simulated_diff_signal']
el_distances = data['det_el_distances']

signal_compensated = signal / el_distances
signal_compensated = ndimage.gaussian_filter1d(signal_compensated, 2)
signal_compensated = np.array((normalize_values(list(signal_compensated))))

cumulative_distances_of_centerline_points = [0]
signal_per_centerline_position = []

with open(BASE_PATH + CENTERLINE_NAME, "r") as infile:
    centerline = json.load(infile)
    centerline_points = centerline["markups"][0]["controlPoints"]

    for i in range(1, len(centerline_points)):
        point_one = np.array(centerline_points[i]["position"])
        point_two = np.array(centerline_points[i - 1]["position"])
        next_p2p_distance = distance_3D(point_one, point_two)
        next_point_position = cumulative_distances_of_centerline_points[i - 1] + next_p2p_distance
        cumulative_distances_of_centerline_points.append(next_point_position)

for i, signal_value in enumerate(signal_compensated):
    centerline_index = project_signal_index_on_centerline_index(i)
    centerline_position = cumulative_distances_of_centerline_points[centerline_index]
    next_position_reference_pair = {"centerline_position": centerline_position, "reference_signal": signal_value}
    signal_per_centerline_position.append(next_position_reference_pair)

reference = {"signal_per_centerline_position": signal_per_centerline_position}
jo = json.dumps(reference, indent=4)

with open(BASE_PATH + DESTINATION_FILENAME + ".json", "w") as outfile:
    outfile.write(jo)
