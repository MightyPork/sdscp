#!/bin/env python3

import re
from readers import CodeReader
from enum import Enum


class Token:
	""" A token

	Token is a meaningful code unit, which can be further
	structured (have sub-tokens).

	Token does NOT neccessarily represent a whole statement.

	Args:
		value (str): a piece of the source code the Token is meant
			to represent

	Attributes:
		value (str): the source that generated this token; may be
			cleaned and processed to be more meaninful.

	"""

	def __init__(self, value):
		self.value = value.strip()


	def is_composite(self):
		""" Get if this token is composite (has sub-tokens) """
		return False


	def tokenize(self):
		""" Parse the value string to something meaningful

		For composite tokens, extract the sub-tokens; otherwise,
		this method may extract information from the source string.

		Returns:
			a list of the sub-tokens.

		"""

		if not self.is_composite():
			raise Exception('Cannot tokenize atomic token.')

		if self.tokens is None:
			self.tokens = []
			self._tokenize()

		return self.tokens


	def _tokenize(self):
		""" Perform the actual tokenization.

		The `tokenize()` method already takes care of caching and
		rejecting to tokenize non-composite tokens.

		The tokens should be stored in `self.tokens`

		"""

		raise NotImplementedError()


	def __str__(self):
		""" Get a human readable representation of the token """

		return type(self).__name__ + '  ' + re.sub(r'\s+', ' ', self.value)



class CompositeToken(Token):
	""" Token that has sub-tokens

	Attributes:
		value (str): source, same as Token
		tokens (list of Token): the sub-tokens are stored here.
			Defaults to None.

	"""


	def __init__(self, value):
		super().__init__(value)
		self.tokens = None  # None = not yet tokenized


	def is_composite(self):
		""" Returns true, because this token is composite """

		return True


	def __str__(self):
		# return type(self).__name__
		self.tokenize()
		return '%s{ %s }' % (
			type(self).__name__,
			', '.join([str(a) for a in (self.tokens or [])])
		)


	def _add(self, token):
		""" Add a token to the tokens array """

		self.tokens.append(token)


# --- keywords ---
class TokenKeyword(Token):
	""" A token representing a keyword

	The token class must be called `T_{KEYWORD}`, for the
	`KEYWORD` (turned lowercase) will be used as the value.

	"""

	def __init__(self):
		super().__init__(type(self).__name__[2:].lower())


	def __str__(self):
		return type(self).__name__



class T_IF(TokenKeyword):
	""" The IF keyword

	A IF-THEN-ELSE statement

	If the ELSE branch is missing, an empty statement will be used.

	The "dangling else" problem...

		IF a IF b foo; ELSE bar;

	...is resolved like so:

		IF a {
			IF b {
				foo;
			} ELSE {
				bar;
			}
		}


	Follows:
		T_Paren(EXPR): The branch condition
		<statement>: The TRUE statement
		-optionally-
		T_ELSE:
		<statement>: The FALSE branch

	"""



class T_ELSE(TokenKeyword):
	""" The ELSE keyword

	Starts the FALSE branch of T_IF.

	Follows:
		<statement>: The branch body

	"""



class T_FOR(TokenKeyword):
	""" The FOR keyword

	A for loop.

	Follows:
		T_Paren(FOR): A "for" paren
			- for_init:
				<statement[]>: Statements to be executed
					before the loop first runs
			- for_cond:
				T_Expression: Loop condition; tested before every loop cycle.
			- for_iter:
				<statement[]>: Statements executed at the end of every loop cycle.
		<statement>: The loop body

	"""



class T_WHILE(TokenKeyword):
	""" The WHILE keyword

	A loop that runs while the condition is true.

	Follows:
		T_Paren(EXPR): The loop condition

		- unless used in T_DO -
		<statement>: The loop body

	"""



class T_SWITCH(TokenKeyword):
	""" The SWITCH keyword

	A switch control structure

	Follows:
		T_Paren(EXPR): The expression compared with the cases
		T_CodeBlock: The switch body
			May contain any number of T_CASE, and optionally
			one T_DEFAULT. The T_DEFAULT can be anywhere in the
			switch body.
			A T_BREAK in the body jumps to the end of the switch
			statement.

	"""



class T_CASE(TokenKeyword):
	""" The CASE keyword (in switch)

	Starts a SWITCH branch.

	Unless there is a T_BREAK in the case body, the next branch
	will be executed unconditionally.

	Follows:
		T_Expression: Value for this switch branch
		<statement[]>: Body of the branch

	"""



class T_DEFAULT(TokenKeyword):
	""" The DEFAULT keyword (in switch)

	Starts the default case.

	Follows:
		T_Colon

	"""



class T_DO(TokenKeyword):
	"""
	The DO keyword

	A loop with condition at the end.

	Follows:
		<statement>: Body of the loop
		T_WHILE
		T_Paren(EXPR): The loop condition
		T_Semicolon

	"""



class T_VAR(TokenKeyword):
	""" The VAR keyword

	Create a variable. If the variable already exists, a syntax
	error is raised.

	Follows:
		T_Name: The variable name
		T_Rvalue (optional): Assigning an initial value
			The Rvalue must not use "extended equals" (eg. +=).
			Doing so is a syntax error.
		T_Semicolon

	When a Rvalue is missing, the default value 0 is used instead.

	"""



class T_GOTO(TokenKeyword):
	""" The GOTO keyword

	Jump to a label.

	It is possible to jump only to a label within the same
	function. Still, doing so may cause unexpected behavior.

	It is recommended to avoid GOTO wherever possible, and
	if it cannot be avoided, check the generated code for
	potential errors.

	Follows:
		T_Name: Label to jump to
		T_Semicolon

	"""



class T_BREAK(TokenKeyword):
	"""	The BREAK keyword

	Jump to the end of the closest loop or switch.
	Doing so leaves the loop scope.

	"""



class T_RETURN(TokenKeyword):
	""" The RETURN keyword

	Leaves a function.
	Doing so leaves the function scope, discarding any
	local variables.

	Follows:
		T_Expression (optional): A return value
		T_Semicolon

	If the return value is missing, a default return
	value is used. Whether that is 1 or 0 depends on
	the compiler configuration.

	"""



class T_CONTINUE(TokenKeyword):
	""" The CONTINUE keyword

	Jump to the condition of the enclosing loop.
	(End current cycle)

	"""



class T_SET(TokenKeyword):
	""" The SET keyword

	Indicate the start of a variable assignment statement.
	This token is synthetic.

	Unlike T_VAR, the assigned variable must already be
	defined in the current scope. If it is not, a syntax
	error is raised.

	Follows:
		T_Name: Name of the assigned variable
		T_Rvalue: The assigned value
		T_Semicolon

	"""



class T_LABEL(TokenKeyword):
	""" The LABEL keyword

	Marks a jump target. This token is generated
	if not explicitly used in the source code.

	Follows:
		T_Name: A name of the label
		T_Colon

	"""



class T_CALL(TokenKeyword):
	""" The CALL keyword

	Call a function/routine.
	This token is synthetic.

	This statement is essentially equivalent to "GOSUB", for
	the return value is discarded.

	Follows:
		T_Name: Name of the called function
		T_Paren(ARGVALS): Call parameters
		T_Semicolon

	"""



class T_FUNCTION(TokenKeyword):
	""" The FUNCTION keyword

	Declare a function.
	This token is synthetic.

	A function has a variable scope and a return value.

	To leave the function with a return value, use T_RETURN
	anywhere within the body.

	The function statement must be in the top-level scope.
	Nesting function in any other statement is a syntax error.

	Follows:
		T_Name: Name of the function
		T_Paren(ARGNAMES): The arguments for the function
		T_CodeBlock: The function body

	"""



class T_Name(Token):
	""" Any identifier not recognized as a keyword """

	def equals(self, other):
		""" Check for value equality

		Args:
			other (T_Name): compared name token

		Returns:
			True if they are equal.

		"""

		return self.value == other.value



class T_Semicolon(Token):
	""" Semicolon

	Marks the end of a statement

	"""

	def __init__(self):
		super().__init__(';')



class T_Colon(Token):
	""" Colon

	Marks the end of a CASE, LABEL or DEFAULT.

	"""

	def __init__(self):
		super().__init__(':')



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
	""" An expression

	Contains:
		<tokens>: The expression tokens.

	Possible tokens:
		- T_Operator ... an arithmetic operator
		- T_Name ....... a name (meaning is context sensitive)
		- T_Paren ...... a paren
			EXPR for changing evaluation order
			ARGVALS arguments for a function call (after a name)
		- T_Bracket .... an array index (after a name)
		- T_Char ....... a char literal
		- T_String ..... a string literal
		- T_Number ..... a number literal

	"""

	def _tokenize(self):
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

			elif (((len(self.tokens) > 0 and
				type(self.tokens[-1:][0]) is T_Operator) or len(self.tokens) == 0)
				and rd.matches(r'[-+]\s*[0-9a-z_]+')):

				# Unary operator
				sign = rd.consume()
				if sign == '+':
					sign = ''

				rd.sweep()

				if sign == '-':
					self.tokens.append(T_Operator('@-'))

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

		for t in self.tokens:
			if t.is_composite():
				t.tokenize()



class T_Rvalue(CompositeToken):
	""" A right-hand-side of an assignment

	Contains:
		T_AssignOperator: =, +=, %= etc.
		T_Expression: The assigned value

	"""

	def _tokenize(self):
		rd = CodeReader(self.value)

		s = rd.consume_until(end='=')
		t = T_AssignOperator(s)
		self.tokens.append(t)

		s = rd.consume_all()
		t = T_Expression(s)
		self.tokens.append(t)



class ParenType(Enum):
	""" Kind of parenthesis (parsing method) """

	UNKNOWN = 0
	""" Paren whose meaning is not resolved yet """

	EXPR = 1
	""" Paren as part of an expression.
	A single expression is expected.
	"""

	FOR = 2
	""" Paren as part of the FOR statement
	Three sections are expected, separated by semicolons;
	"""

	ARGVALS = 3
	""" Function call parameters, separated by commas """

	ARGNAMES = 4
	""" Function argument names, separated by commas """



class T_Paren(CompositeToken):
	""" Parenthesised block

	To parse this token, a `ParenType` must be selected.

	Args:
		value (str): the source code

	Attributes:
		ptype (ParenType): Parenthesis type;
			Determines tokenization method.

	Attributes (ParenType.EXPR):
		expression (T_Expression): In case of EXPR paren, the
			expression token is stored here (it is also stored
			as the only sub-token)

	Attributes (ParenType.FOR):
		for_init (Token[]):
			For loop init statements
		for_init_s (str):
			Source of the for_init

		for_cond (T_Expression):
			For condition expr
		for_cond_s (str):
			Source of the for_cond

		for_iter (Token[]):
			For loop iter statements
		for_iter_s (str):
			Source of the for_iter


	"""

	def __init__(self, value):
		super().__init__(value)

		self.ptype = ParenType.UNKNOWN


	def set_type(self, ptype):
		""" Set the paren type

		Changes the way the paren is tokenized

		Args:
			ptype (ParenType): The requested type

		"""

		self.ptype = ptype


	def _collect_expr(self, rd):
		""" Parse as single expression """

		rd.sweep()
		if rd.has_end():
			rd.error('Unexpected end of string (expected expression)')

		s = rd.consume_all()
		t = T_Expression(s)
		self.tokens.append(t)
		self.expression = t


	def _collect_argvals(self, rd):
		""" Parse as function call argument list """

		while not rd.has_end():

			rd.sweep()
			if rd.has_end():
				break  # end of args after some junk

			s = rd.consume_code(end=',', eof=True, keep_end=False)
			t = T_Expression(s)
			self.tokens.append(t)


	def _collect_argnames(self, rd):
		""" Parse as argument name list """

		while not rd.has_end():

			rd.sweep()
			if rd.has_end():
				break  # end of args after some junk

			s = rd.consume_identifier()
			t = T_Name(s)
			self.tokens.append(t)

			rd.sweep()
			if rd.starts(','):
				rd.consume()  # remove comma


	def _collect_for(self, rd):
		""" Parse as FOR loop paren """

		# init statement
		s = rd.consume_code(end=';', eof=False, keep_end=True).strip()

		tt = Tokenizer(s)
		self.for_init = tt.tokenize()  # tokenlist
		self.for_init_s = s

		# condition
		s = rd.consume_code(end=';', eof=False, keep_end=False).strip()
		if len(s) == 0:
			self.for_cond = T_Expression('1')  # true
			self.for_cond_s = '1'
		else:
			self.for_cond = T_Expression(s)  # one expression token
			self.for_cond_s = s

		# iter statement
		s = rd.consume_code(end=';', eof=True, keep_end=False).strip()
		s += ';'  # add the semicolon to make a complete statement
		tt = Tokenizer(s)
		self.for_iter = tt.tokenize()  # tokenlist
		self.for_iter_s = s


	def _tokenize(self):

		if self.ptype == ParenType.UNKNOWN:
			print('Paren has no type, cannot tokenize: ' + str(self))
			return

		rd = CodeReader(self.value[1:-1].strip())

		if self.ptype == ParenType.EXPR:
			# single expression
			self._collect_expr(rd)

		elif self.ptype == ParenType.ARGVALS:
			# comma-separated list of expressions, can be empty
			self._collect_argvals(rd)

		elif self.ptype == ParenType.ARGNAMES:
			# comma-separated list of argument names
			self._collect_argnames(rd)

		elif self.ptype == ParenType.FOR:
			# arguments for a FOR loop
			self._collect_for(rd)


	def __str__(self):

		s = type(self).__name__ + ' (...) : ' + str(self.ptype.name)

		if self.ptype == ParenType.UNKNOWN:
			s += ', Content: ' + self.value

		elif self.ptype == ParenType.FOR:
			self.tokenize()
			s += ' (INIT %s  | COND %s  | ITER %s )' % (
				self.for_init_s, self.for_cond_s, self.for_iter_s
			)

			s += '\n - INIT {%s}\n - COND {%s}\n - ITER {%s} )' % (
				', '.join([str(a) for a in self.for_init]),
				str(self.for_cond),
				', '.join([str(a) for a in self.for_iter])
			)

		return s



class T_Bracket(CompositeToken):
	""" Square bracket

	Used to specify an array index.

	Contains:
		T_Expression: The array index

	Attributes:
		(same as CompositeToken) +
		index (T_Expression): The index expression

	"""

	def _tokenize(self):

		rd = CodeReader(self.value[1:-1].strip())

		rd.sweep()

		s = rd.consume_code(end=',', eof=True, keep_end=False)
		t = T_Expression(s)
		self.tokens.append(t)
		self.index = t

		rd.sweep()

		if not rd.has_end():
			raise Exception(
				'Invalid array index (must be single expression).'
			)


	def __str__(self):

		return type(self).__name__ + ' [...]'



class T_CodeBlock(CompositeToken):
	""" Braced code block

	Contains:
		<statement[]>: The block body

	"""

	def __init__(self, value):

		super().__init__(value)


	def _tokenize(self):

		rd = Tokenizer(self.value[1:-1])
		self.tokens = rd.tokenize()


	def __str__(self):

		return type(self).__name__ + ' {...}'



class Tokenizer:
	""" Source tokenizer

	Creates a token list for input source code.

	Args:
		source (str): Source code to tokenize
		filename (str, optional): The file this source came from.
			Used mainly for error reporting.

	Attributes:
		filename (str): The filename provided in constructor
		source (str): The source provided in constructor
		tokens (Token[]): List of tokens, created by
			calling `tokenize()`. Used for caching.

	"""

	def __init__(self, source, filename=None):

		self.filename = filename
		self.source = source
		self.tokens = None


	def _add(self, token):
		""" Add a token to the list

		Args:
			token (Token): The added token

		"""

		self.tokens.append(token)


	def tokenize(self):
		""" Convert to tokens, get token list

		Returns:
			A list of obtained tokens, recursively tokenized.

		"""

		if self.tokens is not None:
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

				self._tokenize_identifier(rd)

			# {...stuff...}
			elif rd.has_code_block():

				s = rd.consume_block()
				self._add( T_CodeBlock(s) )

			# ;
			elif rd.starts(';'):

				self._collect_semicolon(rd)

			else:
				rd.error('Unexpected syntax here.')

		# tokenize all composite tokens
		for t in self.tokens:
			if t.is_composite():
				t.tokenize()

		return self.tokens


	def _collect_assign_stmt(self, rd):
		""" Collect a varname = value statement from the reader
		and add it as tokens.

		Leading whitespace is ignored.

		Args:
			rd (CodeReader): the reader

		"""

		rd.sweep()

		s = rd.consume_identifier()
		tok = T_Name(s)
		self._add(tok)

		rd.sweep()

		# array index bracket
		if rd.has_bracket():
			s = rd.consume_block()
			self._add(T_Bracket(s))
			rd.sweep()

		# increment or decrement statement
		if rd.starts('++') or rd.starts('--'):
			sign = rd.consume()
			rd.consume()  # discard the second
			self._add(T_Rvalue( "%s=1" % sign ))

		elif rd.has_rvalue():
			self._add(
				T_Rvalue(rd.consume_rvalue())
			)

		else:
			rd.error('Unexpected syntax.')


	def _collect_semicolon(self, rd):
		""" Collect a semicolon from the reader and add it
		as a token.

		Leading whitespace is ignored.

		Args:
			rd (CodeReader): the reader

		"""

		rd.sweep()

		rd.consume_exact(';')
		self._add( T_Semicolon() )


	def _collect_colon(self, rd):
		""" Collect a colon from the reader
		and add it as a token.

		Leading whitespace is ignored.

		Args:
			rd (CodeReader): the reader

		"""

		rd.sweep()

		rd.consume_exact(':')
		self._add( T_Colon() )


	def _collect_label(self, rd):
		""" Collect a `label:` from the reader
		and add it as tokens (T_LABEL, T_Name, T_Colon)

		The `label` keyword should already be consumed, if present.

		Leading whitespace is ignored.

		Args:
			rd (CodeReader): the reader

		"""
		rd.sweep()

		lbl = rd.consume_identifier()
		self._add( T_LABEL() )
		self._add( T_Name(lbl) )

		rd.sweep()
		rd.consume_exact(':')
		self._add( T_Colon() )


	def _collect_paren(self, rd, paren_type):
		""" Collect a parenthesis of a given type from the reader
		and add it as a token.

		Leading whitespace is ignored.

		Args:
			rd (CodeReader): the reader
			paren_type (ParenType): the expected type of parenthesis

		"""

		rd.sweep()

		if not rd.has_paren():
			rd.error('Expected parenthesis.')

		paren = rd.consume_block()

		t = T_Paren(paren)
		t.set_type(paren_type)
		self._add(t)


	def _tokenize_identifier(self, rd):

		""" Read an identifier from the reader and
		interpret it's meaning.

		If the identifier is a keyword, consume and tokenize all
		that is directly associated with the keyword and check for
		syntax errors in the process.

		Leading whitespace is ignored.

		Args:
			rd (CodeReader): the reader

		"""

		rd.sweep()

		pos_before_s = rd.pos

		s = rd.consume_identifier()

		rd.sweep()

		kwd = s.lower()

		# handle keywords first

		# if-elseif-else
		if kwd == 'if':
			self._add( T_IF() )
			self._collect_paren(rd, ParenType.EXPR)
			return

		elif kwd == 'else':
			self._add( T_ELSE() )
			return

		elif kwd == 'elseif':
			self._add( T_ELSE() )
			self._add( T_IF() )
			self._collect_paren(rd, ParenType.EXPR)
			return

		# the various loops
		elif kwd == 'while':
			self._add( T_WHILE() )
			self._collect_paren(rd, ParenType.EXPR)
			return

		elif kwd == 'for':
			self._add( T_FOR() )
			self._collect_paren(rd, ParenType.FOR)
			return

		elif kwd == 'do':
			self._add( T_DO() )
			return

		elif kwd == 'continue':
			self._add( T_CONTINUE() )
			return

		elif kwd == 'break':
			self._add( T_BREAK() )
			return

		# the switch statemnt
		elif kwd == 'switch':
			self._add( T_SWITCH() )
			self._collect_paren(rd, ParenType.EXPR)
			return

		elif kwd == 'case':
			self._add( T_CASE() )

			expr = rd.consume_code(end=':', consume_end=False)
			t = T_Expression(expr)
			self._add(t)

			self._collect_colon(rd)
			return

		elif kwd == 'default':
			self._add( T_DEFAULT() )

			self._collect_colon(rd)
			return

		elif kwd == 'var':

			while True:
				self._add( T_VAR() )
				rd.sweep()

				# varname
				name = rd.consume_identifier()
				self._add( T_Name(name) )

				rd.sweep()

				# initial value assignment
				if rd.has_rvalue():
					v = rd.consume_rvalue()
					self._add( T_Rvalue(v) )

				rd.sweep()

				# whats next?
				if rd.starts(','):
					# more vars

					rd.consume()  # the comma

					self._add( T_Semicolon() )  # start new statement

					continue  # to next var name

				elif rd.starts(';'):
					# end of it
					rd.consume()  # the sc
					self._add( T_Semicolon() )
					break  # to next statement

				else:
					rd.error('Expected , or ; here.')
			return

		elif kwd == 'goto':
			self._add( T_GOTO() )

			lbl = rd.consume_identifier()
			t = T_Name(lbl)
			self._add(t)

			self._collect_semicolon(rd)
			return

		elif kwd == 'label':
			# the label keyword (optional for labels)

			self._collect_label(rd)
			return

		elif kwd == 'return':
			self._add( T_RETURN() )

			if not rd.starts(';'):
				# return with no value
				expr = rd.consume_code(end=';', consume_end=False)
				t = T_Expression(expr)
				self._add(t)

			# the semicolon
			self._collect_semicolon(rd)
			return

		elif rd.has_paren():
			# function call or declaration

			paren = rd.consume_block()  # consume the paren

			rd.sweep()

			if rd.starts(';'):
				# a call
				self._add( T_CALL() )
				self._add( T_Name(s) )

				t = T_Paren(paren)
				t.set_type(ParenType.ARGVALS)
				self._add(t)

				self._collect_semicolon(rd)
				return

			elif rd.has_code_block():
				# a declaration
				self._add( T_FUNCTION() )
				self._add( T_Name(s) )

				t = T_Paren(paren)
				t.set_type(ParenType.ARGNAMES)
				self._add(t)

				rd.sweep()

				cbl = rd.consume_block()
				self._add( T_CodeBlock(cbl) )
				return

		elif (
			rd.has_bracket() or
			rd.has_rvalue() or
			rd.starts('++') or
			rd.starts('--')
		):

			# foo = bar, other = baz;
			self._add( T_SET() )

			rd.pos = pos_before_s  # rewind

			self._collect_assign_stmt(rd)

			rd.sweep()

			if rd.starts(';'):
				self._collect_semicolon(rd)
				return

			elif rd.starts(','):
				rd.consume()  # the comma

				while True:
					rd.sweep()

					if rd.has_identifier():

						self._add( T_Semicolon() )  # start new statement
						self._add( T_SET() )

						self._collect_assign_stmt(rd)

					else:
						rd.error('Missing identifier.')

					rd.sweep()

					if rd.starts(','):
						rd.consume()
						continue

					elif rd.starts(';'):
						self._collect_semicolon(rd)
						break

					else:
						rd.error('Expected , or ; here.')

				return

		else:
			# just a name
			rd.sweep()

			if rd.starts(':'):
				# was a label without "label" keyword

				rd.pos = pos_before_s

				self._collect_label(rd)

				return

			# unknown meaning
			rd.error("Unexpected syntax: Can't resolve what \"%s\" means here." % s)

		# unknown meaning
		rd.error("Invalid syntax found - missing semicolon maybe?")


	def show(self):
		""" Print tokens to console

		Used for debugging the tokenizer.
		"""

		if self.tokens is None:
			raise Exception('Not parsed yet.')

		show_tokenlist(self.tokens)



def show_tokenlist(tokens, level='  '):
	""" Show a token list, recursively.

	Args:
		tokens (Token[]): Tokens to show
		level (str, optional): Indentation for this level

	"""

	if len(tokens) == 0:
		print(level + '-empty-')

	else:
		for tok in tokens:

			print(level + str(tok))

			if tok.is_composite():
				show_tokenlist(tok.tokenize(), level + '  ')



class TokenWalker:
	""" Recognizes nodes in a token list

	Args:
		tokens (Token[]): token list to walk

	Attributes:
		pos (int): index of current token
		tokens (Token[]): the token list is stored here

	"""

	def __init__(self, tokens):

		# initialize instance variables
		self.pos = 0
		self.tokens = tokens


	def has_next(self):
		""" Get if the walker has more tokens to walk """
		return self.pos < len(self.tokens)


	def peek(self, offset=0):
		""" Peek at the n-th token relative to cursor """

		i = self.pos + offset

		if not i in range(0, len(self.tokens)):
			return None  # EOL

		return self.tokens[i]


	def has(self, cls, offset=0):
		""" Get if the next (or offset) token is of given type """

		return isinstance(self.peek(offset), cls)


	def move(self, steps=1):
		""" Move the cursor """

		self.pos += steps


	def consume_paren(self, ptype):
		""" Consume a paren, assert it is of the
		given type.

		Args:
			ptype (ParenType): The required type

		Returns:
			the paren token
		"""

		paren = self.consume(T_Paren)

		if not paren.ptype == ptype:
			raise Exception(
				'Found paren of type %s, expected %s' % (
					paren.ptype.name, ptype.name
				)
			)

		return paren


	def consume(self, cls=None):
		""" Consume one token, move the cursor.
		Asserts it is of the right type

		Args:
			cls (Token class): required token class

		Returns:
			the token
		"""

		if not self.has_next():
			raise Exception(
				'Unexpected end of token list.'
			)

		if cls is not None:
			if not self.has(cls):
				raise Exception(
					'Expected ' +
					cls.__name__ +
					', found ' +
					type(self.peek()).__name__
				)

		t = self.peek()
		self.move()
		return t
