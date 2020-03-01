def map_range(val, oldmin, oldmax, min, max):
	return (val - oldmin) / (oldmax - oldmin) * (max - min) + min

def clamp(val, min, max):
	if val <= min: return min
	if val >= max: return max
	return val

def clamp01(val):
	return clamp(val, 0, 1)


class Point(tuple):

	def __init__(self, pos):
		self.x = pos[0]
		self.y = pos[1]

	def __getitem__(self, key):
		if key == 0: return self.x
		if key == 1: return self.y
		raise ValueError

	def __add__(self, other):
		if not isinstance(other, tuple): raise TypeError
		return Point((self.x + other[0], self.y + other[1]))

	def __sub__(self, other):
		if not isinstance(other, tuple): raise TypeError
		return Point((self.x - other[0], self.y - other[1]))

	def __mul__(self, other):
		if isinstance(other, (int, float)):
			return Point((self.x * other, self.y * other))
		if isinstance(other, tuple):
			return Point((self.x * other[0], self.y * other[1]))
		raise TypeError

	def __rmul__(self, other):
		return self * other

	def __str__(self):
		return 'Point({}, {})'.format(self.x, self.y)

	def toint(self):
		return Point((int(self.x), int(self.y)))