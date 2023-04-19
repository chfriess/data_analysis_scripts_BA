import numpy as np
import matplotlib.pyplot as plt

synch_frequencies = [800, 1000]
sweep_frequencies = [500, 1000, 2000, 5000, 10000, 20000, 50000]
sweep_times = [3] * 7
synch_begin_low_freq_duration = 3
synch_begin_high_freq_duration = 10
synch_end_high_freq_duration = 10
synch_end_low_freq_duration = 3

SAMPLING_FREQUENCY = 500_000

MOLARITY = "002M"
filepath = "C:\\Users\\Chris\\OneDrive\\Desktop\\sweep_record\\agar_" + MOLARITY + "\\after_sync\\conductivity_measurements__voltage_over_resistor.npy"
destination = "C:\\Users\\Chris\\OneDrive\\Desktop\\sweep_record\\agar_" + MOLARITY + "\\crop_voltage_over_resistor\\"

voltage_over_resistor = np.load(filepath)

begin_of_measurement = int((5 + 9.7) * SAMPLING_FREQUENCY)
end_of_measurement = begin_of_measurement + 3 * 7 * SAMPLING_FREQUENCY
decomposed_frequencies = []

current_offset = begin_of_measurement
epsilon = 500_000

for i in range(len(sweep_frequencies)):
    decomposed_frequencies.append(
        voltage_over_resistor[(current_offset + epsilon):((current_offset + 3 * SAMPLING_FREQUENCY) - epsilon)])
    current_offset += 3 * SAMPLING_FREQUENCY

for i in range(len(decomposed_frequencies)):
    np.save(destination + "voltage_over_resistor_agar_" + MOLARITY + str(sweep_frequencies[i]) + "Hz",
            np.array(decomposed_frequencies[i]))
    plt.plot(np.array(decomposed_frequencies[i]))
    plt.savefig(destination + "voltage_over_resistor_agar_" + MOLARITY + str(sweep_frequencies[i]) + "Hz" + ".svg")
