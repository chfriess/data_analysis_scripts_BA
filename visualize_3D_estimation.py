import random
from mpl_toolkits import mplot3d

import numpy as np
from matplotlib import pyplot as plt

fig = plt.figure()

ax = plt.axes(projection='3d')

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

start_left_renal = project_displacement_on_line(90, start_aorta, direction_aorta)
direction_left_renal = np.array([1, 0, 0])
end_left_renal = project_displacement_on_line(100, start_left_renal, direction_left_renal)

start_right_renal = project_displacement_on_line(90, start_aorta, direction_aorta)
direction_right_renal = np.array([-1, 0, 0])
end_right_renal = project_displacement_on_line(100, start_right_renal, direction_right_renal)

start_left_iliaca = project_displacement_on_line(200, start_aorta, direction_aorta)
direction_left_iliaca = np.array([1, 1, 0])
end_left_iliaca = project_displacement_on_line(100, start_left_iliaca, direction_left_iliaca)

start_right_iliaca = project_displacement_on_line(200, start_aorta, direction_aorta)
direction_right_iliaca = np.array([-1, 1, 0])
end_right_iliaca = project_displacement_on_line(100, start_right_iliaca, direction_right_iliaca)

vessels = [[start_aorta, direction_aorta],
           [start_left_renal, direction_left_renal],
           [start_right_renal, direction_right_renal],
           [start_left_iliaca, direction_left_iliaca],
           [start_right_iliaca, direction_right_iliaca]]


def plot_particle(position, branch):
    point = project_displacement_on_line(displacement=position,
                                         line_start=vessels[branch][0],
                                         line_end=vessels[branch][1])
    ax.scatter3D(point[0], point[1], point[2], color="blue", s=2)


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



particles = []
for i in range(5):
    for j in range(20):
        particles.append([random.uniform(0, 50), i])

for particle in particles:
    plot_particle(position=particle[0], branch=particle[1])
