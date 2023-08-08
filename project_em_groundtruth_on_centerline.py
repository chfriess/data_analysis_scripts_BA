import csv
import math

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# ADD CENTERLINES AS STRAIGHT LINES; DEFINED BY TWO 3D POINTS
CENTERLINE_AORTA_BASIS = np.array([24.9633, -111.474, -257.823])
CENTERLINE_AORTA_TOP = np.array([33.7898, 88.3246, -259.437])
AORTA = {'BASIS': CENTERLINE_AORTA_BASIS, 'TOP': CENTERLINE_AORTA_TOP}

CENTERLINE_ILIACA_UPPER_BASIS = np.array([33.7898, 88.3246, -259.437])
CENTERLINE_ILIACA_UPPER_TOP = np.array([-28.282, 154.153, -256.653])
ILIACA_UPPER = {'BASIS': CENTERLINE_ILIACA_UPPER_BASIS, 'TOP': CENTERLINE_ILIACA_UPPER_TOP}

ILIACA = ILIACA_UPPER
ILIACA_BASIS = CENTERLINE_ILIACA_UPPER_BASIS
ILIACA_TOP = CENTERLINE_ILIACA_UPPER_TOP

# offset between EM and bioelectric catheter tip 23mm
OFFSET = 23

PROJECTION_MERKER = []
DISPLACEMENTS_FROM_ORIGIN = []

OFFSET_CORRECTED_POINTS = []


def closest_point_on_vessel_centerline(vessel: dict, point: np.ndarray):
    x1 = vessel['BASIS']
    x2 = vessel['TOP']
    ap = point - x1
    ab = x2 - x1
    result = x1 + np.dot(ap, ab) / np.dot(ab, ab) * ab
    return result


def closest_point_on_line(start: np.ndarray, end: np.ndarray, point: np.ndarray) -> np.ndarray:
    ap = point - start
    ab = end - start
    result = start + np.dot(ap, ab) / np.dot(ab, ab) * ab
    return result


def is_point_on_line_between_points(start: np.ndarray, end: np.ndarray, point: np.ndarray):
    return abs((distance_3D(start, point) + distance_3D(point, end)) - distance_3D(start, end)) < 0.001


def distance_of_point_from_line(vessel: dict, point: np.ndarray):
    x1 = vessel['BASIS']
    x2 = vessel['TOP']
    if is_point_on_line_between_points(start=x1, end=x2, point=closest_point_on_line(start=x1, end=x2, point=point)):
        return np.linalg.norm(np.cross(x2 - x1, x1 - point)) / np.linalg.norm(x2 - x1)
    else:
        vertical_distance = np.linalg.norm(np.cross(x2 - x1, x1 - point)) / np.linalg.norm(x2 - x1)
        projected_point = closest_point_on_line(start=x1, end=x2, point=point)
        distance_from_start = distance_3D(projected_point, x1)
        distance_from_end = distance_3D(projected_point, x2)
        if distance_from_start < distance_from_end:
            return vertical_distance + distance_from_start
        else:
            return vertical_distance + distance_from_end


def distance_3D(x1: np.ndarray, x2: np.ndarray):
    return math.sqrt(((x2[0] - x1[0]) ** 2) + ((x2[1] - x1[1]) ** 2) + ((x2[2] - x1[2]) ** 2))


def move_single_point_in_direction_of_probe_orientation(point: np.ndarray, orientation: np.ndarray, distance: float):
    x = point[0] + orientation[0] * distance
    y = point[1] + orientation[1] * distance
    z = point[2] + orientation[2] * distance

    return np.array([x, y, z])


def correct_offset(row: np.ndarray):
    point = row[12:15]
    orientation = row[8:11]
    moved_point = move_single_point_in_direction_of_probe_orientation(point=point,
                                                                      orientation=orientation,
                                                                      distance=OFFSET)

    OFFSET_CORRECTED_POINTS.append(moved_point.tolist())


def project_single_point_on_centerline(point: np.ndarray):
    if distance_of_point_from_line(vessel=ILIACA, point=point) <= distance_of_point_from_line(vessel=AORTA,
                                                                                              point=point):
        closest_point = closest_point_on_vessel_centerline(vessel=ILIACA, point=point)

        DISPLACEMENTS_FROM_ORIGIN.append(distance_3D(closest_point, ILIACA_TOP))
        PROJECTION_MERKER.append(closest_point.tolist())
    else:
        closest_point = closest_point_on_vessel_centerline(vessel=AORTA, point=point)
        DISPLACEMENTS_FROM_ORIGIN.append(
            distance_3D(closest_point, CENTERLINE_AORTA_TOP) + distance_3D(ILIACA_TOP, ILIACA_BASIS))
        PROJECTION_MERKER.append(closest_point.tolist())


def project_points_on_centerlines(COREGISTRATION_SOURCE: str,
                                  COREGISTRATION_DESTINATION: str,
                                  BEFORE_CORRECTION: str,
                                  AFTER_CORRECTION: str,
                                  DISPLACEMENT_DESTINATION: str,
                                  FIGURE_DESTINATION: str):
    df_before_projection = pd.read_csv(COREGISTRATION_SOURCE, sep='\t')
    df_test = df_before_projection.iloc[:, 12:15]
    df_test.to_csv(
        BEFORE_CORRECTION + ".csv",
        sep=' ', quoting=csv.QUOTE_NONE, escapechar=' ', index=False,
        header=False)

    np.savetxt(BEFORE_CORRECTION + ".txt", df_test.values, fmt='%f')
    df_before_projection.apply(correct_offset, axis=1)

    df = pd.DataFrame(OFFSET_CORRECTED_POINTS)
    df.to_csv(
        AFTER_CORRECTION + ".csv",
        sep=' ', quoting=csv.QUOTE_NONE, escapechar=' ', index=False,
        header=False)
    np.savetxt(AFTER_CORRECTION + ".txt", df.values, fmt='%f')
    df.apply(project_single_point_on_centerline, axis=1)
    plt.plot(DISPLACEMENTS_FROM_ORIGIN)
    plt.savefig(FIGURE_DESTINATION)
    np.save(DISPLACEMENT_DESTINATION, DISPLACEMENTS_FROM_ORIGIN)

    df_after_projection = pd.DataFrame(PROJECTION_MERKER)
    df_after_projection.to_csv(COREGISTRATION_DESTINATION + ".csv", sep=' ', quoting=csv.QUOTE_NONE, escapechar=' ',
                               index=False,
                               header=False)
    np.savetxt(COREGISTRATION_DESTINATION + ".txt", df_after_projection.values, fmt='%f')


if __name__ == "__main__":
    for sample_nr in []:  # ENTER SAMPLE NRs
        COREGISTRATION_SOURCE = "" + sample_nr + "\\coregistration_" + sample_nr + "_em.csv"  # ENTER PATH
        COREGISTRATION_DESTINATION = "" + sample_nr + "\\groundtruth_coordinates_after_projection"  # ENTER PATH
        COREGISTRATION_BEFORE_CORRECTION = "" + sample_nr + "\\groundtruth_coordinates_before_correction"  # ENTER PATH
        COREGISTRATION_AFTER_CORRECTION = "" + sample_nr + "\\groundtruth_coordinates_after_correction"  # ENTER PATH
        DISPLACEMENT_DESTINATION = "" + sample_nr + "\\displacement_from_origin.npy"  # ENTER PATH
        FIGURE_DESTINATION = "" + sample_nr + "\\displacement_from_origin.svg"  # ENTER PATH

        project_points_on_centerlines(COREGISTRATION_SOURCE=COREGISTRATION_SOURCE,
                                      COREGISTRATION_DESTINATION=COREGISTRATION_DESTINATION,
                                      BEFORE_CORRECTION=COREGISTRATION_BEFORE_CORRECTION,
                                      AFTER_CORRECTION=COREGISTRATION_AFTER_CORRECTION,
                                      DISPLACEMENT_DESTINATION=DISPLACEMENT_DESTINATION,
                                      FIGURE_DESTINATION=FIGURE_DESTINATION)

        plt.clf()
        PROJECTION_MERKER = []
        DISPLACEMENTS_FROM_ORIGIN = []
        OFFSET_CORRECTED_POINTS = []
