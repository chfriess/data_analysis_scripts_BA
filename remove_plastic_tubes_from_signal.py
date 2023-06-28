import numpy as np
from matplotlib import pyplot as plt



SAMPLES = ["39", "41", "42", "44", "45"]
#SAMPLES = ["45"]





"""

PLASTIC_POSITION_START = 75


PLASTIC_POSITION_END = 305

for sample_nr in SAMPLES:
    impedance_path = "C:\\Users\\Chris\\OneDrive\\Desktop\\plastic coregistration data\\04_06_2023_BS\\coregistration_" + sample_nr \
                             + "\\data_bioelectric_sensors" "\\impedance_from_iliaca.npy"
    groundtruth_path = "C:\\Users\\Chris\\OneDrive\\Desktop\\plastic coregistration data\\04_06_2023_BS\\coregistration_" + sample_nr \
                             + "\\data_bioelectric_sensors" "\\groundtruth_shifted_from_iliaca.npy"
    displacement_path = "C:\\Users\\Chris\\OneDrive\\Desktop\\plastic coregistration data\\04_06_2023_BS\\coregistration_" + sample_nr \
                             + "\\data_bioelectric_sensors" "\\displacements_from_iliaca.npy"


    imp = np.load(impedance_path) /100
    gt = np.load(groundtruth_path)
    disp = np.load(displacement_path)

    n = 0
    for i, el in enumerate(gt):
        n = i
        if el > PLASTIC_POSITION_END:
            break

    start = 0
    for i, el in enumerate(gt):
        start = i
        if el > PLASTIC_POSITION_START:
            break

    gt_crop_plastic = gt[start:n]
    print(start)
    print(n)

    imp_crop_plastic = imp[start:(n-1)]
    disp_crop_plastic = disp[start:(n-1)]

    acc = [0]
    for i, el in enumerate(disp_crop_plastic):
        acc.append(acc[i] + el)

    x_gt = np.linspace(0, len(gt_crop_plastic), 150)
    x_bio = np.linspace(0, len(imp_crop_plastic), 149)
    x_acc = np.linspace(0, len(acc), 150)

    gt_interp = np.interp(x_gt, [x for x in range(len(gt_crop_plastic))], gt_crop_plastic)
    imp_interp = np.interp(x_bio,  [x for x in range(len(imp_crop_plastic))], imp_crop_plastic)
    acc_disp_interp = np.interp(x_acc,  [x for x in range(len(acc))], acc)

    disp_interp = []
    for i in range(1, len(acc_disp_interp)):
        disp_interp.append(acc_disp_interp[i] - acc_disp_interp[i-1])


    re_acc = [0]
    for i, el in enumerate(disp_interp):
        re_acc.append(re_acc[i] + el)
    plt.plot(gt_interp, label="gt_interp")
    plt.plot(imp_interp, label="imp_interp")
    plt.plot(re_acc, label="disp_interp")
    plt.legend()


  
    plt.savefig("C:\\Users\\Chris\\OneDrive\\Desktop\\plastic coregistration data\\04_06_2023_BS\\coregistration_" + sample_nr \
                             + "\\data_bioelectric_sensors" + "\\validation_of_plastic_cropping.svg")

    plt.clf()

    np.save("C:\\Users\\Chris\\OneDrive\\Desktop\\plastic coregistration data\\04_06_2023_BS\\coregistration_" + sample_nr \
                             + "\\data_bioelectric_sensors" + "\\impedance_from_iliaca_without_plastic.npy", imp_interp)

    np.save("C:\\Users\\Chris\\OneDrive\\Desktop\\plastic coregistration data\\04_06_2023_BS\\coregistration_" + sample_nr \
                             + "\\data_bioelectric_sensors" + "\\groundtruth_from_iliaca_without_plastic.npy", gt_interp)

    np.save("C:\\Users\\Chris\\OneDrive\\Desktop\\plastic coregistration data\\04_06_2023_BS\\coregistration_" + sample_nr \
                             + "\\data_bioelectric_sensors" + "\\displacements_from_iliaca_without_plastic.npy", disp_interp)

    print(len(imp_interp))
    print(len(disp_interp))
    print(len(gt_interp))
    print("\n\n")



"""

# AGAR PHANTOM

SAMPLES = ["20", "25", "30", "31", "34"]
#SAMPLES = ["20"]




PLASTIC_POSITION_END = 190

for sample_nr in SAMPLES:
    impedance_path = "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom_data_testing\\sample_" + sample_nr \
                             + "\\data_sample_" + sample_nr + "\\impedance_from_iliaca.npy"
    groundtruth_path = "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom_data_testing\\sample_" + sample_nr + \
                               "\\data_sample_" + sample_nr + "\\groundtruth_from_iliaca.npy"
    displacement_path = "C:\\Users\\Chris\\OneDrive\\Desktop\\phantom_data_testing\\sample_" + sample_nr + "\\data_sample_" + sample_nr + "\\displacements_from_iliaca.npy"


    imp = np.load(impedance_path) /1000
    gt = np.load(groundtruth_path)
    disp = np.load(displacement_path)



    n = 0
    for i, el in enumerate(gt):
        if el > 190:
            n = i
            break

    gt_crop_plastic = gt[:n]


    imp_crop_plastic = imp[:(n-1)]
    disp_crop_plastic = disp[:(n-1)]

    acc = [0]
    for i, el in enumerate(disp_crop_plastic):
        acc.append(acc[i] + el)

    x_gt = np.linspace(0, len(gt_crop_plastic), 150)
    x_bio = np.linspace(0, len(imp_crop_plastic), 149)
    x_acc = np.linspace(0, len(acc), 150)



    gt_interp = np.interp(x_gt, [x for x in range(len(gt_crop_plastic))], gt_crop_plastic)
    imp_interp = np.interp(x_bio,  [x for x in range(len(imp_crop_plastic))], imp_crop_plastic)
    acc_disp_interp = np.interp(x_acc,  [x for x in range(len(acc))], acc)


    disp_interp = []
    for i in range(1, len(acc_disp_interp)):
        disp_interp.append(acc_disp_interp[i] - acc_disp_interp[i - 1])

    re_acc = [0]
    for i, el in enumerate(disp_interp):
        re_acc.append(re_acc[i] + el)
    plt.plot(gt_interp, label="gt_interp")
    plt.plot(imp_interp, label="imp_interp")
    plt.plot(re_acc, label="disp_interp")
    plt.legend()


    
    plt.savefig("C:\\Users\\Chris\\OneDrive\\Desktop\\phantom_data_testing\\sample_" + sample_nr \
                + "\\data_sample_" + sample_nr + "\\validation_of_plastic_cropping.svg")

    plt.clf()

    np.save("C:\\Users\\Chris\\OneDrive\\Desktop\\phantom_data_testing\\sample_" + sample_nr \
                             + "\\data_sample_" + sample_nr
            + "\\impedance_from_iliaca_without_plastic.npy", imp_interp)

    np.save("C:\\Users\\Chris\\OneDrive\\Desktop\\phantom_data_testing\\sample_" + sample_nr + \
                               "\\data_sample_" + sample_nr + "\\groundtruth_from_iliaca_without_plastic.npy", gt_interp)

    np.save("C:\\Users\\Chris\\OneDrive\\Desktop\\phantom_data_testing\\sample_" + sample_nr
            + "\\data_sample_" + sample_nr + "\\displacements_from_iliaca_without_plastic.npy", disp_interp)

