from especies import Species
from grid import Grid
import func
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pickle

GRID_SIZE = 40
MAX_ESPECIES = 12
lamb = 50
sigma = 0.05
LOAD_STATE = False
SAVE_STATE = True


def animate(frameNum, img,grid,arrival_func,competing_func,species,lamb):
    '''
    Encapsulate upgrade grid fun so it can be used to generate the frames
    '''
    grid.update_grid(arrival_func,competing_func,species,lamb)

    for specie in species:
        specie.add_timestamp()

    img.set_data((grid.table))
    return img,

def load_run():
    '''
    Deserialize last saved list of species
    '''
    with open("./species/species.pickle", "rb") as infile:
        species = pickle.load(infile)
        for specie in species:
            specie.individuals = 0 #Reset number of individuals
            specie.historical_individual = list() #Reset number of individuals            
    with open("./species/conf_matrix.pickle", "rb") as infile:
        conf_matrix = pickle.load(infile)
    
    return species,conf_matrix

def save_run(species: list,conf_matrix: np.array):
    '''
    Serialize lsit of species and save it
    args:
        species(required): List os objects to be serialized
        conf_matrix(required): Conflict matrix
    '''
    with open("./species/species.pickle", "wb") as outfile:
        # "wb" argument opens the file in binary mode
        pickle.dump(species, outfile)
    with open("./species/conf_matrix.pickle", "wb") as outfile:
        # "wb" argument opens the file in binary mode
        pickle.dump(conf_matrix, outfile)
def main():
    if LOAD_STATE:#load previous state
        species,Species.conflict_matrix = load_run()
    else: #create new objects states to the run
        species = [Species(sigma) for _ in range(MAX_ESPECIES)]
        Species.initialize_matrix(MAX_ESPECIES)
    print(Species.conflict_matrix)
    grid = Grid(GRID_SIZE)
    grid.update_grid(func.a,func.e,species,lamb) #Give some points to make animate func work
    updateInterval = 500

    #Generate plot fig
    fig, ax = plt.subplots()
    img = ax.imshow(grid.table, interpolation='nearest')
    #Update frame and makes animation
    ani = animation.FuncAnimation(fig, animate, fargs=(img, grid, func.a,func.e,species,lamb), frames = 20, interval=updateInterval, save_count = 50)
    plt.show()
    
    #Plot individual numbers over time
    
    for specie in species:
        print(specie.id, specie.historical_individual)
        plt.legend()
        plt.plot(np.array(range(len(specie.historical_individual))),specie.historical_individual, label = f'Espécia {specie.id}')
    
    plt.show()
    
    if SAVE_STATE:
        save_run(species,Species.conflict_matrix)

if __name__ == '__main__':
    main()
