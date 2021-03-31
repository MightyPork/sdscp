#!/bin/env python3

import ast
import operator as op
import functools
from sdscp_errors import *

def append(arr, added):
	""" Append to array, both array or item """

	if (added is None) or (arr is None):
		return

	if type(added) == list:
		arr.extend(added)
	else:
		arr.append(added)


class Obj(object):
	""" Anonymous attribute bundle """

	def __init__(self, **kwargs):
		self.__dict__.update(kwargs)


class SyntaxNode:
	""" Abstract syntactical node.

	Attributes:
		parent (Statement):
			reference to parent statement, used for refactoring.

	"""

	def __init__(self):
		self.parent = None


	def bind_parent(self, parent):
		""" Bind parent statement to this statement,
		bind also child statements.

		"""

		self.parent = parent
		self._bind_children()


	def _bind_children(self):
		""" Bind self to children as parent. """

		pass  # stub


	def get_parent(self, cls=None):
		""" Get parent of given type (skips all parents of different types)

		Args:
			cls (Class): required class for the parent

		Returns: parent of the given type
		Throws: error if no such parent found.

		"""

		if cls is None:
			return self.parent
		else:
			if self.parent is None:
				return None

			if isinstance(self.parent, cls):
				return self.parent

			return self.parent.get_parent(cls)



### EXPRESSION EVALUATOR ###
# This part uses python expression parser to simplify expressions.
# It's no way 100% reliable but seems to work quite good.

# supported operators
operators = {
	ast.Add: op.add,
	ast.Sub: op.sub,
	ast.Mult: op.mul,
	ast.Div: op.truediv,
	ast.Pow: op.pow,
	ast.USub: op.neg,
	ast.BitXor: op.xor,
	ast.BitOr: op.or_,
	ast.BitAnd: op.and_,
	ast.Or: op.or_,
	ast.And: op.and_,
	ast.Not: op.not_,
	ast.LShift: op.lshift,
	ast.RShift: op.rshift,

	ast.NotEq: op.ne,
	ast.Eq: op.eq,
	ast.Compare: op.eq, #?
	ast.Gt: op.gt,
	ast.Lt: op.lt,
	ast.GtE: op.ge,
	ast.LtE: op.le,
}

def eval_expr(expr):
	expr = expr \
		.replace("&&", " and ") \
		.replace("||", " or ") \
		.replace("!", " not ") \
		.strip()

	#print(expr)
	parsed = ast.parse(expr, mode='eval').body
	return eval_(parsed)

def eval_(node):
	if isinstance(node, ast.Num): # <number>
		return node.n
	elif isinstance(node, ast.BinOp): # <left> <operator> <right>
		return operators[type(node.op)](eval_(node.left), eval_(node.right))
	
	elif isinstance(node, ast.BoolOp): # <left> <operator> <right>
		operator = operators[type(node.op)]
		evaled = [eval_(v) for v in node.values]
		prev = evaled[0]
		for v in evaled[1:]:
			prev = operator(prev, v)
		return prev

	elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
		return operators[type(node.op)](eval_(node.operand))

	elif isinstance(node, ast.Compare): # blah <= boo

		if len(node.ops) != 1:
			raise SyntaxError("Could not parse, compound compare operator.")
		if len(node.comparators) != 1:
			raise SyntaxError("Could not parse, compound compare comparators.")

		return operators[type(node.ops[0])](eval_(node.left), eval_(node.comparators[0]))
	else:
		raise TypeError(node)

def power(a, b):
	if any(abs(n) > 100 for n in [a, b]):
		raise ValueError((a,b))
	return op.pow(a, b)

operators[ast.Pow] = power
