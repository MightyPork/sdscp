#!/bin/env python3

import re

from tokens import *


class Statement:
	""" A semantic node

	a code piece that makes sense on it's own
	"""

	def __str__(self):
		return type(self).__name__


def S_Empty(Statement):
	""" An empty statement (nop) """

	def __init__(self, tw):
		tw.consume(T_Semicolon)


def S_Function(Statement):
	""" A function statement """

	def __init__(self, tw):

		# instance variables
		self.args = []
		self.body = None

		# keyword
		tw.consume(T_FUNCTION)

		paren = tw.consume(T_Paren)
		if not paren.type == ParenType.ARGNAMES:
			raise SyntaxError(
				'Expected ARGNAMES paren, got %s'
				% paren.type.name
			)

		# argument token walker
		atw = TokenWalker(paren.tokens)

		# collect all argument names
		while atw.has_next():
			if not atw.has(T_Name):
				raise SyntaxError(
					'Expected identifier, not %s'
					% str(atw.peek())
				)

			n = atw.consume()
			argname = n.value.strip()

			self.args.append(argname)

		# get function body
		self.body = S_Block(tw)


def S_Block(Statement):
	""" A code block statement

	A block is a statement, which has it's own
	variable scope and can hold any number of
	child statements. Block is enclosed in curly braces.
	"""

	def _collect(self, tw):

		self.children = []

		# keyword
		cb = tw.consume(T_CodeBlock)

		# code-block token walker
		ctw = TokenWalker(cb.tokens)

		while ctw.has_next():
			st = ctw.collect_statement()

			if not isinstance(st, S_Empty):
				self.children.append(st)


def S_VarDeclaration(Statement):
	""" A variable declaration

	Optionally, can initialize the value; default value is zero.
	A var declaration can declare only one variable at a time -
	use multiple if needed.
	"""






class TokenWalker:
	""" Recognizes nodes in a token list """

	def __init__(self, tokens):

		# initialize instance variables
		self.pos = 0
		self.tokens = tokens


	def has_next(self):
		""" Get if the walker has more tokens to walk """
		return self.pos < self.tokens.length


	def peek(self, offset=1):
		""" Peek at the n-th token relative to cursor """

		i = self.pos + offset

		if not i in range(0, len(self.tokens)):
			raise Exception('Index out of range: %d' % i)

		return self.tokens[i]



	def has(self, cls, offset=1):
		""" Get if the next (or offset) token is of given type """

		return isinstance(self.peek(offset), cls)


	def move(self, steps=1):
		""" Move the cursor """

		self.pos += steps


	def consume(self, cls):
		""" Consume one token, move the cursor.
		Asserts it is of the right type
		"""

		if not self.has(cls):
			raise Exception(
				'Expected ' +
				cls.__name__ +
				', found ' +
				type(self.peek()).__name__
			)

		self.move()


	def rewind(self):
		""" Go to beginning """

		self.pos = 0



