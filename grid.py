
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

class Grid:
    def __init__(self,M:int = 140):
        self.M = M
        self.grid = Grid.generate_grid(self.M)

    def generate_grid(M: int):
        '''
        Generate grid MxM
        args:
            M (required) : Number of elements in square matrix MxM
        '''
        grid = np.full((M,M),0)
        # print(self.grid)
        return  grid

    def update_grid(self,arrival_func,competing_func):
        '''
        Updates grid's pixels values by computing competing and arrival functions
        '''
        novo = self.grid.copy()#Copy original grid
        
        #Aplies arrival_func
        for pixel in range(self.M):
            #Checks if pixel is not already populated since arrival func is only applied in empty squares
            novo[0][pixel] = arrival_func(novo[0][pixel])#Applies arrival func in the top of the grid
            novo[pixel][0] = arrival_func(novo[0][pixel])#Applies arrival func in left part of the grid
            novo[self.M][pixel] = arrival_func(novo[0][pixel])#Applies arrival func in right part of the grid
            novo[pixel][self.M] = arrival_func(novo[0][pixel])#Applies arrival func in bottom part of the grid

        #Applies competing func to every square
        for i in range(self.M):
            for j in range(self.M):
                novo[i, j] = competing_func(self.grid,(i,j))
        
        self.grid[:][:] = novo[:][:] #Updates original grid to point to the new one
        return self.grid