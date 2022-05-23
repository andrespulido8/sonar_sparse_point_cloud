from cProfile import label
import os
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt

with open('processed_data/PC.txt', 'rb') as fl:
    # Call load method to deserialze
    pc = pickle.load(fl)


def plot_pc(pc_dataframe_list, color=['k'], legend=[None]):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    for ii, df in enumerate(pc_dataframe_list):
        ax.scatter(df["x"], df["y"], df['z'], s=0.5,
                   c=color[ii], label=legend[ii])
    ax.set_xlabel('X [m]')
    ax.set_ylabel('Y [m]')
    ax.set_zlabel('Z [m]')
    plt.legend()
    plt.show()


plot_pc([pc])

with open('processed_data/PC_r.txt', 'rb') as file:
    # A new file will be created
    pc_r = pickle.load(file)

with open('processed_data/PC_l.txt', 'rb') as file:
    # A new file will be created
    pc_l = pickle.load(file)
plot_pc([pc, pc_r, pc_l], color=['k', 'r', 'b'],
        legend=['Original', 'Right', 'Left'])


with open('processed_data/PC_dataset.txt', 'rb') as file:
    # A new file will be created
    PC_dataset = pickle.load(file)

files = os.listdir('log-data-lowrance/02_20_22')
print(files)

pc_list = []
for ii in range(len(files)):
    pc_list.append(PC_dataset[files[ii]])

plot_pc(pc_list, color=['k', 'r', 'b', 'g', 'y'],
        legend=['Original', '1', '2', '3', '4'])
