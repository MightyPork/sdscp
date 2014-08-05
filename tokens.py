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


	# def __str__(self):
	# 	return type(self).__name__

	def __str__(self):
		self.tokenize()
		return '%s{ %s }' % (
				type(self).__name__,
				', '.join([str(a) for a in (self.tokens or [])])
		)

# --- keywords ---

class TokenKeyword(Token):
	""" A token representing a keyword """

	def __init__(self):
		super().__init__( type(self).__name__[2:].lower() )

	def __str__(self):
		return type(self).__name__


class T_IF(TokenKeyword):
	""" The IF keyword """


class T_ELSE(TokenKeyword):
	""" The ELSE keyword (in if) """


class T_FOR(TokenKeyword):
	""" The FOR keyword """


class T_WHILE(TokenKeyword):
	""" The WHILE keyword """


class T_UNTIL(TokenKeyword):
	""" The DEFAULT keyword (while not) """


class T_SWITCH(TokenKeyword):
	""" The SWITCH keyword """


class T_CASE(TokenKeyword):
	""" The CASE keyword (in switch) """


class T_DEFAULT(TokenKeyword):
	""" The DEFAULT keyword (in switch) """


class T_DO(TokenKeyword):
	""" The DO keyword (loop with condition at the end) """


class T_VAR(TokenKeyword):
	""" The VAR keyword """


class T_GOTO(TokenKeyword):
	""" The GOTO keyword """


class T_BREAK(TokenKeyword):
	""" The BREAK keyword """


class T_CONTINUE(TokenKeyword):
	""" The CONTINUE keyword """


class T_CONTINUE(TokenKeyword):
	""" The CONTINUE keyword """


class T_SET(TokenKeyword):
	""" The SET keyword (synthetic, for var assignment) """


class T_LABEL(TokenKeyword):
	""" The LABEL keyword (synthetic, for labels) """


class T_CALL(TokenKeyword):
	""" The CALL keyword (synthetic, for call without assigning retval) """


class T_FUNCTION(TokenKeyword):
	""" The FUNCTION keyword (synthetic, for function/routine declaration) """


# --- end of keywords ---


class T_Name(Token):
	""" Any identifier not recognized as a keyword """


class TokenSymbol(Token):
	""" A token representing a symbol """

	def __init__(self):
		super().__init__('')

	def __str__(self):
		return type(self).__name__


class T_Comma(TokenSymbol):
	""" , """


class T_Semicolon(TokenSymbol):
	""" ; """


class T_Colon(TokenSymbol):
	""" : """


class T_Increment(TokenSymbol):
	""" ++ """


class T_Decrement(TokenSymbol):
	""" -- """


class T_String(Token):
	""" String literal """


class T_Char(Token):
	""" Char literal """


class T_Number(Token):
	""" Dec, hex or bin number literal """


class T_Operator(Token):
	""" Any operator in an expression """


class T_AssignOperator(Token):
	""" Assignment operator at the beginning of a Rvalue """


class T_Expression(CompositeToken):

	def do_tokenize(self):
		rd = CodeReader(self.value)

		while not rd.has_end():
			rd.consume_non_code()

			if rd.has_identifier():
				s = rd.consume_identifier()
				t = T_Name(s)
				self.tokens.append(t)

				rd.consume_non_code()

				if rd.has_bracket():
					s = rd.consume_block()
					t = T_Bracket(s)
					self.tokens.append(t)

				elif rd.has_paren():

					s = rd.consume_block()
					t = T_Paren(s)

					t.set_type(ParenType.ARGVALS)

					self.tokens.append(t)

				continue

			if rd.has_paren():

				s = rd.consume_block()
				t = T_Paren(s)
				t.set_type(ParenType.EXPR)
				self.tokens.append(t)
				continue

			if rd.has_number():
				s = rd.consume_number()
				t = T_Number(s)
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



class T_Rvalue(CompositeToken):

	def do_tokenize(self):
		rd = CodeReader( self.value )

		s = rd.consume_until(end='=')
		t = T_AssignOperator(s)
		self.tokens.append(t)

		s = rd.consume_all()
		t = T_Expression(s)
		self.tokens.append(t)


class ParenType(Enum):
	UNKNOWN = 0
	EXPR = 1
	FOR = 2
	ARGVALS = 3
	ARGNAMES = 4


class T_Paren(CompositeToken):

	def __init__(self, value):
		super().__init__(value)

		self.type = ParenType.UNKNOWN


	def set_type(self, type):
		self.type = type


	def do_tokenize(self):

		if self.type == None:
			print('Paren has no type, cannot tokenize: ' + str(self))
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

		elif self.type == ParenType.ARGVALS:
			# comma-separated list of expressions, can be empty

			while not rd.has_end():

				rd.consume_non_code()
				if rd.has_end():
					break # end of args after some junk

				s = rd.consume_code(end=',', eof=True, keep_end=False)
				t = T_Expression(s)
				self.tokens.append(t)

		elif self.type == ParenType.ARGNAMES:
			# comma-separated list of argument names

			while not rd.has_end():

				rd.consume_non_code()
				if rd.has_end():
					break # end of args after some junk

				s = rd.consume_identifier()
				t = T_Name(s)
				self.tokens.append(t)


		elif self.type == ParenType.FOR:
			# arguments for a FOR loop

			# init statement
			s = rd.consume_code(end=';', eof=False, keep_end=True)

			tt = Tokenizer(s)
			self.for_init = tt.tokenize() # tokenlist
			self.for_init_s = s

			# condition
			s = rd.consume_code(end=';', eof=False, keep_end=False)
			self.for_cond = T_Expression(s) # one expression token
			self.for_cond_s = s

			# iter statement
			s = rd.consume_code(end=';', eof=True, keep_end=False) + ';'
			tt = Tokenizer(s)
			self.for_iter = tt.tokenize() # tokenlist
			self.for_iter_s = s


	def __str__(self):

		s = type(self).__name__ + ' (...) : ' + str(self.type.name)

		if self.type == ParenType.UNKNOWN:
			s += ', Content: ' + self.value

		elif self.type == ParenType.FOR:
			self.tokenize()
			s += ' (INIT %s  | COND %s  | ITER %s )' % (self.for_init_s, self.for_cond_s, self.for_iter_s)
			s += '\n - INIT {%s}\n - COND {%s}\n - ITER {%s} )' % (
				', '.join([str(a) for a in self.for_init]),
				str(self.for_cond),
				', '.join([str(a) for a in self.for_iter])
			)

		return s



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

	def __str__(self):
		return type(self).__name__ + ' [...]'


class T_CodeBlock(CompositeToken):
	def __init__(self, value):
		super().__init__(value)

	def do_tokenize(self):
		rd = Tokenizer( self.value[1:-1] )
		self.tokens = rd.tokenize()

	def __str__(self):
		return type(self).__name__ + ' {...}'


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

			# <identifier>
			elif rd.has_identifier():

				s = rd.consume_identifier()
				rd.consume_non_code() # whitespace perhaps

				kwd = s.lower()

				# handle keywords first


				if kwd == 'case':
					self.tokens.append( T_CASE() )

					expr = rd.consume_code(end=':', consume_end=False)
					t = T_Expression(expr)
					self.tokens.append(t)

					rd.assert_starts(':')

					continue


				elif kwd == 'default':
					self.tokens.append( T_DEFAULT() )

					rd.assert_starts(':') # consumed next iteration
					continue


				elif kwd == 'if':
					self.tokens.append( T_IF() )

					if not rd.has_paren():
						rd.error('Expected parenthesis with IF condition.')

					paren = rd.consume_block()

					t = T_Paren(paren)
					t.set_type(ParenType.EXPR)
					self.tokens.append(t)

					continue


				elif kwd == 'while':
					self.tokens.append( T_WHILE() )

					if not rd.has_paren():
						rd.error('Expected parenthesis with WHILE condition.')

					paren = rd.consume_block()

					t = T_Paren(paren)
					t.set_type(ParenType.EXPR)
					self.tokens.append(t)

					continue


				elif kwd == 'until':
					self.tokens.append( T_UNTIL() )

					if not rd.has_paren():
						rd.error('Expected parenthesis with UNTIL condition.')

					paren = rd.consume_block()

					t = T_Paren(paren)
					t.set_type(ParenType.EXPR)
					self.tokens.append(t)

					continue


				elif kwd == 'for':
					self.tokens.append( T_FOR() )

					if not rd.has_paren():
						rd.error('Expected parenthesis with FOR (init; cond; iter).')

					paren = rd.consume_block()

					t = T_Paren(paren)
					t.set_type(ParenType.FOR)
					self.tokens.append(t)

					continue


				elif kwd == 'switch':
					self.tokens.append( T_SWITCH() )

					if not rd.has_paren():
						rd.error('Expected parenthesis with SWITCH condition.')

					paren = rd.consume_block()

					t = T_Paren(paren)
					t.set_type(ParenType.EXPR)
					self.tokens.append(t)

					continue


				elif kwd == 'else':
					self.tokens.append( T_ELSE() )
					continue


				elif kwd == 'var':

					while True:
						self.tokens.append( T_VAR() )
						rd.consume_non_code() # whitespace

						name = rd.consume_identifier()
						self.tokens.append( T_Name(name) )

						rd.consume_non_code() # whitespace

						if rd.has_rvalue():
							v = rd.consume_rvalue()
							self.tokens.append( T_Rvalue(v) )

						rd.consume_non_code() # whitespace

						if rd.starts(','):
							# more vars

							rd.consume() # the comma

							self.tokens.append( T_Semicolon() ) # start new statement

							continue # to next var name

						elif rd.starts(';'):
							# end of it
							rd.consume() # the sc
							self.tokens.append( T_Semicolon() )
							break # to next statement

						else:
							rd.error('Expected , or ; here.')

					continue


				elif kwd == 'break':
					self.tokens.append( T_BREAK() )

					continue


				elif kwd == 'do':
					self.tokens.append( T_DO() )

					continue


				elif kwd == 'continue':
					self.tokens.append( T_CONTINUE() )

					continue


				elif kwd == 'label':
					# the label keyword (optional for labels)
					self.tokens.append( T_LABEL() )
					continue


				elif kwd == 'goto':
					self.tokens.append( T_GOTO() )

					lbl = rd.consume_identifier()
					t = T_Name(lbl)
					self.tokens.append(t)

					rd.consume_non_code()
					rd.assert_starts(';')


					if rd.starts(';'):
						# return with no value
						continue

					expr = rd.consume_code(end=';', consume_end=False)
					t = T_Expression(expr)
					self.tokens.append(t)

					rd.assert_starts(';') # consumed next iteration
					continue


				elif kwd == 'return':
					self.tokens.append( T_RETURN() )

					if rd.starts(';'):
						# return with no value
						continue

					expr = rd.consume_code(end=';', consume_end=False)
					t = T_Expression(expr)
					self.tokens.append(t)

					rd.assert_starts(';') # consumed next iteration
					continue

				elif rd.has_paren():
					# function call or declaration

					paren = rd.consume_block() # consume the paren

					rd.consume_non_code() # whitespace

					if rd.starts(';'): # was a call
						self.tokens.append( T_CALL() )
						self.tokens.append( T_Name(s) )
						t = T_Paren(paren)
						t.set_type(ParenType.ARGVALS)
						self.tokens.append(t)

					elif rd.has_code_block(): # was a declaration most likely
						self.tokens.append( T_FUNCTION() )
						self.tokens.append( T_Name(s) )
						t = T_Paren(paren)
						t.set_type(ParenType.ARGNAMES)
						self.tokens.append(t)

					continue

				elif rd.has_bracket():
					# moo[foo] = bar;
					self.tokens.append( T_SET() )
					self.tokens.append( T_Name( s ) )

					bracket = rd.consume_block() # consume the bracket
					self.tokens.append( T_Bracket( bracket ) )

					rd.consume_non_code() # whitespace

					if not rd.has_rvalue():
						rd.error('Expected assignment.')

					self.tokens.append( T_Rvalue( rd.consume_rvalue() ) )

					rd.consume_non_code() # whitespace

					rd.consume_exact(';');

					continue

				elif rd.has_rvalue():
					# foo = bar, other = baz;
					self.tokens.append( T_SET() )
					self.tokens.append( T_Name( s ) )
					self.tokens.append( T_Rvalue( rd.consume_rvalue() ) )

					if rd.starts(';'):
						continue

					elif rd.starts(','):
						rd.consume() # the comma

						while True:
							rd.consume_non_code() # whitespace

							if rd.has_identifier():
								self.tokens.append( T_Semicolon() ) # start new statement
								self.tokens.append( T_SET() )
								self.tokens.append( T_Name( rd.consume_identifier() ) )
								rd.consume_non_code() # whitespace

								self.tokens.append( T_Rvalue( rd.consume_rvalue() ) )
							else:
								rd.error('Missing identifier.')

							rd.consume_non_code() # whitespace

							if rd.starts(','):
								continue
							elif rd.starts(';'):
								break
							else:
								rd.error('Expected , or ; here.')


				elif rd.starts('++'):
					rd.consume_exact('++')

					self.tokens.append( T_SET() )
					self.tokens.append( T_Name(s) )
					self.tokens.append( T_Rvalue('+= 1') )


				elif rd.starts('--'):
					rd.consume_exact('--')

					self.tokens.append( T_SET() )
					self.tokens.append( T_Name(s) )
					self.tokens.append( T_Rvalue('-= 1') )


				else:
					# just a name
					rd.consume_non_code() # whitespace

					if rd.starts(':'):
						# was a label
						self.tokens.append( T_LABEL() )
						self.tokens.append( T_Name(s) )

						rd.consume()
						self.tokens.append( T_Colon() )


						continue

					# unknown meaning
					rd.error("Unexpected syntax: Don't know what %s means here." % s)


			# = rvalue;
			elif rd.has_rvalue():

				s = rd.consume_rvalue()
				self.tokens.append( T_Rvalue(s) )


			# (arg, list)
			elif rd.has_paren():

				s = rd.consume_block()
				self.tokens.append( T_Paren(s) )


			# [asf + 16]
			elif rd.has_bracket():

				s = rd.consume_block()
				self.tokens.append( T_Bracket(s) )


			# {...stuff...}
			elif rd.has_code_block():

				s = rd.consume_block()
				self.tokens.append( T_CodeBlock(s) )

			# "string"
			elif rd.has_string():

				s = rd.consume_string()
				self.tokens.append( T_String(s) )


			# 123
			elif rd.has_number():

				s = rd.consume_number()
				self.tokens.append( T_Number(s) )


			# 'c'
			elif rd.has_char():

				s = rd.consume_char()
				self.tokens.append( T_Char(s) )


			# , (eg. var foo, bar;)
			elif rd.starts(','):

				rd.consume()
				self.tokens.append( T_Comma() )


			# ;
			elif rd.starts(';'):
				rd.consume()
				self.tokens.append( T_Semicolon() )


			# :
			elif rd.starts(':'):
				rd.consume()
				self.tokens.append( T_Colon() )


			# ++
			elif rd.starts('++'):
				rd.consume_exact('++')
				self.tokens.append( T_Increment() )


			# --
			elif rd.starts('--'):
				rd.consume_exact('--')
				self.tokens.append( T_Decrement() )


			else:
				rd.error('Unexpected syntax here.')


		return self.tokens


	def show(self):
		""" Print tokens to console """

		if self.tokens == None:
			raise Esception('Not parsed yet.')

		_show_tokenlist(self.tokens)



def _show_tokenlist(tokens, level='  '):
	if len(tokens) == 0:
		print(level + '-empty-')

	else:
		for tok in tokens:

			print(level + str(tok))

			if tok.is_composite():
				_show_tokenlist(tok.tokenize(), level+'  ')





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




