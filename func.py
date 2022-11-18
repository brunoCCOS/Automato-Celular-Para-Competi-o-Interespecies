from click import option
import numpy as np

def arrival(pixel:int ,especies: list,lamb:int):
    '''
    Arrival func to randomize the arrival of a species
    args:  
        - pixel(required): int of the square to be applied the func
        - especies(required): list of all species avaible
        - lamb(required): int, hostility of the enviroment, higher lamb implies in less chance to species appear in pixel
    output:
        - result: the number of the especies ocupying the pixel
    '''
    #If with no especies
    if int:
        calc_proba = lambda lst,i: i/(sum(lst)+lamb) 
        prob = [calc_proba([esp.I for esp in especies],i.I) for i in especies] #Calculate individual probabilities taking hostility into account
        prob.append(1-sum(prob)) #Add the complement
        options = [*[sp.id for sp in especies],0] #List of especies ID
        result = np.random.choice(options,p = prob)#Randomize a especies
        return result
    else:
        return 0

def b(grid:np.array ,pos: list):
    '''
    Calculate and generate a sample for a born in a square in grid
    args:
        grid(required): Grid containing the information
        pos(required): Position of the square to be randomized
    outputs:
        sample: the class that proliferates in that direction
    '''
    if pos[0] == 0:
        neighbors = [] 
def c():