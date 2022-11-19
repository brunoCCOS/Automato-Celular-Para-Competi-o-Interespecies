from especies import Species
from grid import Grid
import func
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

GRID_SIZE = 40
MAX_ESPECIES = 6
lamb = 50
sigma = 0.1

def update(frameNum, img,grid,arrival_func,competing_func,species,lamb):
    '''
    Encapsulate upgrade grid fun so it can be used to generate the frames
    '''
    grid.update_grid(arrival_func,competing_func,species,lamb)
    img.set_data((grid.table))
    print(grid.table)
    return img,

def main():
    species = [Species(sigma) for _ in range(MAX_ESPECIES)]
    Species.initialize_matrix(MAX_ESPECIES)

    print(Species.conflict_matrix)
    grid = Grid(GRID_SIZE)
    grid.update_grid(func.a,func.e,species,lamb) #Give some points to make animate func work
    updateInterval = 200

    #Generate plot fig
    fig, ax = plt.subplots()
    img = ax.imshow(grid.table, interpolation='nearest')
    #Update frame and makes animation
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, func.a,func.e,species,lamb), frames = 100, interval=updateInterval, save_count = 50)
    plt.show()

if __name__ == '__main__':
    main()
