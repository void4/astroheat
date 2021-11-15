from time import time

# For statistics and debugging purposes
class Timer:
	def __init__(self):
		self.time = time()
		self.i = 0

	def next(self):
		nxt = time()
		#print(self.i, nxt-self.time)
		delta = nxt-self.time
		self.time = nxt
		self.i += 1
		return delta
