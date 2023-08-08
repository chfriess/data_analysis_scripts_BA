import math
import numpy as np
from matplotlib import pyplot as plt

FREQUENCIES = [500, 1000, 2000, 5000, 10_000, 20_000, 50_000]

CELL_CONSTANT = 0.005869712999883455
CC_STDEV = 0.0014405813130868863


def rms(signal: np.ndarray) -> float:
    acc = 0
    for value in signal:
        acc += value ** 2
    acc /= len(signal)
    return math.sqrt(acc)


def calculate_current(voltage_over_resistor: np.ndarray, resistor: float) -> float:
    voltage = rms(determine_and_subtract_signal_mean(voltage_over_resistor)) / 1000
    return voltage / resistor


def plot_phase():
    resistor_path = ""  # ENTER RESISTOR PATH
    voltage_over_resistor = np.load(resistor_path)
    plt.plot(voltage_over_resistor)

    inner_pair_path = ""  # ENTER PATH TO VOLTAGE OVER INNER PAIR

    voltage_over_inner_pair_signal = np.load(inner_pair_path)
    plt.plot(voltage_over_inner_pair_signal, color="red")
    plt.show()


def determine_and_subtract_signal_mean(signal: np.ndarray) -> np.ndarray:
    mean = np.mean(signal)
    result = []
    for x in signal:
        result.append(x - mean)
    return np.array(result)


def calculate_conductance() -> float:
    # calculate output current at specific frequency/molarity combination
    resistor_path = ""  # ENTER RESISTOR PATH
    voltage_over_resistor = np.load(resistor_path)
    current = calculate_current(voltage_over_resistor=voltage_over_resistor, resistor=480)
    # calculate conductance of specific frequency/molarity combination
    inner_pair_path = ""  # ENTER PATH TO VOLTAGE OVER INNER PAIR

    voltage_over_inner_pair_signal = np.load(inner_pair_path)

    voltage_over_inner_pair = rms(determine_and_subtract_signal_mean(voltage_over_inner_pair_signal)) / 1000
    return current / voltage_over_inner_pair
