import numpy as np
import matplotlib.pyplot as plt

synch_frequencies = [800, 1000]
sweep_frequencies = [500, 1000, 2000, 5000, 10000, 20000, 50000]
sweep_times = [3]*7
synch_begin_low_freq_duration = 3
synch_begin_high_freq_duration = 10
synch_end_high_freq_duration = 10
synch_end_low_freq_duration = 3

SAMPLING_FREQUENCY = 500_000

filepath = "" + "conductivity_measurements__voltage_over_inner_pair.npy"  # ENTER FILTEPATH
destination = ""  # ENTER DESTINATION

connected_frequencies = np.load(filepath)
decomposed_frequencies = []
begin_of_measurement = int(15 * SAMPLING_FREQUENCY)
current_offset = begin_of_measurement
epsilon = 500_000

signal = []
for i in range(0, len(connected_frequencies), 10):
    signal.append(connected_frequencies[i])

plt.plot(signal)
plt.show()
