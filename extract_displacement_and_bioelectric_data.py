import os

import numpy as np
from matplotlib import pyplot as plt

NO = "35"

if __name__ == "__main__":


    for COREGISTRATION_NR in [str(x) for x in range(25, 26)]:
        path = "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom coregistration data\\06_05_2023_BS\\coregistration_" + COREGISTRATION_NR + "\\data_bioelectric_sensors\\"
        DESTINATION = "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom coregistration data\\06_05_2023_BS\\coregistration_" + COREGISTRATION_NR + "\\em_groundtruth\\groundtruth_" + COREGISTRATION_NR + "_cropped.npy"

        displacements = np.load(path + "cumulative displacements sample" + COREGISTRATION_NR + ".npy")
        impedance = np.load(path + "impedance_sample" + COREGISTRATION_NR + ".npy")

        em_groundtruth = np.load(DESTINATION)

        plt.plot(displacements)
        #plt.plot(impedance)
        #plt.plot(em_groundtruth)

        plt.show()



"""
    
    displacements = np.load(path+"displacements_sample"+COREGISTRATION_NR+".npy")
    impedance = np.load(path + "impedance_sample" + COREGISTRATION_NR + ".npy")

    if len(displacements) > len(impedance):
        displacements = displacements[1:]

    np.save(path+"displacements_sample"+COREGISTRATION_NR+".npy", displacements)

    displacements = np.load(path + "displacements_sample" + COREGISTRATION_NR + ".npy")
    impedance = np.load(path + "impedance_sample" + COREGISTRATION_NR + ".npy")

    em_groundtruth = np.load(DESTINATION)

    if len(displacements) != len(impedance):
        raise ValueError("Now impedance and displacements must share the same length")

    if len(displacements) != len(em_groundtruth):
        raise ValueError("Now displacements and groundtruth must share same length")



os.chdir("C:\\Users\\Chris\\OneDrive\\Desktop\\phantom coregistration data\\06_05_2023_BS\\")

aorta = [1/20 for x in range(200)]
iliaca = [1/13 for x in range(90)]

groundtruth = np.array(aorta + iliaca)

plt.plot(groundtruth)
plt.savefig("groundtruth.svg")
np.save("groundtruth.npy", groundtruth)





os.chdir("C:\\Users\\Chris\\OneDrive\\Desktop\\phantom coregistration data\\06_05_2023_BS\\coregistration_"+NO+"\\data_bioelectric_sensors\\")
FILE = "coregistration_"+NO+"_sampling_corrected.npz"



data = np.load(FILE)




# DISPLACEMENTS
cumulative_displacements = data["windows_x_translation"]
impedance = data["fft_magnitude_BminA"]
print(len(cumulative_displacements))
print(len(impedance))
print(cumulative_displacements[1])


displacements = []

for i in range(1, len(cumulative_displacements)):
    displacements.append(cumulative_displacements[i] - cumulative_displacements[i-1])


plt.plot(cumulative_displacements)
plt.title("cumulative displacement sample" + NO)
plt.savefig("cumulative_displacement_sample" + NO + ".svg")

plt.clf()
plt.plot(displacements)
plt.title("displacements sample" + NO)
plt.savefig("displacements_sample" + NO + ".svg")




np.save("cumulative displacements sample" + NO + ".npy", cumulative_displacements)
np.save("displacements_sample" + NO + ".npy", displacements)




#IMPEDANCE

impedance = data["fft_magnitude_BminA"]

plt.clf()
plt.plot(impedance)
plt.title("impedance sample" + NO)
plt.show()
plt.savefig("impedance_sample" + NO + ".svg")

np.save("impedance_sample" + NO + ".npy", impedance)

data.close()


"""


