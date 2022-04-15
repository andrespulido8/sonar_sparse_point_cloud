import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt

with open('processed_data/PC.txt', 'rb') as fl:
    # Call load method to deserialze
    pc = pickle.load(fl)


def plot_pc(pc_dataframe_list, color=['b']):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    for ii, df in enumerate(pc_dataframe_list):
        ax.scatter(df["x"], df["y"], df['z'], s=0.5, c=color[ii])
    ax.set_xlabel('X [m]')
    ax.set_ylabel('Y [m]')
    ax.set_zlabel('Z [m]')
    plt.show()


plot_pc([pc])

with open('processed_data/PC_r.txt', 'rb') as file:
    # A new file will be created
    pc_r = pickle.load(file)

with open('processed_data/PC_l.txt', 'rb') as file:
    # A new file will be created
    pc_l = pickle.load(file)
plot_pc([pc, pc_r, pc_l], color=['k', 'r', 'b'])
