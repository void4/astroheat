# Uses the grid.pickle file to visualize the data in a different way
from time import time
import pickle

import numpy as np
import matplotlib.pyplot as plt


plt.style.use('dark_background')

plt.title("astrometry.net attention contour plot")

# HD aspect ratio
plt.gcf().set_size_inches(19.2, 10.8)

# Read the starmap background and display it across the entire plot
bgimg = plt.imread("starmap2.png")
plt.imshow(bgimg, extent=[0,360,-90,90])

with open("grid.pickle", "rb") as f:
    grid = pickle.loads(f.read())

xs = np.arange(0,360,360/len(grid[0]))
ys = np.arange(90,-90,-180/len(grid))

plt.contourf(xs, ys, grid, levels=40, alpha=0.5)

# Save the figure to a file
plt.savefig(f"contour_{int(time())}.png", dpi=300)

plt.show()
