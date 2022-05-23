import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from helpers import read_echogram

class EchoGram:
    """ Class to manipulate sonar data. 
        echo - (usually) side scan sonar image with datatype ndarray
        df - pandas dataframe (table) with columns of useful measurements such as depth
        data - raw table used to create self.df
    """
    def __init__(self, filename, channels=None):
        self.filename = filename
        self.data, self.echo = self.test_overlay_wb_echo(filename, channels)
        self.df = pd.DataFrame(self.data)
        self.lat_lon_to_meters(self.df["longitude"].to_numpy(), self.df["latitude"].to_numpy())
        self.initialize_point_cloud()
        
        del self.data
        
    def test_overlay_wb_echo(self, filename, channels=None):
        """ Load sounding data and echogram and plot the entire sonar image. 
            The library, Python SLLIB, used in the helpers.py file, decodes the SL2 file format from Lowrance sonar sounder and
            converts it to two simple data types, one is data, a list of dictionaries, which is later converted to a pandas dataframe,
            a table with the values of the different variables that the sonar outputs, and the second data type is a ndarray that
            represents the image that the sonar outputs. 
            
            Input: 
            Filename: string containing the sl2 file location
            Channel: sonar sensor type
                - 0 = Primary (Traditional Sonar)
                - 1 = Secondary (Traditional Sonar)
                - 2 = DSI (Downscan Imaging)
                - 3 = Sidescan Left
                - 4 = Sidescan Right
                - 5 = Sidescan (Composite)
                Another other value is treated as Invalid.
        """
        data, echo = read_echogram(filename, channels)

        fig, axes = plt.subplots()
        axes.imshow(echo, aspect='auto')
        fig.show()
        #fig.savefig('sss.png', dpi=fig.dpi)
        return data, echo
    
    def lat_lon_to_meters(self, lon, lat, x0=-9147145.64754388, y0=3427601.097538607):
        """ Convert longitude and latitude to global X and Y coordinates in meters
            Inputs:
                lon: longitude 
                lat: latitude
                x0: X position of the origin in the new map
                y0: Y position of the origin in the new map
            NOTE: default of x0 and y0 is (an eyeballed) bottom left point in CITRA pond, Florida
        """
        # Using Spherical Pseudo-Mercator projection
        # https://wiki.openstreetmap.org/wiki/Mercator
        R =  6378137.0
        Y = np.log(np.tan(np.pi / 4 + np.radians(lat) / 2)) * R
        X = np.radians(lon) * R
        
        self.X = X - x0
        self.Y = Y - y0
        self.df["X_m"] = np.copy(self.X)
        self.df["Y_m"] = np.copy(self.Y)
        
    def see_range(self, range):
        """ Plots the whole trajecory in black and the range in the input in red
            inputs: range - vector of start and stop (ex: [10, 200])
        """
        fig, ax = plt.subplots()
        ax.plot(self.X, self.Y, 'ko', ms=0.5)
        ax.plot(self.X[range[0]:range[1]], self.Y[range[0]:range[1]], 'ro', ms=0.5)
        ax.set_aspect('equal')

    def crop_data(self, start, end, step=1, use_conditional=False, condition=None):
        """ crops all the dataypes in the echogram class based on start stop index or conditional
        """
        if use_conditional:
            self.echo = np.delete(self.echo, condition, 1)
            self.X = np.delete(self.X, condition, 0)
            self.Y = np.delete(self.Y, condition, 0)
            self.df = self.df.drop(self.df.index[condition])
        else:
            # to delete the end, start from -1, end in a negative and step -1
            self.echo = np.delete(self.echo, slice(start,end, step), 1)
            self.df = self.df.drop(self.df.index[range(start,end, step)])
            self.X = np.delete(self.X, slice(start,end, step))
            self.Y = np.delete(self.Y, slice(start,end, step))
        
    def initialize_point_cloud(self):
        self.point_cloud = {}
        self.point_cloud["X"] = self.df["X_m"] 
        self.point_cloud["Y"] = self.df["Y_m"]
        self.point_cloud["Z"] = self.df['water_depth_m']
        
        