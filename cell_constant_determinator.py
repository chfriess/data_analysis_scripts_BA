import math
import numpy as np
import os
import csv
import statistics

import matplotlib.pyplot as plt

PATH = "C:\\Users\\Chris\\OneDrive\\Desktop\\sweep_record\\"
RESULT_PATH = "C:\\Users\\Chris\\OneDrive\\Desktop\\sweep_record\\results\\results_without_scaling_error\\"
FREQUENCIES = [500, 1000, 2000, 5000, 10_000, 20_000, 50_000]
NUMBER_OF_FREQUENCIES = 7
MOLARITY = [0.005, 0.01, 0.03, 0.05, 0.15]
MOLARITY_MAP = {
    0.005: "0005M", 0.01: "001M", 0.03: "003M", 0.05: "005M", 0.15: "015M"
}
NUMBER_OF_MOLARITIES = 5
COLORS = ["purple", "blue", "green", "red", "orange"]
LITERATURE = [0.047, 0.094, 0.281, 0.466, 1.375]
CONDUCTANCES = {}
CONDUCTIVITIES = {}
CURRENTS = []


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
    voltage = rms(determine_and_subtract_signal_mean(voltage_over_resistor)) / 1000
    return voltage / resistor


def determine_and_subtract_signal_mean(signal: np.ndarray) -> np.ndarray:
    mean = np.mean(signal)
    result = []
    for x in signal:
        result.append(x-mean)
    return np.array(result)


def calculate_conductance(frequency: int, molarity: float) -> float:
    # calculate output current at specific frequency/molarity combination
    #TODO: reset the molarity == 0.2 to 0.15?
    if molarity == 0.15:
        resistor_path = PATH + "001M" + "\\cropped_voltage_over_resistor" + "\\voltage_over_resistor_"
        resistor_path += "001M" + "_" + str(frequency) + "Hz.npy"
    else:
        resistor_path = PATH + MOLARITY_MAP[molarity] + "\\cropped_voltage_over_resistor" + "\\voltage_over_resistor_"
        resistor_path += MOLARITY_MAP[molarity] + "_" + str(frequency) + "Hz.npy"

    voltage_over_resistor = np.load(resistor_path)
    current = calculate_current(voltage_over_resistor=voltage_over_resistor, resistor=480)
    CURRENTS.append(current)

    # calculate conductance of specific frequency/molarity combination
    inner_pair_path = PATH + MOLARITY_MAP[molarity] + "\\after_crop" + "\\voltage_over_inner_pair_"
    inner_pair_path += str(frequency) + "_Hz_decomposed_.npy"
    voltage_over_inner_pair_signal = np.load(inner_pair_path)

    voltage_over_inner_pair = rms(determine_and_subtract_signal_mean(voltage_over_inner_pair_signal)) / 1000

    return current / voltage_over_inner_pair


def calculate_cell_constant():
    init_conductance_dict()
    cell_constant_predictions_per_frequency = {}
    cell_constant_predictions = []
    for f in range(len(FREQUENCIES)):
        cell_constant_predictions_per_frequency[f] = []
    for m in range(NUMBER_OF_MOLARITIES):
        for f in range(NUMBER_OF_FREQUENCIES):
            g = calculate_conductance(FREQUENCIES[f], MOLARITY[m])
            CONDUCTANCES[MOLARITY[m]].append(g)
            cell_constant_predictions.append((g / LITERATURE[m]))
            cell_constant_predictions_per_frequency[f].append((g / LITERATURE[m]))
    print("cell constant predictions: ")
    for c in cell_constant_predictions_per_frequency.values():
        print(c)

    print("\n\n")
    cell_constant = statistics.mean(cell_constant_predictions)
    with open(RESULT_PATH + 'cell_constant.txt', 'w') as file:
        file.write("CELL CONSTANT = " + str(cell_constant) + "\n")
        file.write("CELL CONSTANT STDEV = " + str(statistics.stdev(cell_constant_predictions))+ "\n\n\n\n")

        for f in range(len(FREQUENCIES)):
            file.write("Cell constant for " + str(FREQUENCIES[f]) + ": " + str(statistics.mean(cell_constant_predictions_per_frequency[f]))+ "\n")
            file.write("Cell constant stdev for " + str(FREQUENCIES[f]) + ": " + str(statistics.stdev(cell_constant_predictions_per_frequency[f]))+ "\n\n")


    return cell_constant


def predict_conductivity():
    init_conductivity_dict()
    cell_constant = calculate_cell_constant()
    # TODO: save CELL CONSTANT
    for key in CONDUCTANCES.keys():
        for conductance in CONDUCTANCES[key]:
            CONDUCTIVITIES[key].append(conductance / cell_constant)


def save_conductance_and_conductivites_as_csv():
    """
    save conductance and predicted conductivity as csv
    """
    with open(RESULT_PATH + 'conductances.csv', 'w', newline='') as csvfile:
        conductance_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        conductance_writer.writerow(["Molarity"] + [str(x) for x in FREQUENCIES])
        for key in CONDUCTANCES.keys():
            conductance_writer.writerow([key] + CONDUCTANCES[key])

    with open(RESULT_PATH + 'conductivity.csv', 'w', newline='') as csvfile:
        conductivity_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        conductivity_writer.writerow(["Molarity"] + [str(x) for x in FREQUENCIES])
        for key in CONDUCTIVITIES.keys():
            conductivity_writer.writerow([key] + CONDUCTIVITIES[key])


def save_data_analysis_conductivity_and_conductance_as_csv():
    """
    [NaCl]  G(S) average    G(S) SD    G(S) % SD    sigma average    sigma peyman
    sigma percentage difference to literature
    :return:
    """
    with open(RESULT_PATH + 'complete_analysis.csv', 'w', newline='') as csvfile:
        conductivity_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        conductivity_writer.writerow(["Molarity"] + ["G(S) average"] + ["G(S) % SD"])
        for key in CONDUCTANCES.keys():
            conductivity_writer.writerow(
                [key] + [statistics.mean(CONDUCTANCES[key])] + [statistics.stdev(CONDUCTANCES[key])])

        conductivity_writer.writerow(
            ["Molarity"]+["sigma average"] + ["sigma stddev"] + ["sigma peyman"] + ["sigma perc difference to peyman"])
        i = 0
        for key in CONDUCTIVITIES.keys():
            conductivity_writer.writerow(
                [key] +
                [statistics.mean(CONDUCTIVITIES[key])] +
                [statistics.stdev(CONDUCTIVITIES[key])] +
                [LITERATURE[i]] +
                [((statistics.mean(CONDUCTIVITIES[key]) - LITERATURE[i])/LITERATURE[i]) * 100])
            i += 1


def plot_conductances():
    i = 0
    plt.ylabel("conductance (S)")
    plt.xlabel("frequency [Hz]")
    for key in CONDUCTANCES.keys():
        plt.plot(FREQUENCIES, CONDUCTANCES[key], color=COLORS[i], label=MOLARITY_MAP[key])
        plt.scatter(FREQUENCIES, CONDUCTANCES[key], color=COLORS[i])
        i += 1
    plt.legend()
    plt.savefig(RESULT_PATH + 'conductance.svg')


def plot_conductivities_with_benchmark():
    plt.clf()
    i = 0
    plt.ylabel("conductivity (S/m)")
    plt.xlabel("frequency [Hz]")
    for key in CONDUCTIVITIES.keys():
        plt.plot(FREQUENCIES, CONDUCTIVITIES[key], color=COLORS[i], label=MOLARITY_MAP[key])
        plt.scatter(FREQUENCIES, CONDUCTIVITIES[key], color=COLORS[i])
        i += 1

    plt.legend()
    plt.savefig(RESULT_PATH + 'conductivity.svg')


def calculate_current_mean_and_stdev():
    mean = statistics.mean(CURRENTS)
    stdev = statistics.stdev(CURRENTS)
    with open(RESULT_PATH + 'current_mean_and_stddev.txt', 'w') as file:
        file.write("mean current = " + str(mean) + "\n")
        file.write("mean stdev current = " + str(stdev))


def calculate_cell_constant_and_conductivity():
    predict_conductivity()
    save_conductance_and_conductivites_as_csv()
    save_data_analysis_conductivity_and_conductance_as_csv()
    plot_conductances()
    #plot_conductivities_with_benchmark()



if __name__ == '__main__':
    calculate_cell_constant_and_conductivity()
    calculate_current_mean_and_stdev()
