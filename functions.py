import numpy as np
import math
import random
from abc import ABCMeta, abstractmethod


class Function:

	@abstractmethod
	def sample(self, x):
		pass

	def __add__(self, other):
		if isinstance(other, (int, float)):
			return Sum((self, Constant(other)))
		if not isinstance(other, Function): raise TypeError
		return Sum((self, other))

	def __radd__(self, other):
		return self + other

	def __sub__(self, other):
		if isinstance(other, (int, float)):
			return sum((self, Constant(-other)))
		if not isinstance(other, Function): raise TypeError
		return Sum((self, -1 * other))

	def __rsub__(self, other):
		if not isinstance(other, (int, float)): raise TypeError
		return Constant(other) - self

	def __mul__(self, other):
		if isinstance(other, (int, float)):
			return Product((self, Constant(other)))
		if not isinstance(other, Function): raise TypeError
		return Product((self, other))

	def __rmul__(self, other):
		return self * other


class Constant(Function):

	def __init__(self, value):
		self.value = value

	def sample(self, x):
		return self.value


class Random(Function):

	def __init__(self, seed):
		self.seed = seed

	def sample(self, x):
		random.seed(a=int(x * 10 * self.seed))
		return random.randint(20, 60) / 10.0


class X(Function):

	def sample(self, x):
		return x


class Sum(Function):

	def __init__(self, summands):
		self.summands = summands

	def sample(self, x):
		return sum((f.sample(x) for f in self.summands))


class Product(Function):

	def __init__(self, factors):
		self.factors = factors

	def sample(self, x):
		return np.prod([f.sample(x) for f in self.factors])


class Sin(Function):

	def __init__(self, input):
		self.input = input

	def sample(self, x):
		return math.sin(self.input.sample(x))

class Cos(Function):

	def __init__(self, input):
		self.input = input

	def sample(self, x):
		return math.cos(self.input.sample(x))