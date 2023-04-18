import math
import statistics

import numpy as np


FREQUENCIES = [500, 1000, 2000, 5000, 10_000, 20_000, 50_000]
MOLARITY = "005M"
DESTINATION = "C:\\Users\\Chris\\OneDrive\\Desktop\\sweep_record\\agar_"+MOLARITY+"\\conductivity\\"
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


def determine_and_subtract_signal_mean(signal: np.ndarray) -> np.ndarray:
    mean = np.mean(signal)
    result = []
    for x in signal:
        result.append(x-mean)
    return np.array(result)


def calculate_conductance(frequency: int) -> float:
    # calculate output current at specific frequency/molarity combination
    #TODO: reset the molarity == 0.2 to 0.15?
    resistor_path = "C:\\Users\\Chris\\OneDrive\\Desktop\\sweep_record\\agar_"+MOLARITY+"\\crop_voltage_over_resistor" \
                    "\\voltage_over_resistor_agar_"+MOLARITY+str(frequency)+"Hz.npy"
    voltage_over_resistor = np.load(resistor_path)
    current = calculate_current(voltage_over_resistor=voltage_over_resistor, resistor=480)
    # calculate conductance of specific frequency/molarity combination
    inner_pair_path = "C:\\Users\\Chris\\OneDrive\\Desktop\\sweep_record\\agar_"+MOLARITY+"\\after_crop" \
                      "\\voltage_over_inner_pair_"+str(frequency)+"_Hz_decomposed_.npy"

    voltage_over_inner_pair_signal = np.load(inner_pair_path)

    voltage_over_inner_pair = rms(determine_and_subtract_signal_mean(voltage_over_inner_pair_signal)) / 1000
    return current / voltage_over_inner_pair


if __name__ == '__main__':
    conductances = []
    for f in FREQUENCIES:
        conductances.append(calculate_conductance(f))

    conductance = statistics.mean(conductances)
    with open(DESTINATION + "conductance_agar_"+MOLARITY+".txt", 'w') as file:
        file.write("Conductance of agar with "+MOLARITY+" NaCl: \n")
        file.write(str(conductance))
        file.write("\n\n")
        file.write("Conductivity of agar with "+MOLARITY+" Nacl and K = " + str(CELL_CONSTANT) + "\n")
        file.write(str(conductance/CELL_CONSTANT))


