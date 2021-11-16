from time import time
from math import floor, ceil

from astropy.coordinates import Angle
from regions import PixCoord, RectanglePixelRegion
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import numpy as np
from sklearn.preprocessing import normalize

from dbreader import get_captures
from utils import Timer

# How many subdivisions per degree
SCALE = 2

# Right ascension is plotted horizontally, Declination vertically
w = int(360*SCALE)
h = int(180*SCALE)

# Makes the background black instead of white, text and borders white
plt.style.use('dark_background')

fig, ax = plt.subplots(1, 1)

# HD aspect ratio
fig.set_size_inches(19.2, 10.8)

plt.title("astrometry.net attention heatmap")

plt.xlim(0, 360)
plt.ylim(-90, 90)

# We want pixels to be squares
ax.set_aspect('equal')

# Read the starmap background and display it across the entire plot
bgimg = plt.imread("starmap.png")
ax.imshow(bgimg, extent=[0,360,-90,90])

credits = "Background by Dominic Ford 2011-2021, from https://in-the-sky.org/data/constellations_map.php"
plt.text(0, -100, credits, fontsize=8)

# We use a floating point grid to count, because there may be more than 255 rectangles above one pixel (risking overflow/oversaturation)
# Later, we normalize the grid to 0-1 and then scale up to 255 to get the RGB values
grid = np.zeros((h,w))

def to_color(value):
	return (int(value), 0, 0, 50)

patches = []

# Read the csv row by row, allowing for early KeyboardInterrupt for testing with fewer patches
try:
	for capture_index, capture in enumerate(get_captures()):

		if capture_index % 100 == 0:
			print(capture_index)

		if capture_index == 25000:
			break

		angle = Angle(capture.angle, 'deg')

		center = PixCoord(x=capture.x, y=capture.y)
		reg = RectanglePixelRegion(center=center, width=capture.width,
			                       height=capture.height, angle=angle)

		patch = reg.as_artist(facecolor=(1,1,0,0.3), edgecolor=(1,0,0,0.3), lw=1, fill=True)

		# We could render the rectangles with matplotlib, but the oversaturation problem would occur
		#ax.add_patch(patch)
		#patch.set_rasterized(True)
		patches.append(patch)

except KeyboardInterrupt:
	pass

print(len(patches), "patches")

timer = Timer()

for patch_index, patch in enumerate(patches):

	if patch_index % 100 == 0:
		print("%.2f" % (patch_index/len(patches)*100))

	bbox = patch.get_tightbbox(None)
	points = []
	extra = 5
	for y in np.arange(int(floor(bbox.ymin-extra)), int(ceil(bbox.ymax+extra)), 1/SCALE):
		for x in np.arange(int(floor(bbox.xmin-extra)), int(ceil(bbox.xmax+extra)), 1/SCALE):
			points.append([x,y])

	results = patch.contains_points(points)

	for result_index, result in enumerate(results):
		if result:
			x, y = points[result_index]
			if 0 <= x < 360 and -90 <= y < 90:# and patch.contains_point((x,y)):

				ry = int(round((-y+90)*SCALE))
				rx = int(round((360-x)*SCALE))

				if 0 < ry < h and 0 < rx < w:
					grid[ry][rx] += 1

print("%.2f" % (len(patches)/timer.next()), "patches/second")

print(len(patches), "patches")

# Normalize the grid to float 0-1
# TODO scale logarithmically?
grid += 1
grid = np.log(grid)
grid /= grid.max()

import pickle

with open("grid.pickle", "wb+") as f:
	f.write(pickle.dumps(grid))

# Scale to 0-255 and cast to unsigned integer
grid = np.uint8(grid*255)

img = Image.fromarray(grid).convert("RGBA")

# Split the image into its color channels to adjust them
r,g,b,a = img.split()

#r = r.point(lambda i:0)
g = g.point(lambda i:i*0.3)
b = b.point(lambda i:0)

# Merge the color channels back together into an image
img = Image.merge("RGBA", (r,g,b,a))

# Make the image a bit transparent and display it just like the background image
img.putalpha(127)
ax.imshow(img, extent=[0,360,-90,90])

# Save the figure to a file
plt.savefig(f"{int(time())}_{len(patches)}.png", dpi=300)

# And finally display the interactive matplotlib window
plt.show()
