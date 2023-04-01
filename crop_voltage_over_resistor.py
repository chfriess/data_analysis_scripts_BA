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

filepath = ""
destination = "C:\\Users\\Chris\\OneDrive\\Desktop\\sweep_record\\015M\\cropped_voltage_over_resistor\\"
voltage_over_resistor = np.load(filepath)


begin_of_measurement = (int)((5+9.7)*SAMPLING_FREQUENCY)
end_of_measurement = begin_of_measurement + 3*7*SAMPLING_FREQUENCY


voltage_over_resistor = voltage_over_resistor[begin_of_measurement:end_of_measurement]

np.save(destination+"", np.array(voltage_over_resistor))
plt.plot(np.array(voltage_over_resistor))
plt.savefig(destination+"" + ".svg")
