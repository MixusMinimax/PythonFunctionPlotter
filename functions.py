import numpy as np
import math
import random
from abc import ABCMeta, abstractmethod


class Function:

	@abstractmethod
	def sample(self, x):
		pass

	def __neg__(self):
		return -1 * self

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

	def __truediv__(self, other):
		if isinstance(other, (int, float)):
			return Product((self, Constant(1 / other)))
		if not isinstance(other, Function): raise TypeError
		return Fraction(self, other)

	def __rtruediv__(self, other):
		if isinstance(other, (int, float)):
			return Constant(other) / self
		raise TypeError

	def __pow__(self, other):
		if isinstance(other, (int, float)):
			return Pow(self, Constant(other))
		if not isinstance(other, Function): raise TypeError
		return Pow(self, other)

	def __rpow__(self, other):
		if isinstance(other, (int, float)):
			return Constant(other) ** self
		raise TypeError


class Constant(Function):

	def __init__(self, value):
		self.value = value

	def sample(self, x):
		return self.value

	def __str__(self):
		return str(self.value)


class Random(Function):

	def __init__(self, seed):
		self.seed = seed

	def sample(self, x):
		#random.seed(a=int(x * 10 * self.seed))
		return random.randint(0, 1000) / 1000.0

	def __str__(self):
		return 'random({})'.format(self.seed)


class X(Function):

	def sample(self, x):
		return x

	def __str__(self):
		return 'x'


class Sum(Function):

	def __init__(self, summands):
		self.summands = summands

	def sample(self, x):
		return sum((f.sample(x) for f in self.summands))

	def __str__(self):
		return '(' + ' + '.join([str(f) for f in self.summands]) + ')'


class Product(Function):

	def __init__(self, factors):
		self.factors = factors

	def sample(self, x):
		return np.prod([f.sample(x) for f in self.factors])

	def __str__(self):
		return '(' + ' * '.join([str(f) for f in self.factors]) + ')'


class Fraction(Function):

	def __init__(self, dividend, divisor):
		self.dividend = dividend
		self.divisor = divisor

	def sample(self, x):
		return self.dividend.sample(x) / self.divisor.sample(x)

	def __str__(self):
		return '{} / {}'.format(self.dividend, self.divisor)


class Sin(Function):

	def __init__(self, input):
		self.input = input

	def sample(self, x):
		return math.sin(self.input.sample(x))

	def __str__(self):
		return 'sin({})'.format(self.input)


class Cos(Function):

	def __init__(self, input):
		self.input = input

	def sample(self, x):
		return math.cos(self.input.sample(x))

	def __str__(self):
		return 'cos({})'.format(self.input)


class Pow(Function):

	def __init__(self, base, exponent):
		self.base = base
		self.exponent = exponent

	def sample(self, x):
		return self.base.sample(x) ** self.exponent.sample(x)

	def __str__(self):
		return '{}^{}'.format(self.base, self.exponent)

class Exp(Function):

	def __init__(self, input):
		self.input = input

	def sample(self, x):
		return math.exp(self.input.sample(x))

	def __str__(self):
		return 'exp({})'.format(self.input)