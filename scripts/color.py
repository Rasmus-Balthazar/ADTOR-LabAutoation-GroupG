


class Color():
	def __init__(self, red, green, blue):
		self.red = red
		self.green = green
		self.blue = blue
	
	def distance(self, col):
		return ((self.red - col.red)**2 + (self.green - col.green)**2 + (self.blue - col.blue)**2)/3