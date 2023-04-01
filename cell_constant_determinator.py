import math
import numpy as np
import os
import csv
import statistics

import matplotlib.pyplot as plt

FREQUENCIES = [500, 1000, 2000, 5000, 10_000, 20_000, 50_000]
NUMBER_OF_FREQUENCIES = 7
MOLARITY = [0.005, 0.01, 0.03, 0.05, 0.15]
NUMBER_OF_MOLARITIES = 5
COLORS = ["black", "blue", "green", "red", "orange"]
LITERATURE = [0.047, 0.094, 0.281, 0.466, 1.375]
CONDUCTANCES = {}
CONDUCTIVITIES = {}


def init_conductance_dict():
    for i in range(len(MOLARITY)):
        CONDUCTANCES[MOLARITY[i]] = []


def init_conductivity_dict():
    for i in range(len(MOLARITY)):
        CONDUCTIVITIES[MOLARITY[i]] = []


def rms(signal: np.ndarray) -> float:
    acc = 0
    for value in signal:
        acc += value ** 2
    acc /= len(signal)
    return math.sqrt(acc)


def calculate_current(voltage_over_resistor: np.ndarray, resistor: float) -> float:
    voltage = rms(voltage_over_resistor) / 1000
    return voltage / resistor


def calculate_conductance(frequency: int, molarity: float) -> float:
    pass


def calculate_cell_constant():
    init_conductance_dict()
    cell_constant_predictions = []
    for f in range(NUMBER_OF_FREQUENCIES):
        for m in range(NUMBER_OF_MOLARITIES):
            g = calculate_conductance(FREQUENCIES[f], MOLARITY[m])
            CONDUCTANCES[MOLARITY].append(g)
            cell_constant_predictions.append(g / LITERATURE[m])
    return statistics.mean(cell_constant_predictions)


def predict_conductivity():
    init_conductivity_dict()
    CELL_CONSTANT = calculate_cell_constant()
    print("CELL CONSTANT = ", CELL_CONSTANT)
    # TODO: save CELL CONSTANT
    for key in CONDUCTANCES.keys():
        CONDUCTIVITIES[key].append(CONDUCTANCES[key] / CELL_CONSTANT)


def save_conductance_and_conductivites_as_csv():
    """
    save conductance and predicted conductivity as csv
    """
    pass


def save_data_analysis_conductivity_and_conductance_as_csv():
    """
    [NaCl]  G(S) average    G(S) SD    G(S) % SD    sigma average    sigma peyman   sigma percentage difference to literature
    :return:
    """
    pass


def save_average_frequency_dependent_conductivity_error_as_csv():
    pass


def plot_conductances():
    pass


def plot_conductivities_with_benchmark():
    pass


if __name__ == '__main__':
    pass
