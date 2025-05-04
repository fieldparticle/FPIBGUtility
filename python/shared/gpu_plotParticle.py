import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation  
import keyboard
class ParticlePlot3D:

    def __init__(self,particleList):
        self.particleList = particleList
        self.elev = 0.0
        self.azim = 0.0
        self.roll = 0.0
    #abscissa ≡ horizontal
    #ordinate ≡ verticle
    #right = ordinate on rifht
    #left = ordinate on left
    #T top =  abscissa on top
    #B bottom = abscissa on bottom
    def viewXY(self):
        self.elev= -86.0
        self.azim = 160.0
        self.roll = 112.0


    def plotParticle(self):
    
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_aspect('equal', adjustable='box')
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.view_init(elev=self.elev, azim=self.azim, roll=self.roll) 
        for ii in self.particleList:
            r = ii.PosLoc[3]
            phi, theta = np.mgrid[0:2*np.pi:100j, 0:np.pi:50j]
            # Convert to Cartesian coordinates
            x = ii.PosLoc[0] + r * np.sin(theta) * np.cos(phi)
            y = ii.PosLoc[1] + r * np.sin(theta) * np.sin(phi)
            z = ii.PosLoc[2] + r * np.cos(theta)
            ax.scatter(x, y, z)
            
        plt.show()
        
class ParticlePlot2D:

    partAry = []
    def __init__(self,particleList):
        self.pl = particleList
        self.elev = 0.0
        self.azim = 0.0
        self.roll = 0.0
        
        # initializing a figure in  
       

    def start(self):
        # which the graph will be plotted 
        self.fig, self.ax=plt.subplots()



    #abscissa ≡ horizontal
    #ordinate ≡ verticle
    #right = ordinate on rifht
    #left = ordinate on left
    #T top =  abscissa on top
    #B bottom = abscissa on bottom
    def viewXY(self):
        self.elev= -86.0
        self.azim = 160.0
        self.roll = 112.0

    


    def plotParticle(self):
        self.fig.clf()
        self.ax.set_aspect( 1 ) 
        plt.xlim( 0.0 , 3.5 ) 
        plt.ylim( 0.0 , 3.5 ) 
        self.ax.set_aspect('equal', adjustable='box')
        plt.xlabel("X")
        plt.ylabel("Y")
        for ii in self.pl:
            r = ii.PosLoc[3]
            angle = np.linspace( 0 , 2 * np.pi , 150 ) 
            x = ii.PosLoc[0] + r * np.cos( angle ) 
            y = ii.PosLoc[1] + r * np.sin( angle ) 
            plt.plot(ii.PosLoc[0], ii.PosLoc[1], 'go', label='marker only')  # use this to plot a single point
            plt.plot(x, y) 

        plt.pause(1)
        plt.show(block=False)
       
            
        
                
 
