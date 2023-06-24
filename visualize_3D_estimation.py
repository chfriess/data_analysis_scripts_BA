import json
import random
from mpl_toolkits import mplot3d

import numpy as np
from matplotlib import pyplot as plt



"""

ax.plot3D(x_aorta, y_aorta, z_aorta, 'gray')
ax.plot3D(x_iliaca_left, y_iliaca_left, z_iliaca_left, 'gray')
ax.plot3D(x_iliaca_right, y_iliaca_right, z_iliaca_right, 'gray')
ax.plot3D(x_renal_left, y_renal_left, z_renal_left, 'gray')
ax.plot3D(x_renal_right, y_renal_right, z_renal_right, 'gray')

"""


def project_displacement_on_line(displacement: float, line_start: np.ndarray, line_end: np.ndarray):
    return line_start + displacement * line_end


start_aorta = np.array([0, 0, 0])
direction_aorta = np.array([1, 1, 1])
end_aorta = project_displacement_on_line(200, start_aorta, direction_aorta)
start_aorta2 = np.array([70, 70, 70])
direction_aorta2 = np.array([1, 1, 1])


start_left_renal = project_displacement_on_line(70, start_aorta, direction_aorta)
direction_left_renal = np.array([1, 0, 0])
end_left_renal = project_displacement_on_line(100, start_left_renal, direction_left_renal)

start_right_renal = project_displacement_on_line(70, start_aorta, direction_aorta)
direction_right_renal = np.array([-1, 0, 0])
end_right_renal = project_displacement_on_line(100, start_right_renal, direction_right_renal)

start_left_iliaca = project_displacement_on_line(200, start_aorta, direction_aorta)
direction_left_iliaca = np.array([1, 1, 0])
end_left_iliaca = project_displacement_on_line(100, start_left_iliaca, direction_left_iliaca)

start_right_iliaca = project_displacement_on_line(200, start_aorta, direction_aorta)
direction_right_iliaca = np.array([-1, 1, 0])
end_right_iliaca = project_displacement_on_line(100, start_right_iliaca, direction_right_iliaca)

vessels = [[start_aorta, direction_aorta],
            [start_aorta2, direction_aorta2],
           [start_left_renal, direction_left_renal],
           [start_right_renal, direction_right_renal],
           [start_left_iliaca, direction_left_iliaca],
           [start_right_iliaca, direction_right_iliaca]]


def plot_particle(position, branch, ax):
    point = project_displacement_on_line(displacement=position,
                                         line_start=vessels[branch][0],
                                         line_end=vessels[branch][1])
    ax.scatter3D(point[0], point[1], point[2], color="blue", s=2)




with open("C:\\Users\\Chris\\OneDrive\\Desktop\\particles_per_step.json", "r") as infile:
    particles_per_step = json.load(infile)
    start = particles_per_step["0"]
    diverging = particles_per_step["38"]
    end = particles_per_step["90"]



    for i in range(0, 147):
        fig = plt.figure(i)

        ax = plt.axes(projection='3d')

        ax.plot3D([start_aorta[0], end_aorta[0]],
                  [start_aorta[1], end_aorta[1]],
                  [start_aorta[2], end_aorta[2]],
                  color='black',
                  alpha=0.5)

        ax.plot3D([start_left_renal[0], end_left_renal[0]],
                  [start_left_renal[1], end_left_renal[1]],
                  [start_left_renal[2], end_left_renal[2]],
                  color='black',
                  alpha=0.5)

        ax.plot3D([start_right_renal[0], end_right_renal[0]],
                  [start_right_renal[1], end_right_renal[1]],
                  [start_right_renal[2], end_right_renal[2]],
                  color='black',
                  alpha=0.5)

        ax.plot3D([start_left_iliaca[0], end_left_iliaca[0]],
                  [start_left_iliaca[1], end_left_iliaca[1]],
                  [start_left_iliaca[2], end_left_iliaca[2]],
                  color='black',
                  alpha=0.5)

        ax.plot3D([start_right_iliaca[0], end_right_iliaca[0]],
                  [start_right_iliaca[1], end_right_iliaca[1]],
                  [start_right_iliaca[2], end_right_iliaca[2]],
                  color='black',
                  alpha=0.5)

        count = 0
        for p in particles_per_step[str(i)]:
            if p[0] == 2:
                count += 1
            #plot_particle(position=p[1], branch=p[0], ax=ax)

            plt.title("update step " + str(i))
        print(count)

        #plt.show()
        #plt.savefig("C:\\Users\\Chris\\OneDrive\\Desktop\\film\\frame"+str(i)+".png")



