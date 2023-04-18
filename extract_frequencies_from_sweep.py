import numpy as np
import matplotlib.pyplot as plt
import pickle

synch_frequencies = [800, 1000]
sweep_frequencies = [500, 1000, 2000, 5000, 10000, 20000, 50000]
sweep_times = [3]*7
synch_begin_low_freq_duration = 3
synch_begin_high_freq_duration = 10
synch_end_high_freq_duration = 10
synch_end_low_freq_duration = 3

SAMPLING_FREQUENCY = 500_000

filepath = "C:\\Users\\Chris\\OneDrive\\Desktop\\sweep_record\\015M\\after_sync\\conductivity_measurements__voltage_over_inner_pair.npy"
destination = "C:\\Users\\Chris\\OneDrive\\Desktop\\sweep_record\\015M\\after_crop\\"

connected_frequencies = np.load(filepath)
decomposed_frequencies = []
begin_of_measurement = int((5 + 9.7) * SAMPLING_FREQUENCY)
current_offset = begin_of_measurement
epsilon = 500_000

for i in range (len(sweep_frequencies)):
    decomposed_frequencies.append(connected_frequencies[(current_offset+epsilon):((current_offset+3*SAMPLING_FREQUENCY)-epsilon)])
    current_offset += 3*SAMPLING_FREQUENCY

for i in range(len(decomposed_frequencies)):
    filename = "voltage_over_inner_pair_" + str(sweep_frequencies[i])+"_Hz_decomposed_"
    np.save(destination+filename, np.array(decomposed_frequencies[i]))
    fig, axes = plt.subplots(1, sharex='all')
    axes.plot(np.array(decomposed_frequencies[i]))
    plt.plot(np.array(decomposed_frequencies[i]))
    plt.savefig(destination+filename + ".svg")
    pickle.dump(fig, open(destination+filename+".pkl", 'wb'))
