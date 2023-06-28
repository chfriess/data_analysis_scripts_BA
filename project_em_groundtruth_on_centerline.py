import csv
import math

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

CENTERLINE_AORTA_BASIS = np.array([26.9584, -136.889, -325.379])
CENTERLINE_AORTA_TOP = np.array([30.2799, 62.9124, -333.653])
AORTA = {'BASIS': CENTERLINE_AORTA_BASIS, 'TOP': CENTERLINE_AORTA_TOP}

# CENTERLINE_ILIACA_LOWER_BASIS = np.array([12.5576, 52.093, -275.282])
# CENTERLINE_ILIACA_LOWER_TOP = np.array([75.6866, 115.839, -263.231])
# ILIACA_LOWER = {'BASIS': CENTERLINE_ILIACA_LOWER_BASIS, 'TOP': CENTERLINE_ILIACA_LOWER_TOP}

CENTERLINE_ILIACA_UPPER_BASIS = np.array([30.2799, 62.9124, -333.653])
CENTERLINE_ILIACA_UPPER_TOP = np.array([88.0561,	118.787,	-335.968])
ILIACA_UPPER = {'BASIS': CENTERLINE_ILIACA_UPPER_BASIS, 'TOP': CENTERLINE_ILIACA_UPPER_TOP}

SIDE_BRANCH_BASIS = np.array([28.7437, -29.4956, -329.826])
SIDE_BRANCH_TOP = np.array([-53.0332, -75.5902, -327.574])
SIDE_BRANCH = {'BASIS': SIDE_BRANCH_BASIS, 'TOP': SIDE_BRANCH_TOP}

ILIACA = ILIACA_UPPER
ILIACA_BASIS = CENTERLINE_ILIACA_UPPER_BASIS
ILIACA_TOP = CENTERLINE_ILIACA_UPPER_TOP

PROJECTION_MERKER = []
DISPLACEMENTS_FROM_ORIGIN = []

OFFSET = 25


def closest_point_on_line(vessel: dict, point: np.ndarray):
    x1 = vessel['BASIS']
    x2 = vessel['TOP']
    ap = point - x1
    ab = x2 - x1
    result = x1 + np.dot(ap, ab) / np.dot(ab, ab) * ab
    return result


def distance_of_point_from_line(vessel: dict, point: np.ndarray):
    x1 = vessel['BASIS']
    x2 = vessel['TOP']
    return np.linalg.norm(np.cross(x2 - x1, x1 - point)) / np.linalg.norm(x2 - x1)


def distance_3D(x1: np.ndarray, x2: np.ndarray):
    return math.sqrt(((x2[0] - x1[0]) ** 2) + ((x2[1] - x1[1]) ** 2) + ((x2[2] - x1[2]) ** 2))


def read_em_coregistration_csv(path: str):
    df = pd.read_csv(path, sep=',')
    return df


def project_single_point_on_centerline(point: np.ndarray):
    if distance_of_point_from_line(vessel=ILIACA, point=point) <= distance_of_point_from_line(vessel=AORTA,
                                                                                              point=point) \
            and distance_of_point_from_line(vessel=AORTA, point=point) <= distance_of_point_from_line(
        vessel=SIDE_BRANCH, point=point):
        closest_point = closest_point_on_line(vessel=ILIACA, point=point)
        # if closest_point[1] < ILIACA_TOP[1]:
        # DISPLACEMENTS_FROM_ORIGIN.append(-distance_3D(closest_point, ILIACA_TOP))
        # else:
        DISPLACEMENTS_FROM_ORIGIN.append(distance_3D(closest_point, ILIACA_TOP))
        PROJECTION_MERKER.append(closest_point.tolist())
    elif distance_of_point_from_line(vessel=SIDE_BRANCH, point=point) <= distance_of_point_from_line(vessel=ILIACA,
                                                                                                     point=point) \
            and distance_of_point_from_line(vessel=SIDE_BRANCH, point=point) <= distance_of_point_from_line(
        vessel=AORTA,
        point=point):
        closest_point = closest_point_on_line(vessel=SIDE_BRANCH, point=point)
        DISPLACEMENTS_FROM_ORIGIN.append(
            distance_3D(closest_point, SIDE_BRANCH_BASIS) + distance_3D(CENTERLINE_AORTA_TOP,
                                                                        SIDE_BRANCH_BASIS) + distance_3D(ILIACA_TOP,
                                                                                                         ILIACA_BASIS))

        PROJECTION_MERKER.append(closest_point.tolist())
    else:
        closest_point = closest_point_on_line(vessel=AORTA, point=point)
        DISPLACEMENTS_FROM_ORIGIN.append(
            distance_3D(closest_point, CENTERLINE_AORTA_TOP) + distance_3D(ILIACA_TOP, ILIACA_BASIS))
        PROJECTION_MERKER.append(closest_point.tolist())
        print("distance =" + str(distance_3D(ILIACA_TOP, ILIACA_BASIS)))
    """
    
    """


def project_points_on_centerlines(COREGISTRATION_SOURCE: str,
                                  COREGISTRATION_DESTINATION: str,
                                  DISPLACEMENT_DESTINATION: str,
                                  FIGURE_DESTINATION: str):
    df_before_projection = pd.read_csv(COREGISTRATION_SOURCE, sep='\t')
    df = df_before_projection.iloc[:, 12:15]
    df.apply(project_single_point_on_centerline, axis=1)
    plt.plot(DISPLACEMENTS_FROM_ORIGIN)
    plt.savefig(FIGURE_DESTINATION)
    np.save(DISPLACEMENT_DESTINATION, DISPLACEMENTS_FROM_ORIGIN)

    df_after_projection = pd.DataFrame(PROJECTION_MERKER)
    df_after_projection.to_csv(COREGISTRATION_DESTINATION, sep=' ', quoting=csv.QUOTE_NONE, escapechar=' ', index=False,
                               header=False)


if __name__ == "__main__":
    sample_nr = "1"

    # for sample_nr in [str(x) for x in range(1, 11)]:
    COREGISTRATION_SOURCE = "C:\\Users\\Chris\\OneDrive\\Desktop\\tilt_phantom\\main branch new setup\\sample_" + sample_nr + "\\em_groundtruth\\coregistration_" + sample_nr + "_em.csv"
    COREGISTRATION_DESTINATION = "C:\\Users\\Chris\\OneDrive\\Desktop\\tilt_phantom\\main branch new setup\\sample_" + sample_nr + "\\em_groundtruth\\groundtruth_coordinates_after_projection.csv"
    DISPLACEMENT_DESTINATION = "C:\\Users\\Chris\\OneDrive\\Desktop\\tilt_phantom\\main branch new setup\\sample_" + sample_nr + "\\em_groundtruth\\displacement_from_origin.npy"
    FIGURE_DESTINATION = "C:\\Users\\Chris\\OneDrive\\Desktop\\tilt_phantom\\main branch new setup\\sample_" + sample_nr + "\\em_groundtruth\\displacement_from_origin.svg"

    project_points_on_centerlines(COREGISTRATION_SOURCE=COREGISTRATION_SOURCE,
                                  COREGISTRATION_DESTINATION=COREGISTRATION_DESTINATION,
                                  DISPLACEMENT_DESTINATION=DISPLACEMENT_DESTINATION,
                                  FIGURE_DESTINATION=FIGURE_DESTINATION)

    plt.clf()
    PROJECTION_MERKER = []
    DISPLACEMENTS_FROM_ORIGIN = []
