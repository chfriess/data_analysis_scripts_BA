import math
import numpy as np
import os
import csv
import statistics

import matplotlib.pyplot as plt

FREQUENCIES = [500, 1000, 2000, 5000, 10000]
MOLARITY = ["0005M", "001M", "003M", "005M", "015M"]
COLORS = ["black", "blue", "green", "red", "orange"]
LITERATURE = [0.047, 0.094, 0.281, 0.466, 1.375]


# assumption: delta T is constant
def rms(signal: np.ndarray) -> float:
    sum = 0
    for value in signal:
        sum += value ** 2
    sum /= len(signal)
    return math.sqrt(sum)


def plot_conductance_vs_frequency(signal: list, c: str, l: str):
    if (len(signal) != len(FREQUENCIES)):
        raise ValueError("every frequency needs one value, every value needs one frequency")
    plt.scatter(FREQUENCIES[0], signal[0], color=c, label=l)
    plt.plot(FREQUENCIES, signal, color=c)
    for i in range(1, len(signal)):
        plt.scatter(FREQUENCIES[i], signal[i], color=c)


def calculate_current(voltage_over_resistor: np.ndarray, resistor: float) -> float:
    voltage = rms(voltage_over_resistor) / 1000
    return voltage / resistor


def save_conductance_as_csv(signal: list):
    pass


def calculate_conductance(current: float, molarity: str) -> list:
    base_path = ""
    end_path = ""
    conductances = []

    for f in FREQUENCIES:
        voltage_over_inner_pair = np.load(base_path + molarity + "\\result\\" + str(f) + "Hz" + end_path)
        # voltage in mv
        v = rms(voltage_over_inner_pair) / 1000
        conductances.append(1 / (v / current))
    return conductances


if __name__ == '__main__':
    signal_for_current_calculation = np.load("")
    current = calculate_current(signal_for_current_calculation, 243)

    os.chdir("")

    f = open('conductances.csv', 'w')

    writer = csv.writer(f)
    writer.writerow(["Molarity"] + FREQUENCIES + ["mean G(s)", "sd G(S)"])

    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Conductance [S]")

    all_conductances = []

    for i in range(5):
        conductances = calculate_conductance(current, MOLARITY[i])
        all_conductances.append(conductances)
        plot_conductance_vs_frequency(conductances, COLORS[i], MOLARITY[i])

        conductances.append(statistics.mean(conductances))
        conductances.append(statistics.stdev(conductances))
        conductances.insert(0, MOLARITY[i])
        writer.writerow(conductances)

    plt.legend()
    plt.savefig("conductance_vs_frequencies.svg")

    f.close()

    """
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Conductance (S)")

    signal_0005 = [1, 1.1, 1, 0.9, 1]
    signal_001  = [3, 3, 3.1, 3, 2.9]

    plot_conductance_vs_frequency(signal_0005, "blue", "0.005M" )
    plot_conductance_vs_frequency(signal_001, "red", "0.01M" )

    plt.legend()
    plt.show()


    signal_0005 = [1, 1, 1.1, 1, 0.9, 1]
    signal_001  = [3, 3, 3.1, 3, 2.9, 3]
    signal_003  = [5, 5, 5.1, 5, 4.9, 5]
    signal_005  = [7, 7, 7.1, 7, 6.9, 7]
    signal_015  = [9, 9, 9.1, 9, 8.9, 9]

    plt.plot(signal_0005, label="0.005M", color="blue")
    for i in range(len(signal_0005)):
        plt.scatter(i, signal_0005[i], color="blue")

    plt.plot(signal_001, label="0.01M", color="green")
    for i in range(len(signal_001)):
        plt.scatter(i, signal_001[i], color="green")


    plt.plot(signal_003, label="0.03M", color="red")
    for i in range(len(signal_003)):
        plt.scatter(i, signal_003[i], color="red")


    plt.plot(signal_005, label="0.05M", color="orange")
    for i in range(len(signal_005)):
        plt.scatter(i, signal_005[i], color="orange")

    plt.plot(signal_015, label="0.15M",color="purple")
    for i in range(len(signal_015)):
        plt.scatter(i, signal_015[i], color="purple")

    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Conductance (S)")

    plt.legend()
    plt.show()
    """

