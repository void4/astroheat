# Uses the grid.pickle file to visualize the data in a different way
from time import time
import pickle

import numpy as np
import matplotlib.pyplot as plt


plt.style.use('dark_background')

LOGSCALING = False

SCALING = "log" if LOGSCALING else "linear"

plt.title(f"astrometry.net attention contour plot ({SCALING} scaling)")

# HD aspect ratio
plt.gcf().set_size_inches(19.2, 10.8)

# Read the starmap background and display it across the entire plot
bgimg = plt.imread("starmap2.png")
plt.imshow(bgimg, extent=[0,360,-90,90])

credits = "Background by Dominic Ford 2011-2021, from https://in-the-sky.org/data/constellations_map.php"
plt.text(0, 91, credits, fontsize=8)

credits = "Data graciously supplied by astrometry.net, created by void4"
plt.text(292, 91, credits, fontsize=8)

with open("grid.pickle", "rb") as f:
    grid = pickle.loads(f.read())

xs = np.arange(0,360,360/len(grid[0]))
ys = np.arange(90,-90,-180/len(grid))

if LOGSCALING:
    grid += 1
    grid = np.log10(grid)

gridmax = grid.max()
grid /= gridmax
grid *= 255

print(gridmax)

cs = plt.contourf(xs, ys, grid, levels=40, alpha=0.5, cmap="viridis")

proxy = [plt.Rectangle((0,0),1,1,fc = pc.get_facecolor()[0])
    for pc in cs.collections]

print(dir(cs.collections[0]))
truevalues = [v/255*gridmax for v in cs.cvalues]
print(truevalues)

plt.legend(proxy, [f"range({int(v)}-{int(truevalues[i+1]) if i+1 < len(truevalues) else int(gridmax)})" for i, v in enumerate(truevalues)])

plt.tight_layout()

# Save the figure to a file
plt.savefig(f"contour_{int(time())}.png", dpi=300)

plt.show()
