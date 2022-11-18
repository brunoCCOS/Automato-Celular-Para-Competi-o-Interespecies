import numpy as np

class Especies:
    
    conflict_matrix = None
    
    def __init__(self,sigma):
        self.B = np.random.normal(loc=0.1,scale=sigma)
        self.D = np.random.normal(loc=0.05,scale=sigma)
        self.I = np.random.normal(loc=0.25,scale=sigma)
    
    def initialize_matrix(M):
        '''
        Initialize static matrix conflict_matrix with MxM entries from random samples betwen (0,1)
        args:
            - M(required) : Number of especies to be accounted in conflict matrix
        '''
        #Random sample probabilities
        samples = np.uniform(low = 0., high = 1., size = (M,M))
        #Generate random matrix MxM with numbers betwen (0,1)
        Especies.conflict_matrix =  np.full((M,M),samples)
        #Iterate matrix and compensate to make opposite sides sums 1 and diagonals entries to be 1 either
        for row in range(M):
            for i in range(M):
                if row == i:
                    Especies.conflict_matrix[i][i] = 1 # Initialize diagonals with 1
                    break #Exit of that line
                else: 
                    Especies.conflict_matrix[row][i]=1 - Especies.conflict_matrix[i][row] # Calculates the complement of the probability in the upper part