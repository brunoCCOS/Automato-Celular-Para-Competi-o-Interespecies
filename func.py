import numpy as np
from especies import Species
from itertools import combinations

def a(pixel:int ,species: list,lamb:int):
    '''
    Arrival func to randomize the arrival of a species
    args:  
        - pixel(required): int of the square to be applied the func
        - species(required): list of all species avaible
        - lamb(required): int, hostility of the enviroment, higher lamb implies in less chance to species appear in pixel
    output:
        - result: the number of the species ocupying the pixel
    '''
    #If with no species
    if pixel == 0:
        calc_proba = lambda lst,i: i/(sum(lst)+lamb) 
        prob = [calc_proba([esp.E for esp in species],i.E) for i in species] #Calculate individual probabilities taking hostility into account
        prob.append(1-sum(prob)) #Add the complement
        options = [*[sp.id for sp in species],0] #List of species ID
        result = np.random.choice(options,p = prob)#Randomize a species
        return result
    else:
        return pixel

def c(conflict_arr: list):
    '''
    Solve dispute for multiples species based on Conflict Matrix, using a pseudo-number generator to sort which specie will win
    args:
        - conflict_arr(required): List containing all species ids that are involved in conflict
    outputs:
        - winner: species ID that won the conflict
    '''
    if len(conflict_arr)>1:
        calc_proba = lambda lst,i: sum([Species.conflict_matrix[lst[i]-1][lst[idx]-1] for idx in range(len(lst)) if idx!=i])/len(list(combinations(lst,2)))
        prob = [calc_proba(conflict_arr,i) for i in range(len(conflict_arr))] #Calculate individual probabilities of winning the conflict at all
        winner = np.random.choice(conflict_arr,p = prob)#Randomize a species
    else:
        winner = conflict_arr[0]
    return winner

def d(id: int,species: list):
    '''
    Calculate and generate a sample for a death in a square in grid
    args:
        - id(required): Specie id that populates that square
        - species(required): list of all species avaible

    outputs:
        state: 0 if the class in the square dies,1 otherwise
    '''
    if id != 0:
        state = np.random.choice([0,id],p = [species[id-1].D,1-species[id-1].D])
        return state
    else:
        return 0

def e(grid:np.array ,pos: tuple,species: list):
    '''
    Calculate and generate a sample for a born in a square in grid
    args:
        grid(required): Grid containing the information
        pos(required): Position of the square to be randomized
        species(required): list of all species avaible
    outputs:
        square_value: the class that proliferates in that direction
    '''

    i = pos[0]#row
    j = pos[1]#column
    local_value = grid[i,j] #actual value
    N = len(grid[0])#Length
    
    neighbors_idx = [[i,(j-1)],[i,(j+1)],[(i-1),j],[(i+1), j],[(i-1),(j-1)], [(i-1),(j+1)] ,[(i+1),(j-1)] ,[(i+1),(j+1)]] #List of the neighbors indices
    neighbors = [grid[neigh[0],neigh[1]] for neigh in neighbors_idx if neigh[0]<N and neigh[1]<N and neigh[0]>=0 and neigh[1]>=0]  #List of the neighbors that dont exceed the grid
    
    born_samples = [value for value in neighbors if value!=0 and np.random.choice((0,1),p=[1-species[value-1].E,species[value-1].E]) == 1] #Sort if each neighbor will reproduce in the square direction or not
    if  local_value != 0:
        born_samples.append(local_value)
    if born_samples:
        square_value = c(born_samples)
        return square_value
    else:
        return 0
    
def g(grid:np.array ,pos: tuple,species: list):
    '''
    Encapsulate all func in order and simulate a timestep result for a square
        grid(required): Grid containing the information
        pos(required): Position of the square to be randomized
        species(required): list of all species avaible
    outputs:
        compete_state: the class that end-up in that square
    '''
    previous = grid[pos[0],pos[1]]
    grid[pos[0],pos[1]] = d(previous,species)
    compete_state = e(grid,pos,species)
    return compete_state