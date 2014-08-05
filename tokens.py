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


class T_RETURN(TokenKeyword):
	""" The RETURN keyword """


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
	""" An expression """

	def do_tokenize(self):
		""" Parse expression sub-tokens """

		rd = CodeReader(self.value)

		while not rd.has_end():
			rd.sweep()

			if rd.has_identifier():
				# an identifier
				# can be variable or a function call

				s = rd.consume_identifier()
				t = T_Name(s)
				self.tokens.append(t)

				rd.sweep()

				if rd.has_bracket():
					# array index
					s = rd.consume_block()
					t = T_Bracket(s)
					self.tokens.append(t)

				elif rd.has_paren():
					# paren with arguments for the function
					s = rd.consume_block()
					t = T_Paren(s)

					t.set_type(ParenType.ARGVALS)

					self.tokens.append(t)



			elif rd.has_paren():
				# Parenthesised sub-expression
				s = rd.consume_block()
				t = T_Paren(s)
				t.set_type(ParenType.EXPR)
				self.tokens.append(t)


			elif rd.has_number():
				# Number literal
				s = rd.consume_number()
				t = T_Number(s)
				self.tokens.append(t)


			elif rd.has_operator():
				# Operator
				s = rd.consume_operator()
				t = T_Operator(s)
				self.tokens.append(t)


			elif rd.has_char():
				# Char literal
				s = rd.consume_char()
				t = T_Char(s)
				self.tokens.append(t)


			elif rd.has_string():
				# String literal
				s = rd.consume_string()
				t = T_String(s)
				self.tokens.append(t)

			else:
				raise Exception('Unexpected expression token near' + rd.peek(10))



class T_Rvalue(CompositeToken):
	""" A right-hand-side of an assignment
	including the assignment operator as the first sub-token
	"""

	def do_tokenize(self):
		rd = CodeReader( self.value )

		s = rd.consume_until(end='=')
		t = T_AssignOperator(s)
		self.tokens.append(t)

		s = rd.consume_all()
		t = T_Expression(s)
		self.tokens.append(t)



class ParenType(Enum):
	""" Kind of parenthesis (parsing method) """
	UNKNOWN = 0
	EXPR = 1
	FOR = 2
	ARGVALS = 3
	ARGNAMES = 4



class T_Paren(CompositeToken):
	""" Parenthesised block """

	def __init__(self, value):
		super().__init__(value)

		self.type = ParenType.UNKNOWN



	def set_type(self, type):
		self.type = type



	def __collect_expr(self, rd):
		""" parse as single expression """

		rd.sweep()
		if rd.has_end():
			rd.error('Unexpected end of string (expected expression)')

		s = rd.consume_all()
		t = T_Expression(s)
		self.tokens.append(t)



	def __collect_argvals(self, rd):
		""" parse as function call argument list """

		while not rd.has_end():

			rd.sweep()
			if rd.has_end():
				break # end of args after some junk

			s = rd.consume_code(end=',', eof=True, keep_end=False)
			t = T_Expression(s)
			self.tokens.append(t)



	def __collect_argnames(self, rd):
		""" parse as argument name list """

		while not rd.has_end():

			rd.sweep()
			if rd.has_end():
				break # end of args after some junk

			s = rd.consume_identifier()
			t = T_Name(s)
			self.tokens.append(t)



	def __collect_for(self, rd):
		""" parse as for loop paren """

		# init statement
		s = rd.consume_code(end=';', eof=False, keep_end=True).strip()

		tt = Tokenizer(s)
		self.for_init = tt.tokenize() # tokenlist
		self.for_init_s = s

		# condition
		s = rd.consume_code(end=';', eof=False, keep_end=False).strip()
		if len(s) == 0:
			self.for_cond = T_Expression('1') # true
			self.for_cond_s = '1'
		else:
			self.for_cond = T_Expression(s) # one expression token
			self.for_cond_s = s

		# iter statement
		s = rd.consume_code(end=';', eof=True, keep_end=False).strip() + ';'
		tt = Tokenizer(s)
		self.for_iter = tt.tokenize() # tokenlist
		self.for_iter_s = s



	def do_tokenize(self):

		if self.type == None:
			print('Paren has no type, cannot tokenize: ' + str(self))
			pass # Cannot parse without context

		rd = CodeReader( self.value[1:-1].strip() )

		if self.type == ParenType.EXPR:
			# single expression
			self.__collect_expr(rd)


		elif self.type == ParenType.ARGVALS:
			# comma-separated list of expressions, can be empty
			self.__collect_argvals(rd)


		elif self.type == ParenType.ARGNAMES:
			# comma-separated list of argument names
			self.__collect_argnames(rd)


		elif self.type == ParenType.FOR:
			# arguments for a FOR loop
			self.__collect_for(rd)


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
	""" Square bracket """

	def __init__(self, value):
		super().__init__(value)


	def do_tokenize(self):
		rd = CodeReader( self.value[1:-1].strip() )

		rd.sweep()

		s = rd.consume_code(end=',', eof=True, keep_end=False)
		t = T_Expression(s)
		self.tokens.append(t)

		rd.sweep()

		if not rd.has_end():
			raise Exception('Invalid array index (must be single expression).')


	def __str__(self):
		return type(self).__name__ + ' [...]'



class T_CodeBlock(CompositeToken):
	""" Braced code block """

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
		""" Convert to tokens, get token list """

		if self.tokens != None:
			return self.tokens

		self.tokens = []

		rd = CodeReader(self.source, self.filename)

		while not rd.has_end():

			# discard garbage
			rd.sweep()

			# End of string.
			if rd.has_end():
				break

			# <identifier>
			elif rd.has_identifier():

				self.__tokenize_identifier(rd)


			# {...stuff...}
			elif rd.has_code_block():

				s = rd.consume_block()
				self.tokens.append( T_CodeBlock(s) )


			# ;
			elif rd.starts(';'):

				self.__collect_semicolon(rd)


			else:
				rd.error('Unexpected syntax here.')


		return self.tokens


	def __collect_assign_stmt(self, rd):
		""" Collect a varname = value statement from reader and add as tokens """
		rd.sweep()

		s = rd.consume_identifier()
		tok = T_Name(s)
		self.tokens.append(tok)

		rd.sweep()

		# array index bracket
		if rd.has_bracket():
			s = rd.consume_block()
			self.tokens.append(T_Bracket(s))
			rd.sweep()


		if rd.starts('++') or rd.starts('--') :
			sign = rd.consume()
			rd.consume() # discard the second
			self.tokens.append( T_Rvalue( "%s=1" % sign ) )
		elif rd.has_rvalue():
			self.tokens.append( T_Rvalue( rd.consume_rvalue() ) )
		else:
			rd.error('Unexpected syntax.')


	def __collect_semicolon(self, rd):
		rd.sweep()

		rd.consume_exact(';')
		self.tokens.append( T_Semicolon() )


	def __collect_colon(self, rd):
		rd.sweep()

		rd.consume_exact(':')
		self.tokens.append( T_Colon() )


	def __collect_label(self, rd):
		rd.sweep()

		lbl = rd.consume_identifier()
		self.tokens.append( T_LABEL() )
		self.tokens.append( T_Name(lbl) )

		rd.sweep()
		rd.consume_exact(':')
		self.tokens.append( T_Colon() )


	def __collect_paren(self, rd, paren_type):
		rd.sweep()

		if not rd.has_paren():
			rd.error('Expected parenthesis.')

		paren = rd.consume_block()

		t = T_Paren(paren)
		t.set_type(paren_type)
		self.tokens.append(t)


	def __tokenize_identifier(self, rd):
		rd.sweep()

		pos_before_s = rd.get_pos()

		s = rd.consume_identifier()

		rd.sweep()

		kwd = s.lower()

		# handle keywords first

		# if-elseif-else
		if kwd == 'if':
			self.tokens.append( T_IF() )
			self.__collect_paren(rd, ParenType.EXPR)


		elif kwd == 'else':
			self.tokens.append( T_ELSE() )


		elif kwd == 'elseif':
			self.tokens.append( T_ELSE() )
			self.tokens.append( T_IF() )
			self.__collect_paren(rd, ParenType.EXPR)



		# the various loops
		elif kwd == 'while':
			self.tokens.append( T_WHILE() )
			self.__collect_paren(rd, ParenType.EXPR)


		elif kwd == 'until':
			self.tokens.append( T_UNTIL() )
			self.__collect_paren(rd, ParenType.EXPR)


		elif kwd == 'for':
			self.tokens.append( T_FOR() )
			self.__collect_paren(rd, ParenType.FOR)


		elif kwd == 'do':
			self.tokens.append( T_DO() )


		elif kwd == 'continue':
			self.tokens.append( T_CONTINUE() )


		elif kwd == 'break':
			self.tokens.append( T_BREAK() )

		# the switch statemnt
		elif kwd == 'switch':
			self.tokens.append( T_SWITCH() )
			self.__collect_paren(rd, ParenType.EXPR)


		elif kwd == 'case':
			self.tokens.append( T_CASE() )

			expr = rd.consume_code(end=':', consume_end=False)
			t = T_Expression(expr)
			self.tokens.append(t)

			self.__collect_colon(rd)


		elif kwd == 'default':
			self.tokens.append( T_DEFAULT() )

			self.__collect_colon(rd)



		elif kwd == 'var':

			while True:
				self.tokens.append( T_VAR() )
				rd.sweep()

				#varname
				name = rd.consume_identifier()
				self.tokens.append( T_Name(name) )

				rd.sweep()

				# initial value assignment
				if rd.has_rvalue():
					v = rd.consume_rvalue()
					self.tokens.append( T_Rvalue(v) )

				rd.sweep()

				# whats next?
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



		elif kwd == 'goto':
			self.tokens.append( T_GOTO() )

			lbl = rd.consume_identifier()
			t = T_Name(lbl)
			self.tokens.append(t)

			self.__collect_semicolon(rd)


		elif kwd == 'label':
			# the label keyword (optional for labels)
			rd.move_to(pos_before_s) # backtrack
			self.__collect_label(rd)


		elif kwd == 'return':
			self.tokens.append( T_RETURN() )

			if not rd.starts(';'):
				# return with no value
				expr = rd.consume_code(end=';', consume_end=False)
				t = T_Expression(expr)
				self.tokens.append(t)

			# the semicolon
			self.__collect_semicolon(rd)


		elif rd.has_paren():
			# function call or declaration

			paren = rd.consume_block() # consume the paren

			rd.sweep()

			if rd.starts(';'):
				# a call
				self.tokens.append( T_CALL() )
				self.tokens.append( T_Name(s) )

				t = T_Paren(paren)
				t.set_type(ParenType.ARGVALS)
				self.tokens.append(t)

				self.__collect_semicolon(rd)


			elif rd.has_code_block():
				# a declaration
				self.tokens.append( T_FUNCTION() )
				self.tokens.append( T_Name(s) )

				t = T_Paren(paren)
				t.set_type(ParenType.ARGNAMES)
				self.tokens.append(t)

				rd.sweep()

				cbl = rd.consume_block()
				self.tokens.append( T_CodeBlock(cbl) )


		elif rd.has_bracket() or rd.has_rvalue() or rd.starts('++') or rd.starts('--'):

			# foo = bar, other = baz;
			self.tokens.append( T_SET() )

			rd.move_to(pos_before_s) # rewind

			self.__collect_assign_stmt(rd)

			rd.sweep()

			if rd.starts(';'):
				self.__collect_semicolon(rd)

			elif rd.starts(','):
				rd.consume() # the comma

				while True:
					rd.sweep()

					if rd.has_identifier():

						self.tokens.append( T_Semicolon() ) # start new statement
						self.tokens.append( T_SET() )

						self.__collect_assign_stmt(rd)

					else:
						rd.error('Missing identifier.')

					rd.sweep()

					if rd.starts(','):
						rd.consume()
						continue

					elif rd.starts(';'):
						self.__collect_semicolon(rd)
						break

					else:
						rd.error('Expected , or ; here.')


		else:
			# just a name
			rd.sweep()

			if rd.starts(':'):
				# was a label without "label" keyword

				rd.move_to(pos_before_s)

				self.__collect_label(rd)

				return

			# unknown meaning
			rd.error("Unexpected syntax: Don't know what %s means here." % s)



	def show(self):
		""" Print tokens to console """

		if self.tokens == None:
			raise Esception('Not parsed yet.')

		show_tokenlist(self.tokens)



def show_tokenlist(tokens, level='  '):
	""" Show a token list """
	if len(tokens) == 0:
		print(level + '-empty-')

	else:
		for tok in tokens:

			print(level + str(tok))

			if tok.is_composite():
				show_tokenlist(tok.tokenize(), level+'  ')





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


	def move(self, steps=1):
		""" Move the cursor """

		self.pos += steps
