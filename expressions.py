#!/bin/env python3

from tokens import *
from utils import SyntaxNode
from sdscp_errors import *

def parse(expr_token):
	""" Converts T_Expression to Expression

	Variables and brackets are put together to form array
	variables, literals are unified as E_Literal, function
	calls are connected with their parentheses.

	Therefore, some basic validation is performed, but nothing
	deep (eg. arity is not checked)

	Args:
		expr_token (T_Expression): The parsed expression token

	Returns:
		Expression

	"""

	tw = TokenWalker(expr_token.tokenize())

	eg = E_Group()

	while tw.has_next():

		# function call with args
		if tw.has(T_Name) and tw.has(T_Paren, offset=1):
			name = tw.consume(T_Name).value.strip()
			paren = tw.consume_paren(ParenType.ARGVALS)

			args = [parse(a) for a in paren.tokenize()]

			eg._add( E_Call(name, args) )

		# variable with bracket
		elif tw.has(T_Name) and tw.has(T_Bracket, offset=1):
			name = tw.consume(T_Name).value.strip()
			bracket = tw.consume(T_Bracket)

			eg._add( E_Variable(name, parse(bracket.index)) )

		# variable
		elif tw.has(T_Name):
			name = tw.consume(T_Name).value.strip()

			eg._add( E_Variable(name) )

		# any operator
		elif tw.has(T_Operator):
			value = tw.consume(T_Operator).value.strip()

			eg._add( E_Operator(value) )

		# any literal
		elif tw.has(T_String) or tw.has(T_Char) or tw.has(T_Number):

			lit = tw.consume()

			eg._add( E_Literal(lit) )

		# a paren
		elif tw.has(T_Paren):

			paren = tw.consume_paren(ParenType.EXPR)

			# convert and unwrap
			eg._add( parse(paren.expression) )

		else:
			raise SdscpSyntaxError('Unexpected token in expression: %s' % str(tw.peek()))

	# simplify - unwrap single-child parens (even nested)
	while isinstance(eg, E_Group) and len(eg.children) == 1:
		eg = eg.children[0]

	return eg



class Expression(SyntaxNode):
	""" Represents an expression.

	This is a higher level expression than T_Expression.
	It a syntaxtic unit in larger expression.

	"""

	def __str__(self):
		return type(self).__name__



class E_Group(Expression):
	""" An expression group. Visually, a parenthesis.

	Args:
		children (Expression[]):
			A list of child expressions

	Attributes:
		children (Expression[]):
			The child expressions.

	"""

	def __init__(self, children=None):
		super().__init__()

		if children is None:
			children = []

		self.children = children


	def _add(self, child):
		""" Add a child expression

		Args:
			child (Expression): The added child expr

		"""

		self.children.append(child)


	def _bind_children(self):
		for e in self.children:
			e.bind_parent(self)


	def __str__(self):
		return '(%s)' % ', '.join( [str(a) for a in self.children] )



class E_Literal(Expression):
	""" A literal of any type, as an expression.

	Args:
		token (Token): The literal token

	Attributes:
		token (Token): The literal token
		value (str): The value of the token is kept here

	"""

	def __init__(self, token):
		super().__init__()

		self.token = token
		self.value = token.value


	def is_string(self):
		return isinstance(self.token, T_String)


	def is_char(self):
		return isinstance(self.token, T_Char)


	def is_number(self):
		return isinstance(self.token, T_Number)


	def __str__(self):
		return self.value



class E_Operator(Expression):
	""" An operator of any kind.

	Args:
		value (str): The operator as found in source code.

	Attributes:
		value (str): The operator is kept here

	"""

	def __init__(self, value):
		super().__init__()

		self.value = value


	def __str__(self):
		return self.value



class E_Variable(Expression):
	""" Variable in expression, or a Lvalue.

	Can be array element.

	Args:
		name (str): Variable name
		index (Expression, optional):
			Array index (for array variable)

	Attributes:
		name (str): Variable name
		index (T_Expression): The array index, or None for non-array

	"""

	def __init__(self, name, index=None):
		super().__init__()

		self.name = name

		if isinstance(index, T_Expression):
			index = parse(index)

		self.index = index


	def is_array(self):
		""" Check if this variable is array element """

		return self.index is None


	def _bind_children(self):
		if self.index is not None:
			self.index.bind_parent(self)


	def __str__(self):
		s = self.name
		if self.index is not None:
			s += '[%s]' % self.index
		return s



class E_Call(Expression):
	""" Represents a function call in expression.

	The return value is used in the expression.

	Args:
		name (str): Name of the called function
		args (Expression[]):
			Function arguments.
			Use empty list for no-argument functions.

	Attributes:
		name (str): The func name
		args (Expression[]): The call args

	"""

	def __init__(self, name, args=None):
		super().__init__()
		if args is None:
			args = []

		self.name = name
		self.args = args


	def _bind_children(self):
		for e in self.args:
			e.bind_parent(self)


	def __str__(self):
		s = self.name + '(%s)' % ', '.join( [str(a) for a in self.args] )
		return s
