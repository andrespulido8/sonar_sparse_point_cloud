import os
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import open3d as o3d

## Load Point Cloud dataframes from jupyter notebooks using pickle
# October21 data
with open('processed_data/PC.txt', 'rb') as fl:
    oct = pickle.load(fl)
oct = oct.dropna()
with open('processed_data/PC_r.txt', 'rb') as file:
    oct_r = pickle.load(file)
oct_r = oct_r.dropna(axis=0)
with open('processed_data/PC_l.txt', 'rb') as file:
    oct_l = pickle.load(file)
oct_l = oct_l.dropna()
# February22 data
with open('processed_data/PC_dataset.txt', 'rb') as file:
    feb_r = pickle.load(file)
with open('processed_data/PC_dataset2.txt', 'rb') as file:
    feb_l = pickle.load(file)
with open('processed_data/PC_depth.txt', 'rb') as file:
    feb= pickle.load(file)

def plot_pc(pc_dataframe_list, color=['k'], legend=['Original'], size=[0.5]):
    """ Plot point cloud dataframe 
    Input:
        pc_dataframe_list: list of dataframes
        color: list of colors
        legend: list of legends
        size: list of sizes
        Output:
            Plot
    """
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    for ii, df in enumerate(pc_dataframe_list):
        ax.scatter(df["x"], df["y"], df['z'], s=size[ii],
                   c=color[ii], label=legend[ii])
    ax.set_xlabel('X [m]')
    ax.set_ylabel('Y [m]')
    ax.set_zlabel('Z [m]')
    plt.legend()
    plt.show()

## Call functions to plot point clouds

# October 21 plot
oct_pc = pd.concat([oct_r, oct_l])
#plot_pc([pc])
plot_pc([oct, oct_r, oct_l], color=['k', 'r', 'b'],
        legend=['Original', 'Right', 'Left'], size=[0.5, 0.5, 0.5])

# February21 plot
#feb_list = [feb_r, feb_l]
#plot_pc(pc_list, color=['r', 'b'],
#        legend=['Right', 'Left'], size=[0.5, 0.5])
#feb_list.append(feb_pc)
#plot_pc(pc_list, color=['r', 'b', 'k'],
#        legend=['Right', 'Left', 'Original'], size=[0.5, 0.5, 0.2])

# Full point cloud
#pc_r = pd.concat([feb_r, oct_r])
#pc_l = pd.concat([feb_l, oct_l])
#pc = pd.concat([oct, feb_pc])

# Outlier Removal
def display_inlier_outlier(cloud, ind):
    inlier_cloud = cloud.select_by_index(ind)
    outlier_cloud = cloud.select_by_index(ind, invert=True)

    print("Showing outliers (red) and inliers (gray): ")
    outlier_cloud.paint_uniform_color([1, 0, 0])
    inlier_cloud.paint_uniform_color([0.8, 0.8, 0.8])
    o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])

print("Statistical oulier removal")
pcd = o3d.geometry.PointCloud()
oct_arr = oct_pc[['x', 'y', 'z']].values
pcd.points = o3d.utility.Vector3dVector(oct_arr)
#cl, ind = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=1)
# remove_radius_outlier is super sensitive to parameters. It'd be fun to try an
#  optimization to get specific # of outliers removed
cl, ind = pcd.remove_radius_outlier(nb_points=10, radius=3.011) # nb_points = 10, radius = 3.010

#display_inlier_outlier(cl, ind)

oct_out_arr = np.asarray(cl.points)
for ii, index in enumerate(ind):
    if index >= len(oct_r):
        x = ii
        print('len(oct_r): ', len(oct_r))
        print('index: ', index)
        break

## create list from 0 to len(oct_r) of numbers that are not in ind
reverse = [i for i in range(len(oct_pc)) if i not in ind]

ind1 = ind[:x]; ind2 = ind[x:]

oct_out_r = pd.DataFrame(oct_arr[:len(oct_r)][ind1], columns=['x', 'y', 'z'])
oct_out_l = pd.DataFrame(oct_arr[range(-1,-len(oct_l)-1,-1)][np.array(ind2)-len(oct_r)], columns=['x', 'y', 'z'])

plot_pc([oct, oct_out_r, oct_out_l], color=['k', 'r', 'b'],
        legend=['Down-scan sonar depth', 'Side-scan starboard', 'Side-scan port'], size=[0.5, 1, 1])

oct_out = pd.DataFrame(oct_out_arr, columns=['x', 'y', 'z'])
print('original length: ', len(oct_pc))
print('no outlier length: ', len(oct_out))
print('outliers removed: ', len(oct_pc) - len(oct_out), len(reverse))
plot_pc([oct_out, oct_pc.iloc[reverse]], color=['cyan', 'r'], legend=['Stayed', 'Outliers'], size=[0.5, 1])
print('done')

