#!/bin/env python3

import ast
import operator as op
import functools

def append(arr, added):
	""" Append to array, both array or item """

	if (added is None) or (arr is None):
		return

	if type(added) == list:
		arr.extend(added)
	else:
		arr.append(added)


class CompatibilityError(SyntaxError):
	""" Error caused by incompatibility of the source code
	with SDS-C target syntax. The code may be valid, but not
	supported by the compiler.
	"""


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
	ast.LShift: op.lshift,
	ast.RShift: op.rshift,
}

def eval_expr(expr):
	return eval_(ast.parse(expr, mode='eval').body)

def eval_(node):
	if isinstance(node, ast.Num): # <number>
		return node.n
	elif isinstance(node, ast.BinOp): # <left> <operator> <right>
		return operators[type(node.op)](eval_(node.left), eval_(node.right))
	elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
		return operators[type(node.op)](eval_(node.operand))
	else:
		raise TypeError(node)

def power(a, b):
	if any(abs(n) > 100 for n in [a, b]):
		raise ValueError((a,b))
	return op.pow(a, b)

operators[ast.Pow] = power
