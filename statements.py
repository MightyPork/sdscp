#!/bin/env python3

import re

from tokens import *


class Statement:
	""" A syntactic unit

	A code piece that makes sense on it's own, and can be
	converted to source code if needed.
	"""

	def __str__(self):
		return type(self).__name__



class S_Empty(Statement):
	""" An empty statement (nop)

	Args:
		tw (TokenWalker): tw to collect the statement from

	"""

	def __init__(self, tw):
		tw.consume(T_Semicolon)



class S_Goto(Statement):
	""" A goto statement. Will work only with label
	that is in the same function.

	Args:
		tw (TokenWalker): tw to collect the statement from

	Attributes:
		name (T_Name):
			Name of the label to jump to.

	"""

	def __init__(self, tw):
		# keyword
		tw.consume(T_GOTO)

		# the label name
		self.name = tw.consume(T_Name)

		# a semicolon
		tw.consume(T_Semicolon)



class S_Label(Statement):
	""" A label, goto target.

	Args:
		tw (TokenWalker): tw to collect the statement from

	Attributes:
		name (T_Name):
			Name of the label. Must be unique within the function.

	"""

	def __init__(self, tw):
		# keyword
		tw.consume(T_LABEL)

		# the label name
		self.name = tw.consume(T_Name)

		# a colon
		tw.consume(T_Colon)



class S_Call(Statement):
	""" Function call, discarding the return value.

	Args:
		tw (TokenWalker): tw to collect the statement from

	Attributes:
		name (T_Name): function name
		args (T_Expression[]): list of argument values

	"""

	def __init__(self, tw):

		# keyword
		tw.consume(T_CALL)

		# func name
		self.name = tw.consume(T_Name)

		# arguments paren
		paren = tw.consume_paren(ParenType.ARGVALS)

		# collect all argument names
		atw = TokenWalker(paren.tokens)
		self.args = []
		while atw.has_next():
			val = atw.consume(T_Expression)
			self.args.append(val)

		tw.consume(T_Semicolon)



class S_Function(Statement):
	""" A function statement

	Args:
		tw (TokenWalker): tw to collect the statement from

	Attributes:
		name (T_Name): function name
		args (T_Name[]): list of argument names
		body_st (S_Block): a function body

	"""

	def __init__(self, tw):

		# keyword
		tw.consume(T_FUNCTION)

		# func name
		self.name = tw.consume(T_Name)

		# arguments paren
		paren = tw.consume_paren(ParenType.ARGNAMES)

		# collect all argument names
		atw = TokenWalker(paren.tokens)
		self.args = []
		while atw.has_next():
			n = atw.consume(T_Name)
			self.args.append(n)

		# get function body
		self.body_st = S_Block(tw)



class S_Return(Statement):
	""" A return statement

	Args:
		tw (TokenWalker): tw to collect the statement from

	Attributes:
		value (T_Expression): The return value

	"""

	def __init__(self, tw):
		# keyword
		tw.consume(T_RETURN)

		if tw.has(T_Expression):
			# explicitly given return value
			self.value = tw.consume(T_Expression)
		else:
			# a defualt return value
			self.value = T_Expression('0')

		tw.consume(T_Semicolon)



class S_Case(Statement):
	""" A case in switch.

	Args:
		tw (TokenWalker): tw to collect the statement from

	Attributes:
		value (T_Expression):
			The case value (compared to the switch value)

	"""

	def __init__(self, tw):
		# keyword
		tw.consume(T_CASE)

		# the value
		self.value = tw.consume(T_Expression)

		# a colon
		tw.consume(T_Colon)



class S_Break(Statement):
	""" A break statement, used in loops and switch.

	Args:
		tw (TokenWalker): tw to collect the statement from

	"""

	def __init__(self, tw):
		# keyword
		tw.consume(T_BREAK)

		# a semicolon
		tw.consume(T_Semicolon)



class S_Continue(Statement):
	""" A continue statement, used in loops.

	Args:
		tw (TokenWalker): tw to collect the statement from

	"""

	def __init__(self, tw):
		# keyword
		tw.consume(T_CONTINUE)

		# a semicolon
		tw.consume(T_Semicolon)



class S_Block(Statement):
	""" A code block statement

	A block has it's own variable scope and can
	hold any number of child statements.

	Args:
		tw (TokenWalker): tw to collect the statement from

	Attributes:
		statements (Statement[]): List of body statements

	"""

	def __init__(self, tw):

		self.statements = []

		# keyword
		cb = tw.consume(T_CodeBlock)

		# code-block token walker
		ctw = TokenWalker(cb.tokens)

		# collect all child statements
		while ctw.has_next():
			st = ctw.consume_statement()

			# add if not an empty statement
			if not isinstance(st, S_Empty):
				self.statements.append(st)



class S_Var(Statement):
	""" A variable declaration.

	Args:
		tw (TokenWalker): tw to collect the statement from

	Attributes:
		name (str): the variable name
		value (T_Expression): the initial value

	"""

	def __init__(self, tw):

		# keyword
		tw.consume(T_VAR)

		# variable name
		self.name = tw.consume(T_Name)

		# optional rvalue
		if tw.has(T_Rvalue):

			# operator and value
			rv = tw.consume(T_Rvalue)
			assignOp = rv.tokens[0]
			expr = rv.tokens[1]

			# cannot use other than simple = in declaration
			# the variable isn't defined yet.
			if assignOp.value != '=':
				raise Exception(
					'Cannot use %s in variable declaration!'
					% assignOp.value
				)

			self.value = expr

		else:
			# synthetic zero value
			self.value = T_Expression('0')

		tw.consume(T_Semicolon)



def S_Assign(Statement):
	""" A variable assignment.

	Args:
		tw (TokenWalker): tw to collect the statement from

	Attributes:
		name (T_Name): the variable name
		op (T_AssignOperator): the assignment operator, eg. += or =
		value (T_Expression): the assigned value

	"""

	def __init__(self, tw):

		# keyword
		tw.consume(T_SET)

		# variable name
		self.name = tw.consume(T_Name)

		# operator and value
		rv = tw.consume(T_Rvalue)
		self.op = rv.tokens[0]
		self.value = rv.tokens[1]

		# end of statement
		tw.consume(T_Semicolon)



def S_If(Statement):
	""" If-else statement

	Args:
		tw (TokenWalker): tw to collect the statement from

	Attributes:
		cond (T_Expression): the branching condition
			goes to "true" branch if th condition is non-zero.
		then_st (Statement): the "true" statement
		else_st (Statement): the "false" statement

	"""

	def __init__(self, tw):

		# keyword
		tw.consume(T_IF)

		# paren with condition
		paren = tw.consume_paren(ParenType.EXPR)
		self.cond = paren.expression

		# the "then" branch
		self.then_st = tw.consume_statement()

		if tw.has(T_ELSE):
			# "else" branch
			self.else_st = tw.consume_statement()
		else:
			# there is no "else" branch
			# add empty statement instead.
			self.else_st = S_Empty()



def S_While(Statement):
	""" While loop

	Args:
		tw (TokenWalker): tw to collect the statement from

	Attributes:
		cond (T_Expression): the loop condition.
			Tested before each cycle.
		body (Statement): the loop body statement

	"""

	def __init__(self, tw):

		# keyword
		tw.consume(T_WHILE)

		# paren with condition
		paren = tw.consume_paren(ParenType.EXPR)
		self.cond = paren.expression

		# the loop body
		self.body_st = tw.consume_statement()



def S_DoWhile(Statement):
	""" Do-While loop

	Args:
		tw (TokenWalker): tw to collect the statement from

	Attributes:
		cond (T_Expression): the loop condition.
			Tested before each cycle.
		body (Statement): the loop body statement

	"""

	def __init__(self, tw):

		# keyword
		tw.consume(T_DO)

		# the loop body
		self.body_st = tw.consume_statement()

		# keyword
		tw.consume(T_WHILE)

		# paren with condition
		paren = tw.consume_paren(ParenType.EXPR)
		self.cond = paren.expression

		# end of the statement.
		tw.consume(T_Semicolon)



def S_For(Statement):
	""" For loop

	Args:
		tw (TokenWalker): tw to collect the statement from

	Attributes:
		init (Statement[]): the init statement
		cond (T_Expression): the loop condition;
			Tested before each cycle.
		iter (Statement[]): the iter statement;
			Executed after each cycle.
		body (Statement): the loop body statement

	"""

	def __init__(self, tw):

		# keyword
		tw.consume(T_FOR)

		# paren with init, cond, iter
		paren = tw.consume_paren(ParenType.FOR)
		self.cond = paren.for_cond

		# init statements
		itw = TokenWalker(paren.for_init)
		self.init = []
		while itw.has_next():
			s = itw.consume_statement()
			self.init.append(s)

		# iter statements
		itw = TokenWalker(paren.for_iter)
		self.iter = []
		while itw.has_next():
			s = itw.consume_statement()
			self.iter.append(s)

		# the loop body
		self.body_st = tw.consume_statement()



def S_Switch(Statement):
	""" Switch statement

	CASEs that are in the body's top level are part
	of this switch.

	Anywhere in the body can be used a BREAK statement
	to escape from the switch (of course, if it is nested
	in a loop or other switch, it has no effect on this
	main switch)

	Args:
		tw (TokenWalker): tw to collect the statement from

	Attributes:
		value (T_Expression): The switch value;
			The CASE values are compared with it.

		body (T_Block): The switch body.

	"""

	def __init__(self, tw):

		# keyword
		tw.consume(T_SWITCH)

		# paren with condition
		paren = tw.consume_paren(ParenType.EXPR)
		self.value = paren.expression

		# the switch body
		self.body_st = tw.consume(T_CodeBlock)



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


	def consume_statement(self):
		""" Try to consume a statement, based on the current
		token (typically keyword)

		Returns:
			the statement

		"""

		# code block (used in structures)
		if self.has(T_CodeBlock):
			return S_Block(self)

		# empty statemenr
		if self.has(T_Semicolon):
			return S_Empty(self)

		# a function
		if self.has(T_FUNCTION):
			return S_Function(self)

		# return statement
		if self.has(T_RETURN):
			return S_Return(self)

		# GOTO statement
		if self.has(T_GOTO):
			return S_Goto(self)

		# LABEL
		if self.has(T_LABEL):
			return S_Label(self)

		# if-else
		if self.has(T_IF):
			return S_If(self)

		# a switch statement
		if self.has(T_SWITCH):
			return S_Switch(self)

		# while
		if self.has(T_WHILE):
			return S_While(self)

		# do-while
		if self.has(T_DO):
			return S_DoWhile(self)

		# for
		if self.has(T_FOR):
			return S_For(self)

		# break
		if self.has(T_BREAK):
			return S_Break(self)

		# continue
		if self.has(T_CONTINUE):
			return S_Continue(self)

		# var declaration
		if self.has(T_VAR):
			return S_Var(self)

		# var assignment
		if self.has(T_SET):
			return S_Assign(self)


		# ...

		# token not recognized
		raise Exception(
			'Could not create statement for token %s' % (
				str(self.peek())
			)
		)


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

		self.move()


	def rewind(self):
		""" Go to beginning """

		self.pos = 0



