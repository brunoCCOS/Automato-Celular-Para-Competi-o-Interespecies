from especies import Species
from grid import Grid
import func
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation
import pickle
from IPython import display
import itertools
import sys

GRID_SIZE = 80
MAX_ESPECIES = 12
LAMB = 20
SIGMA = 0.05
LOAD_STATE = False#If true load serialized objects from previous sim
SAVE_STATE = False#If true serialize objects in the for post sims
SAVE_IMAGE = True#If true animation will not be displayed, only the final frames the it will need to be closed
GRID_SEARCH = False# If true will run for all combinations betwen params below, if false, only runs for default values

#Grid of hyper params
l = [20,50,150]
sig = [0.01,0.05,0.1]
MAX = [6,12]
args = [l,sig,MAX]

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
        #reset inidivual count atributes for each re sim
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
def main(lamb = LAMB, sigma = SIGMA, MAX_ESPECIES = MAX_ESPECIES):
    if LOAD_STATE:#load previous state
        species,Species.conflict_matrix = load_run()
    else: #create new objects states to the run
        species = [Species(sigma) for _ in range(MAX_ESPECIES)]
        Species.initialize_matrix(MAX_ESPECIES)
    print(Species.conflict_matrix)
    grid = Grid(GRID_SIZE)
    
    #Update the grid until it has at least one species in it for matters of plotting in animation.
    while not grid.table.any():
        grid.update_grid(func.a,func.e,species,lamb) #Give some points to make animate func work
    updateInterval = 100

    #Generate plot fig
    fig, ax = plt.subplots()
    img = ax.imshow(grid.table, interpolation='nearest',cmap='viridis')
    # colormap used by imshow
    colors = [ img.cmap(img.norm(value)) for value in range(len(species)+1)]
    # create a patch (proxy artist) for every color 
    patches = [ mpatches.Patch(color=colors[i], label=f"{'Empty' if i==0 else 'Specie'+str(i)}".format(l=i) ) for i in range(len(species)+1) ]
    # put those patched as legend-handles into the legend
    plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0. )
    #Update frame and makes animation
    ani = animation.FuncAnimation(fig, animate, fargs=(img, grid, func.a,func.e,species,lamb), frames = 120, interval=updateInterval, save_count = 15000)
    #Save animation animated video and last frame state.
    if SAVE_IMAGE:
        print('Saving image, it may take a while...')
        ani.save(f'./sims/s={MAX_ESPECIES}_lambda={lamb}_sigma={sigma}_animated.gif', writer="Pillow",fps=60)
        fig.savefig(f'./sims/s={MAX_ESPECIES}_lambda={lamb}_sigma={sigma}.png')
        plt.close()
    else:
        plt.show()

    #Plot individual numbers over time
    fig, ax = plt.subplots(2)
    fig.set_figheight(5)
    fig.set_figwidth(10)
    for specie in species:
        ax[1].scatter(specie.D,specie.E,color=colors[specie.id])
        ax[0].plot(np.array(range(len(specie.historical_individual))),specie.historical_individual, label = f'Species: {specie.id}',c = colors[specie.id])
        fig.legend()
    #Saving img in sims folder
    if SAVE_IMAGE:
        plt.savefig(f'./sims/s={MAX_ESPECIES}_lambda={lamb}_sigma={sigma}_graf.jpg')
    else:
        plt.show()
    #Save state for future runs
    if SAVE_STATE:
        save_run(species,Species.conflict_matrix)

if __name__ == '__main__':
    main(50, 0.1, 6)

#[(20, 0.01, 6), ((20, 0.01, 12)), (20, 0.05, 6), (20, 0.05, 12), (20, 0.1, 6), (20, 0.1, 12), (50, 0.01, 6), (50, 0.01, 12), (50, 0.05, 6), (50, 0.05, 12), (50, 0.1, 6), (50, 0.1, 12), (150, 0.01, 6), (150, 0.01, 12), (150, 0.05, 6), (150, 0.05, 12), (150, 0.1, 6), (150, 0.1, 12)]