import numpy as np
import math
import time
import random
import re
from abc import ABCMeta, abstractmethod

time = 0

replaces = [('x', 'X()'), ('exp', 'Exp'), ('sin', 'Sin'), ('cos', 'Cos'),\
	('random', 'Random'), ('t', 'Time()')]

def check_function(function):
	if not isinstance(function, Function):
		raise TypeError


class Function:

	def parse(t):
		for pair in replaces:
			t = re.sub(r'\b%s\b'% pair[0], pair[1], t)
		f = eval('Constant(0)+' + t)
		if isinstance(f, Function):
			return f.simplify()
		raise TypeError

	@abstractmethod
	def sample(self, x):
		pass

	@abstractmethod
	def derivative(self):
		pass

	@abstractmethod
	def simplify(self):
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

	def __mod__(self, other):
		if isinstance(other, (int, float)):
			return Modulo(self, Constant(other))
		if not isinstance(other, Function): raise TypeError
		return Modulo(self, other)

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

	def derivative(self):
		return Constant(0)

	def simplify(self):
		return self

	def __str__(self):
		return str(self.value)


class Random(Function):

	def __init__(self, seed):
		if isinstance(seed, (int, float)):
			seed = Constant(seed)
		if not isinstance(seed, Function): raise TypeError
		self.seed = seed

	def sample(self, x):
		random.seed(a=int((self.seed.sample(x) * 1000 + 0x7fffffff)))
		return random.randint(0, 1000) / 1000.0

	def derivative(self):
		return Constant(0)

	def simplify(self):
		return self

	def __str__(self):
		return 'random({})'.format(self.seed)


class X(Function):

	def sample(self, x):
		return x

	def derivative(self):
		return Constant(1)

	def simplify(self):
		return self

	def __str__(self):
		return 'x'


class Sum(Function):

	def __init__(self, summands):
		self.summands = summands

	def sample(self, x):
		return sum((f.sample(x) for f in self.summands))

	def derivative(self):
		return Sum([f.derivative() for f in self.summands])

	def simplify(self):
		return self

	def __str__(self):
		return '(' + ' + '.join([str(f) for f in self.summands]) + ')'


class Product(Function):

	def __init__(self, factors):
		self.factors = factors

	def sample(self, x):
		return np.prod([f.sample(x) for f in self.factors])

	def derivative(self):
		if len(self.factors) == 1:
			return self.factors[0].derivative()
		elif len(self.factors) == 2:
			return self.factors[0].derivative() * self.factors[1]\
					+ self.factors[0] * self.factors[1].derivative()
		return Product([Product(self.factors[0:2]), Product(self.factors[2:])]).derivative()

	def simplify(self):
		return self

	def __str__(self):
		return '(' + ' * '.join([str(f) for f in self.factors]) + ')'


class Modulo(Function):

	def __init__(self, a, b):
		self.a = a
		self.b = b

	def sample(self, x):
		return self.a.sample(x) % self.b.sample(x)

	def derivative(self):
		return self.a.derivative()

	def simplify(self):
		return self

	def __str__(self):
		return '{} % {}'.format(self.a, self.b)


class Fraction(Function):

	def __init__(self, dividend, divisor):
		self.dividend = dividend
		self.divisor = divisor

	def sample(self, x):
		return self.dividend.sample(x) / self.divisor.sample(x)

	def derivative(self):
		return (self.dividend.derivative() * self.divisor - self.dividend * self.divisor.derivative()) /\
				self.divisor ** 2

	def simplify(self):
		return self

	def __str__(self):
		return '{} / {}'.format(self.dividend, self.divisor)


class Sin(Function):

	def __init__(self, input):
		self.input = input

	def sample(self, x):
		return math.sin(self.input.sample(x))

	def derivative(self):
		return Cos(self.input) * self.input.derivative()

	def simplify(self):
		return self

	def __str__(self):
		return 'sin({})'.format(self.input)


class Cos(Function):

	def __init__(self, input):
		self.input = input

	def sample(self, x):
		return math.cos(self.input.sample(x))

	def derivative(self):
		return -Sin(self.input) * self.input.derivative()

	def simplify(self):
		return self

	def __str__(self):
		return 'cos({})'.format(self.input)


class Pow(Function):

	def __init__(self, base, exponent):
		self.base = base
		self.exponent = exponent

	def sample(self, x):
		return self.base.sample(x) ** self.exponent.sample(x)

	def derivative(self):
		return exponent * Pow(self.base, self.exponent - Constant(1))

	def simplify(self):
		return self

	def __str__(self):
		return '{}^{}'.format(self.base, self.exponent)

class Exp(Function):

	def __init__(self, input):
		self.input = input

	def sample(self, x):
		return math.exp(self.input.sample(x))

	def derivative(self):
		return Exp(self.input) * self.input.derivative()

	def simplify(self):
		return self

	def __str__(self):
		return 'exp({})'.format(self.input)

class Time(Function):

	def sample(self, x):
		return time / 60

	def derivative(self):
		return Constant(0)

	def simplify(self):
		return self

	def __str__(self):
		return 't'