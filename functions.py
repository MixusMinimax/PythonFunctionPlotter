import numpy as np
import math
import time
import random
import re
from abc import ABCMeta, abstractmethod

current_time = 0

replaces = [('x', 'X()'), ('exp', 'Exp'), ('ln', 'Ln'), ('sqrt', 'Sqrt'), ('sin', 'Sin'), ('cos', 'Cos'),\
	('tan', 'Tan'),('random', 'Random'), ('t', 'Time()')]

def check_function(function):
	if not isinstance(function, Function):
		raise TypeError

# Turns numberes into Constants, but does nothing to functions
def to_function(value):
	if isinstance(value, (int, float)):
		return Constant(value)
	if not isinstance(value, Function): raise TypeError
	return value

def parse(t, verbose=True):
	if isinstance(t, Function): return t
	try:
		start = time.time()
		for pair in replaces:
			t = re.sub(r'\b%s\b'% pair[0], pair[1], t)
		derivative_level = 0
		while t.startswith('derivative '):
			t = t[len('derivative '):]
			derivative_level += 1
		if derivative_level > 0:
			t = '({}){}'.format(t, '.derivative()' * derivative_level)
		if verbose: print('===[PARSING]===')
		if verbose: print('Input:      {}'.format(t))
		f = to_function(eval(t))
		if verbose: print('Result:     {}'.format(f))
		if isinstance(f, Function):
			f = f.simplify()
			time_taken = time.time() - start
			if verbose: print('Time taken: {}s'.format(time_taken))
			return f
		raise TypeError
	except:
		if verbose: print('Invalid Input')
		return None


class Function:

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
		return Sum((self, other))

	def __radd__(self, other):
		if not isinstance(other, (int, float)): raise TypeError
		return self + other

	def __sub__(self, other):
		return Sum((self, -other))

	def __rsub__(self, other):
		if not isinstance(other, (int, float)): raise TypeError
		return Constant(other) - self

	def __mul__(self, other):
		return Product((self, other))

	def __rmul__(self, other):
		if not isinstance(other, (int, float)): raise TypeError
		return self * other

	def __mod__(self, other):
		return Modulo(self, other)

	def __truediv__(self, other):
		return Fraction(self, other)

	def __rtruediv__(self, other):
		if not isinstance(other, (int, float)): raise TypeError
		return Constant(other) / self

	def __pow__(self, other):
		return Pow(self, other)

	def __rpow__(self, other):
		if not isinstance(other, (int, float)): raise TypeError
		return Constant(other) ** self


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
		self.summands = tuple([to_function(f) for f in summands])

	def sample(self, x):
		return sum((f.sample(x) for f in self.summands))

	def derivative(self):
		return Sum([f.derivative() for f in self.summands]).simplify()

	def simplify(self):
		summands = [f.simplify() for f in self.summands]

		# flatmap nested sums
		sums = [f.summands for f in summands if isinstance(f, Sum)]
		flatmappedsums = [f for fs in sums for f in fs]
		summands = [f for f in summands if not isinstance(f, Sum)]
		summands.extend(flatmappedsums)

		# simplify constants into one
		simplified_constant = Constant(sum([f.value for f in summands if isinstance(f, Constant)]))
		summands = [f for f in summands if not isinstance(f, Constant)]
		if len(summands) == 0 or simplified_constant.value != 0:
			summands.append(simplified_constant)

		# factorize sames
		counts = dict()
		for f in summands:
			if str(f) in counts:
				counts[str(f)][1] += 1
			else:
				counts[str(f)] = [f, 1]

		changed = False
		new_summands = []
		for key in counts:
			pair = counts[key]
			f = pair[0]
			count = pair[1]
			if count == 1:
				new_summands.append(f)
			elif count > 1:
				changed = True
				new_summands.append(Product((Constant(count), f)))

		if len(new_summands) == 0:
			return Constant(0)
		elif len(new_summands) == 1:
			return new_summands[0]

		ret = Sum(new_summands)
		return ret.simplify() if changed else ret

	def __str__(self):
		s = ' + '.join([str(f) for f in self.summands])
		if len(self.summands) > 1:
			return '({})'.format(s)
		else:
			return s


class Product(Function):

	def __init__(self, factors):
		self.factors = tuple([to_function(f) for f in factors])

	def sample(self, x):
		return np.prod([f.sample(x) for f in self.factors])

	def derivative(self):
		if len(self.factors) == 1:
			return self.factors[0].derivative().simplify()
		elif len(self.factors) == 2:
			return (self.factors[0].derivative() * self.factors[1]\
					+ self.factors[0] * self.factors[1].derivative()).simplify()
		return Product([Product(self.factors[0:2]), Product(self.factors[2:])]).derivative().simplify()

	def simplify(self):
		factors = [f.simplify() for f in self.factors]
		if 0 in [f.value for f in factors if isinstance(f, Constant)]:
			return Constant(0)

		# flatmap nested products
		products = [f.factors for f in factors if isinstance(f, Product)]
		flatmappedproducts = [f for fs in products for f in fs]
		factors = [f for f in factors if not isinstance(f, Product)]
		factors.extend(flatmappedproducts)

		# simplify constants into one
		simplified_constant = Constant(np.prod([f.value for f in factors if isinstance(f, Constant)]))
		factors = [f for f in factors if not isinstance(f, Constant)]
		if len(factors) == 0 or abs(simplified_constant.value - 1) > 1e-9:
			factors.insert(0, simplified_constant)

		# powerize sames
		counts = dict()
		for f in factors:
			if str(f) in counts:
				counts[str(f)][1] += 1
			else:
				counts[str(f)] = [f, 1]

		changed = False
		new_factors = []
		for key in counts:
			pair = counts[key]
			f = pair[0]
			count = pair[1]
			if count == 1:
				new_factors.append(f)
			elif count > 1:
				changed = True
				new_factors.append(Pow(f, Constant(count)))

		if len(new_factors) == 0:
			return Constant(0)
		elif len(new_factors) == 1:
			return new_factors[0]

		ret = Product(new_factors)
		return ret.simplify() if changed else ret

	def __str__(self):
		s = ' * '.join([str(f) for f in self.factors])
		if len(self.factors) > 1:
			return '({})'.format(s)
		else:
			return s


class Modulo(Function):

	def __init__(self, a, b):
		self.a = to_function(a)
		self.b = to_function(b)

	def sample(self, x):
		return self.a.sample(x) % self.b.sample(x)

	def derivative(self):
		return self.a.derivative().simplify()

	def simplify(self):
		return self.a.simplify() % self.b.simplify()

	def __str__(self):
		return '{} % {}'.format(self.a, self.b)


class Fraction(Function):

	def __init__(self, dividend, divisor):
		self.dividend = to_function(dividend)
		self.divisor = to_function(divisor)

	def sample(self, x):
		return self.dividend.sample(x) / self.divisor.sample(x)

	def derivative(self):
		return (self.dividend.derivative().simplify() * self.divisor\
			- self.dividend * self.divisor.derivative().simplify()) /\
				(self.divisor ** 2).simplify()

	def simplify(self):
		return self.dividend.simplify() / self.divisor.simplify()

	def __str__(self):
		return '{} / {}'.format(self.dividend, self.divisor)


class Sin(Function):

	def __init__(self, input):
		self.input = to_function(input)

	def sample(self, x):
		return math.sin(self.input.sample(x))

	def derivative(self):
		return Cos(self.input) * self.input.derivative().simplify()

	def simplify(self):
		return Sin(self.input.simplify())

	def __str__(self):
		return 'sin({})'.format(self.input)


class Cos(Function):

	def __init__(self, input):
		self.input = to_function(input)

	def sample(self, x):
		return math.cos(self.input.sample(x))

	def derivative(self):
		return -Sin(self.input) * self.input.derivative().simplify()

	def simplify(self):
		return Cos(self.input.simplify())

	def __str__(self):
		return 'cos({})'.format(self.input)


class Tan(Function):

	def __init__(self, input):
		self.input = to_function(input)

	def sample(self, x):
		return math.tan(self.input.sample(x))

	def derivative(self):
		return Fraction(1, Pow(Cos(self.input), 2)) * self.input.derivative().simplify()

	def simplify(self):
		return Tan(self.input.simplify())

	def __str__(self):
		return 'tan({})'.format(self.input)


class Pow(Function):

	def __init__(self, base, exponent):
		self.base = to_function(base)
		self.exponent = to_function(exponent)

	def sample(self, x):
		return self.base.sample(x) ** self.exponent.sample(x)

	def derivative(self):
		# TODO
		base = self.base.simplify()
		exponent = self.exponent.simplify()
		if isinstance(base, Constant) and isinstance(exponent, Constant):
			return Constant(0)
		if isinstance(base, Constant):
			return (Ln(base) * self * exponent.derivative()).simplify()
		if isinstance(exponent, Constant):
			return (exponent * (base ** Constant(exponent.value - 1)) * base.derivative()).simplify()
		raise NotImplementedError

	def simplify(self):
		base = self.base.simplify()
		exponent = self.exponent.simplify()
		if isinstance(base, Constant) and base.value == 1:
			return Constant(1)
		if isinstance(exponent, Constant) and exponent.value == 1:
			return base
		return base ** exponent

	def __str__(self):
		return '{}^{}'.format(self.base, self.exponent)

class Exp(Function):

	def __init__(self, input):
		self.input = to_function(input)

	def sample(self, x):
		return math.exp(self.input.sample(x))

	def derivative(self):
		return Exp(self.input) * self.input.derivative().simplify()

	def simplify(self):
		input = self.input.simplify()
		if isinstance(input, Constant) and input.value == 0:
			return Constant(1)
		return Exp(input)

	def __str__(self):
		return 'exp({})'.format(self.input)


class Ln(Function):

	def __init__(self, input):
		self.input = to_function(input)

	def sample(self, x):
		return math.log(self.input.sample(x))

	def derivative(self):
		return self.input.derivative().simplify() / self.input

	def simplify(self):
		input = self.input.simplify()
		if isinstance(input, Constant) and input.value == 1:
			return Constant(0)
		return Ln(input)


	def __str__(self):
		return 'ln({})'.format(self.input)


class Sqrt(Function):

	def __init__(self, input):
		self.input = input

	def sample(self, x):
		return math.sqrt(self.input.sample(x))

	def derivative(self):
		return Constant(0.5) * self.input.derivative().simplify() / Sqrt(self.input)

	def simplify(self):
		input = self.input.simplify()
		if isinstance(input, Constant):
			n = math.sqrt(input.value)
			if n == int(n):
				return Constant(n)
		return Sqrt(self.input.simplify())

	def __str__(self):
		return 'sqrt({})'.format(self.input)


class Time(Function):

	def sample(self, x):
		return current_time

	def derivative(self):
		return Constant(0)

	def simplify(self):
		return self

	def __str__(self):
		return 't'


class Random(Function):

	def __init__(self, seed):
		seed = to_function(seed)
		self.seed = seed

	def sample(self, x):
		random.seed(a=int((self.seed.sample(x) * 1000 + 0x7fffffff)))
		return random.randint(0, 1000) / 1000.0

	def derivative(self):
		return Constant(0)

	def simplify(self):
		return Random(self.seed.simplify())

	def __str__(self):
		return 'random({})'.format(self.seed)