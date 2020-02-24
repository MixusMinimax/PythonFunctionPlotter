def map_range(val, oldmin, oldmax, min, max):
	return (val - oldmin) / (oldmax - oldmin) * (max - min) + min

def clamp(val, min, max):
	if val <= min: return min
	if val >= max: return max
	return val

def clamp01(val):
	return clamp(val, 0, 1)