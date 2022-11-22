import numpy as np
from scipy.stats import truncnorm

def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)


class Species:

    
    count = 1
    conflict_matrix = None
    
    def __init__(self,sigma):
        self.E = np.random.normal(loc=0.25,scale=sigma)
        self.D = np.random.normal(loc=0.1,scale=sigma)
        self.id = Species.count
        self.historical_individual = list()
        self.individuals = 0
        Species.count+=1

    def grow_individual(self):
        self.individuals += 1

    def death_individual(self):
        self.individuals -= 1

    def add_timestamp(self):
        self.historical_individual.append(self.individuals)
        
    def initialize_matrix(M):
        '''
        Initialize static matrix conflict_matrix with MxM entries from random samples betwen (0,1)
        args:
            - M(required) : Number of species to be accounted in conflict matrix
        '''
        #Random sample probabilities
        samples = np.random.uniform(low = 0., high = 1., size = (M,M))
        #Generate random matrix MxM with numbers betwen (0,1)
        Species.conflict_matrix =  np.full((M,M),samples)
        #Iterate matrix and compensate to make opposite sides sums 1 and diagonals entries to be 1 either
        for row in range(M):
            for i in range(M):
                if row == i:
                    Species.conflict_matrix[i][i] = 0.5 # Initialize diagonals with 1
                    break #Exit of that line
                else: 
                    Species.conflict_matrix[row][i] = 1 - Species.conflict_matrix[i][row] # Calculates the complement of the probability in the upper part