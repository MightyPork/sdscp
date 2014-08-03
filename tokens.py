#!/bin/env python3

import re
from readers import CodeReader
from enum import Enum


class Token:
	def __init__(self, value):
		self.value = value.strip()
		self.tokens = None

	def is_composite(self):
		return False

	def get_value(self):
		return self.value

	def tokenize(self):
		if not self.is_composite():
			raise Exception('Cannot tokenize atomic token.')

		if self.tokens != None:
			return self.tokens

		self.tokens = []
		self.do_tokenize()

		return self.tokens

	def do_tokenize(self):
		raise Exception('STUB')

	def __str__(self):
		return type(self).__name__ + '  ' + re.sub(r'\s+', ' ', self.value)


class CompositeToken(Token):
	""" Token that has sub-tokens and needs to be further tokenized """

	def is_composite(self):
		return True


class T_Identifier(Token): pass


class T_Expression(CompositeToken):

	def do_tokenize(self):
		rd = CodeReader(self.value)

		t = None

		while not rd.has_end():
			rd.consume_non_code()

			if rd.has_identifier():
				s = rd.consume_identifier()
				t = T_Identifier(s)
				self.tokens.append(t)
				continue

			if rd.has_number():
				s = rd.consume_number()
				t = T_Number(s)
				self.tokens.append(t)
				continue

			if rd.has_paren():
				is_expr = not isinstance(t, T_Identifier)
				s = rd.consume_block()
				t = T_Paren(s)

				if is_expr:
					t.set_type(ParenType.EXPR)
				else:
					t.set_type(ParenType.ARGS)

				self.tokens.append(t)
				continue

			if rd.has_bracket():
				s = rd.consume_block()
				t = T_Bracket(s)
				self.tokens.append(t)
				continue

			if rd.has_operator():
				s = rd.consume_operator()
				t = T_Operator(s)
				self.tokens.append(t)
				continue

			if rd.has_char():
				s = rd.consume_char()
				t = T_Char(s)
				self.tokens.append(t)
				continue

			if rd.has_string():
				s = rd.consume_string()
				t = T_String(s)
				self.tokens.append(t)
				continue

			raise Exception('Unexpected token near' + rd.peek(10))



class T_Number(Token): pass


class T_Operator(Token): pass


class T_Label(Token): pass


class T_AssignmentOperator(Token): pass


class T_Rvalue(CompositeToken):

	def do_tokenize(self):
		rd = CodeReader( self.value )

		s = rd.consume_until(end='=')
		t = T_AssignmentOperator(s)
		self.tokens.append(t)

		s = rd.consume_all()
		t = T_Expression(s)
		self.tokens.append(t)


class ParenType(Enum):
	UNKNOWN = 0
	EXPR = 1
	FOR = 2
	ARGS = 3


class T_Paren(CompositeToken):

	def __init__(self, value):
		super().__init__(value)

		self.type = ParenType.UNKNOWN


	def set_type(self, type):
		self.type = type


	def do_tokenize(self):

		if self.type == None:
			pass # Cannot parse without context

		rd = CodeReader( self.value[1:-1].strip() )

		if self.type == ParenType.EXPR:
			# single expression

			rd.consume_non_code()
			if rd.has_end():
				rd.error('Unexpected end of string')

			s = rd.consume_all()
			t = T_Expression(s)
			self.tokens.append(t)

		elif self.type == ParenType.ARGS:
			# comma-separated list of expressions, can be empty

			while not rd.has_end():

				rd.consume_non_code()
				if rd.has_end():
					break # end of args after some junk

				s = rd.consume_code(end=',', eof=True, keep_end=False)
				t = T_Expression(s)
				self.tokens.append(t)

		elif self.type == ParenType.FOR:
			# arguments for a FOR loop

			self.for_init = None
			self.for_cond = None
			self.for_iter = None

			# init statement
			s = rd.consume_code(end=';', eof=False, keep_end=True)

			tt = Tokenizer(s)
			self.for_init = tt.tokenize()

			# condition
			s = rd.consume_code(end=';', eof=False, keep_end=False)
			self.for_cond = T_Expression(s)

			# iter statement
			s = rd.consume_code(end=';', eof=True, keep_end=False) + ';'

			tt = Tokenizer(s)
			self.for_iter = tt.tokenize()


	def __str__(self):
		return type(self).__name__ + ': Type = ' + str(self.type) + ', ' + self.value



class T_Bracket(CompositeToken):
	def __init__(self, value):
		super().__init__(value)

	def do_tokenize(self):
		rd = CodeReader( self.value[1:-1].strip() )

		rd.consume_non_code()

		s = rd.consume_code(end=',', eof=True, keep_end=False)
		t = T_Expression(s)
		self.tokens.append(t)

		rd.consume_non_code()

		if not rd.has_end():
			raise Exception('Invalid array index (must be single expression).')


class T_CodeBlock(CompositeToken):
	def __init__(self, value):
		super().__init__(value)

	def do_tokenize(self):
		rd = Tokenizer( self.value[1:-1] )
		self.tokens = rd.tokenize()


class T_String(Token): pass


class T_Char(Token): pass


class T_StatementEnd(Token): pass



class Tokenizer:
	""" Source tokenizer
	 - checks for obvious errors
	 - removes comments
	 - creates a token list
	"""

	def __init__(self, source, filename=None):

		self.filename = filename
		self.source = source
		self.tokens = None

	def tokenize(self):

		if self.tokens != None:
			return self.tokens

		self.tokens = []

		rd = CodeReader(self.source, self.filename)

		while not rd.has_end():

			# discard garbage
			rd.consume_non_code()

			# End of string.
			if rd.has_end():
				break


			# label:
			elif rd.has_label():

				s = rd.consume_label()
				t = T_Label(s)
				self.tokens.append(t)


			# <identifier>
			elif rd.has_identifier():

				s = rd.consume_identifier()
				t = T_Identifier(s)
				self.tokens.append(t)


			# = rvalue;
			elif rd.has_rvalue():

				s = rd.consume_rvalue()
				t = T_Rvalue(s)
				self.tokens.append(t)


			# (arg, list)
			elif rd.has_paren():

				s = rd.consume_block()
				t = T_Paren(s)
				self.tokens.append(t)


			# [asf + 16]
			elif rd.has_bracket():

				s = rd.consume_block()
				t = T_Bracket(s)
				self.tokens.append(t)


			# {...stuff...}
			elif rd.has_code_block():

				s = rd.consume_block()
				t = T_CodeBlock(s)
				self.tokens.append(t)


			# "string"
			elif rd.has_string():

				s = rd.consume_string()
				t = T_String(s)
				self.tokens.append(t)


			# 'c'
			elif rd.has_char():

				s = rd.consume_char()
				t = T_Char(s)
				self.tokens.append(t)


			# some statement
			else:
				s = rd.consume_code()
				t = T_StatementEnd(s)
				self.tokens.append(t)


		return self.tokens


	def show(self):
		""" Print tokens to console """

		if self.tokens == None:
			raise Esception('Not parsed yet.')

		_show_tokenlist(self.tokens)



def _show_tokenlist(tokens, level='\t'):
	for tok in tokens:

		print(level + str(tok))

		if tok.is_composite():
			_show_tokenlist(tok.tokenize(), level+'\t')





class TokenWalker:
	""" Utility for walking a token list """

	def __init__(self, tokens):
		self.tokens = tokens
		self.cursor = 0



	def has_next(self):
		""" Get if the walker has more tokens to walk """
		return self.cursor < self.tokens.length



	def has_prev(self):
		""" Get if the walker is not at the beginning """
		return self.cursor > 0



	def peek(self, offset=1):
		""" Peek at the n-th token relative to cursor """

		i = self.cursor + offset

		if not i in range(0, len(self.tokens)):
			raise Exception('Index out of range: %d' % i)

		return self.tokens[i]



	def has(self, clazz, offset=1):
		""" Get if the next (or offset) token is of given type """

		return isinstance(self.peek(offset), clazz)



	def discard(self, count=1):
		""" Discard tokens at current position """

		# after removing one the list shifts back
		# - keep removing the same index
		for i in range(0, count):
			del self.tokens[self.pos]



	def move(self, steps=1):
		""" Move the cursor """

		self.pos += steps


	def descend(self):
		""" Get a TokenWalker for sub-tokens of the current token """

		t = self.peek()
		if not t.is_composite():
			raise Exception('Cannot descend into atomic token!')

		return TokenWalker( t.tokenize() )




