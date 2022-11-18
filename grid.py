
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

class Grid:   
    def __init__(self,M:int = 140):
        self.M = M
        self.grid = self.generate_grid(self.M)
    
    def generate_grid(self,M: int):
        '''
        Generate grid MxM
        args:
            M (required) : Number of elements in square matrix MxM
        '''
        self.grid = np.full(M*M,tuple())
        return  self.grid.reshape(M,M)

    def update_grid(self,arrival_func,competing_func):
        '''
        Updates grid's pixels values by computing competing and arrival functions
        '''
        novo = self.grid.copy()#Copy original grid
        
        #Aplies arrival_func
        for pixel in range(self.M):
            #Checks if pixel is not already populated since arrival func is only applied in empty squares
            if novo[0][pixel]:
                novo[0][pixel] = arrival_func(novo[0][pixel])#Applies arrival func in the top of the grid
            if novo[pixel][0]:
                novo[pixel][0] = arrival_func(novo[0][pixel])#Applies arrival func in left part of the grid
            if novo[self.M][pixel]:
                novo[self.M][pixel] = arrival_func(novo[0][pixel])#Applies arrival func in right part of the grid
            if novo[pixel][self.M]:
                novo[pixel][self.M] = arrival_func(novo[0][pixel])#Applies arrival func in bottom part of the grid

        #Applies competing func to every square
        for i in range(self.M):
            for j in range(self.M):
                novo[i, j] = competing_func(self.grid,(i,j))
        
        self.grid[:][:] = novo[:][:] #Updates original grid to point to the new one
        return self.grid