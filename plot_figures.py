import os
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import pickle
from echogram import EchoGram


with open('processed_data/dataset_012022.txt', 'rb') as fl:
    dataset_012022 = pickle.load(fl)
with open('processed_data/cropped_dataset.txt', 'rb') as fl:
    cropped_dataset = pickle.load(fl)

files = os.listdir('log-data-lowrance/02_20_22')
print(files)


xmin = 1.0033640917390585
xmax = 140.47097257710993
ymin = -2.006728178821504
ymax = 114.38350624218583
no_so1 = [10401, 11400,     0]
ea_we1 = [12401, 13700,    3]
no_so_range1 = range(no_so1[0], no_so1[1])
ea_we_range1 = range(ea_we1[0], ea_we1[1])

plt.style.use("fast")

plt.rcParams.update({
    "text.usetex": False,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica"]})


fig, ax = plt.subplots()
ax.plot(dataset_012022[files[no_so1[2]]].X,
        dataset_012022[files[no_so1[2]]].Y, '-ok', ms=1, alpha=0.7)
ax.plot(dataset_012022[files[ea_we1[2]]].X,
        dataset_012022[files[ea_we1[2]]].Y, '-ok', ms=1, alpha=0.7)
ax.plot(dataset_012022[files[no_so1[2]]].X[no_so_range1],
        dataset_012022[files[no_so1[2]]].Y[no_so_range1], '-or', ms=0.05)
ax.plot(dataset_012022[files[ea_we1[2]]].X[ea_we_range1],
        dataset_012022[files[ea_we1[2]]].Y[ea_we_range1], '-or', ms=0.05)
# ax.set_aspect('equal')
ax.set_xlabel('$x$ [m]')
ax.set_ylabel('$y$ [m]')
plt.xlim(xmin-10, xmax+10)
plt.ylim(ymin-10, ymax+10)
plt.grid()
plt.show()
fig.savefig('paper_figures/pattern1.jpg', dpi=fig.dpi)
