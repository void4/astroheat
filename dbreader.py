from random import randint
import csv

# requires http://broiler.astrometry.net/~dstn/temp/wcs.csv.gz
f = open("wcs.csv")
reader = csv.reader(f, delimiter=" ")

# Skip header
next(reader)

# Test objects
class M33:

	def __init__(self):
		self.x, self.y = 23.469, 30.645
		self.width, self.height = 10,10
		self.angle = 226

# Random rectangle
class Thing:

	def __init__(self):
		self.x, self.y = randint(0,359), randint(-90, 89)
		self.width, self.height = randint(1,60), randint(1,60)
		self.angle = randint(0,360)

# Rectangle with given properties
class CustomThing:
	def __init__(self, x, y, width, height, angle):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.angle = angle

# Gives a rectangle around M33 and a few random ones
def get_captures2():
	yield M33()
	for i in range(10):
		yield Thing()

# The function that is actually used to read the .csv data
def get_captures():

	for row in reader:

		# Right Ascension and Declination
		ra, dec = float(row[1]), float(row[2])

		# Scale per pixel in arcseconds per pixel
		pixscale = float(row[4])

		# Image width and height in pixels
		imagew = float(row[15])
		imageh = float(row[16])

		# Image width and height in degrees
		width = imagew * pixscale / 3600
		height = imageh * pixscale / 3600

		yield CustomThing(ra, dec, width, height, float(row[5]))
