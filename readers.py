#!/bin/env python3

import re
from sdscp_errors import *

class BaseReader:
	""" Utility for scanning through a text

	Args:
		source (str): The text to read
		filename (str): The file the text came from
			Used for error reporting.

	Attributes:
		text (str): The scanned text
		filename (str): The file the text came from
		pos (int): Current cursor position in the text
		length (int): Length of the text

	"""

	def __init__(self, source, filename=None):

		# Initialize instance varibales
		self.text = source
		self.filename = filename
		self.pos = 0
		self.length = len(source)


	def set_pos(self, p):
		self.pos = p


	def near(self):
		""" Get something near the current cursor,
		for error messages.

		Format:
			At: >>Stuff That Follows<<,
			Near: >>A Bit Before And A Bit After<<

		"""

		begin = self.pos-20
		end = self.pos+20

		if begin < 0:
			begin = 0

		if end > self.length:
			end = self.length

		near = re.sub(r'[\n\t ]+', ' ', self.text[begin:end])
		fwd = re.sub(r'[\n\t ]+', ' ', self.text[self.pos:self.pos+20])

		return 'At: >>%s<<\nNear: >>%s<<' % (fwd, near)


	def pos2line(self, pos):
		""" Convert absolute pos to line number

		Args:
			pos (int): Character position in the text

		Returns:
			Line number the `pos` is at.

		"""

		processed = self.text[:pos]
		return processed.count('\n') + 1


	def pos2col(self, pos):
		""" Convert absolute pos to column number

		Args:
			pos (int): Character position in the text

		Returns:
			Column number the `pos` is at.

		"""

		processed = self.text[:pos]
		lineno = processed.count('\n') + 1

		if lineno == 1:
			return len(processed)
		else:
			return len(processed) - processed.rindex('\n')


	def error(self, message):
		""" Report an error

		Raise a SdscpSyntaxError with the current position,
		what's "near" and the given error message.

		Args:
			message (str): The error message

		"""

		lineno = self.pos2line(self.pos)
		column = self.pos2col(self.pos)

		if self.filename is None:
			raise SdscpSyntaxError(message + '\n' + self.near())
		else:
			raise SdscpSyntaxError(
				message +
				'\nIn file %s at line %d, col %d,\n%s' % (
					self.filename, lineno, column, self.near()
				)
			)


	def peek(self, chars=1, offset=0):
		""" Look at the next chars

		Does not change current `pos`.

		Args:
			chars (int): Number of chars to get (max)
			offset (int, optional):
				How many characters to skip before taking the "peek".
				Counted from the current pos; defualt is 0.

		Returns:
			`chars` characters starting at the current `pos`.

		"""

		self.validate_cursor()

		return self.text[self.pos + offset : self.pos + offset + chars]


	def from_pos(self, pos_begin):
		""" Get text from `pos_begin` to the current `pos`.

		The character at the current `pos` is not included.

		Args:
			pos_begin (int): Start of the retrieved chunk of text

		Returns:
			characters from `pos_begin` to the current `pos`

		"""

		if pos_begin > self.pos:
			raise Exception('pos_begin must be <= current pos.')

		return self.text[pos_begin : self.pos]


	def starts(self, expected):
		""" Get if the following text starts with
		the given string. By "following" is meant the portion
		from the current `pos`.

		Args:
			expected (str): The tested string

		Returns:
			True if the following text starts with `expected`
		"""

		if self.has_end():
			return False

		self.validate_cursor()

		return expected == self.text[ self.pos : self.pos+len(expected) ]


	def matches(self, regex, flags=0):
		""" Get if the following text matches the given regex.

		By "following" is meant the portion from the current `pos`.

		Args:
			regex (str/regex): The tested regex
			flags (int): re flags

		Returns:
			True if the following text matches the `regex`

		"""

		self.validate_cursor()

		return re.match(regex, self.text[self.pos:], flags)


	def move(self, chars=1):
		""" Move the cursor

		Args:
			chars (int, optional):
				Number of chars to skip, defaults to 1.

		"""

		self.pos += chars


	def end_reached(self):
		""" Get if the cursor is at the end of string

		Returns:
			True if the cursor is beyond the last character.

		"""

		return self.pos >= self.length


	def validate_cursor(self):
		""" Assert that the cursor is not outside text bounds.

		If the assertion is not met, an error is raised.
		"""

		if self.pos >= self.length or self.pos < 0:
			self.error('Unexpected end of scope. Maybe something like missing semicolon?')


	def consume(self, chars=1):
		""" Advance forth and return the found characters

		Args:
			chars (int, optional):
				Number of characters to consume, defaults to 1.

		Returns:
			The consumed characters

		"""

		self.validate_cursor()

		pos_begin = self.pos
		self.move(chars)
		return self.from_pos(pos_begin)


	def consume_exact(self, to_consume):
		""" Consume the given string

		Does the same as

			consume(len(to_consume))

		but only if the following text starts with
		the expetced string.

		Args:
			to_consume (str): The string to consume

		Returns:
			The consumed string.

		"""

		self.validate_cursor()

		if not self.starts(to_consume):
			self.error('Expected %s, found %s' % ( to_consume, self.peek( len(to_consume) ) ) )

		return self.consume( len(to_consume) )


	def consume_until(self, end, eof=False, consume_end=True, keep_end=True):
		""" Consume characters until the `end` is found or the
		end of text is reached.

		Args:
			end (str): The end mark, can be multiple characters long.
			eof (bool, optional):
				Whether to allow EOF instead of the `end` mark.
				False to raise error if `end` is not found.
				Defaults to False.
			consume_end (bool, optional):
				Whether to include the `end` mark in the consumed string.
				Defaults to True.
			keep_end:
				Whether to keep the `end`, if it is found an consumed.
				Set to False to discard the `end` mark.
				Defaults to True.

		Returns:
			The consumed string.

		"""

		self.validate_cursor()

		pos_begin = self.pos

		while self.pos+len(end) <= self.length:

			if self.starts(end):

				if not consume_end:
					return self.from_pos(pos_begin)
				else:
					if keep_end:
						self.pos += len(end) # advance past the delimiter
						txt = self.from_pos(pos_begin)

					else:
						txt = self.from_pos(pos_begin)
						self.pos += len(end) # advance past the delimiter

					return txt

			self.consume() # advance one character

		if eof:
			self.pos = self.length
			return self.from_pos(pos_begin)
		else:
			self.pos = pos_begin
			self.error('Expected to find %s, reached end of file.' % end)


	def consume_line(self):
		""" Consume until newline or EOF, including the newline """

		return self.consume_until('\n', eof=True) # until newline or EOF


	def consume_all(self):
		""" Consume all until EOF """

		pos_begin = self.pos
		self.pos = self.length
		return self.from_pos(pos_begin)


	def assert_matches(self, regex):
		""" Raise error if the given regex does not match

		Args:
			regex (str/regex): The texted regex

		"""

		if not self.matches(regex):
			self.error('Unexpected character, expected to match: ' + regex.pattern)


	def assert_starts(self, string):
		""" Raise error if the following text
		does not start with the given piece.

		Args:
			string (str): The expected string.

		"""

		if not self.starts(string):
			self.error('Unexpected character, expected: '+string)




class CodeReader(BaseReader):
	""" Utility for scanning through C-like source code

	Args:
		source (str): The source code text
		filename (str, optional):
			Name of the file the text came from.
			Defaults to None.

	Attributes:
		Various regexes

	"""


	RE_IDENTIFIER_START = re.compile(r'[a-z_]', re.I|re.A) # ignorecase | ascii
	RE_IDENTIFIER_BODY  = re.compile(r'\w', re.I|re.A)

	RE_IDENTIFIER       = re.compile(
		r''' # identifier
		^[a-z_]
		\w*
		(?:[^\w]|\Z)
		''', re.I|re.A|re.X
	)

	RE_STRING_QUOTE = re.compile(r'^"')
	RE_CHAR_QUOTE   = re.compile(r'^\'')

	RE_PAREN_OPEN  = re.compile(r'^[\[({]')
	RE_PAREN_CLOSE = re.compile(r'^[\])}]')

	COMMENT       = '//'
	COMMENT_OPEN  = '/*'
	COMMENT_CLOSE = '*/'

	RE_COMMENT_OPEN  = re.compile(r'^/\*')
	RE_COMMENT_CLOSE = re.compile(r'^\*/')

	RE_RVALUE_EXTENDED_EQUALS = re.compile(r'^[-*+/%&|^]=')

	RE_OPERATOR = re.compile(
		r''' # operator
		(?:
			[-<>+*/%|&^~!]	# short operators
			| &&			# long operators
			| \|\|
			| <<
			| >>
			| >=
			| <=
			| ==
			| !=
			| \+\+
			| --
		)
		''', re.I|re.X
	)


	RE_LABEL = re.compile(
		r''' # label
		^
		( label[ \t]+ )?	# optional label keyword
		[a-z_]	# identifier
		\w*
		:
		''', re.I|re.A|re.X
	)

	# assoc array of left-to-right parens
	PARENS = {
		'(': ')',
		'[': ']',
		'{': '}'
	}


	def __init__(self, source, filename=None):
		super().__init__(source, filename)


	def sweep(self):
		""" Consume comments and whitespace

		Returns:
			The consumed whitespace and comments

		"""

		pos_begin = self.pos

		while self.pos < self.length:

			# single-line comment
			if self.has_inline_comment():
				self.consume_inline_comment()
				continue

			# multi-line comment
			if self.has_block_comment():
				self.consume_block_comment()
				continue

			# meaning-less whitespace
			if self.matches(r'\s+'):
				self.consume_whitespace()
				continue

			break

		return self.from_pos(pos_begin)


	def consume_block(self, keep_parens=True):
		""" Consume until matching close parenthesis

		Args:
			keep_parens (boo, optional):
				Whether to keep the parentheses in the
				returned string. They are consumed either way.

		Returns:
			The consumed block (), {} or []

		"""

		pos_begin = self.pos
		opening = self.peek()

		self.assert_matches(self.RE_PAREN_OPEN);

		closing = self.PARENS.get(opening)

		if closing is None:
			self.error('Invalid opening paren/bracket: %s' % opening)

		nested = 0
		self.consume()

		while self.pos < self.length:

			self.sweep()

			if self.matches( self.RE_STRING_QUOTE ):
				self.consume_string()
				continue

			if self.matches( self.RE_CHAR_QUOTE ):
				self.consume_char()
				continue

			# look ahead
			char = self.consume()

			if char == opening:
				# nested paren
				nested += 1

			elif char == closing:
				if nested == 0:
					if keep_parens:
						return self.from_pos(pos_begin)
					else:
						return self.from_pos(pos_begin)[1:-1].strip()
				else:
					nested -= 1

		self.set_pos(pos_begin)
		self.error( 'Unterminated %s...%s block' % (opening, closing) )


	def consume_block_comment(self):
		""" Consume a block comment

		Returns:
			The consumed comment

		"""

		pos_begin = self.pos

		self.consume_exact(self.COMMENT_OPEN)
		self.consume_until(self.COMMENT_CLOSE)

		return self.from_pos(pos_begin)


	def consume_inline_comment(self):
		""" Consume a inline comment

		Returns:
			The consumed comment

		"""

		return self.consume_line()


	def consume_code(self, end=';', eof=False, consume_end=True, keep_end=True):
		""" Consume code chunk until the given `end` delimiter.

		Takes care of nested parentheses, comments and strings.

		Args:
			end (str): The end mark, can be multiple characters long.
			eof (bool, optional):
				Whether to allow EOF instead of the `end` mark.
				False to raise error if `end` is not found.
				Defaults to False.
			consume_end (bool, optional):
				Whether to include the `end` mark in the consumed string.
				Defaults to True.
			keep_end:
				Whether to keep the `end`, if it is found an consumed.
				Set to False to discard the `end` mark.
				Defaults to True.

		Returns:
			The consumed code

		"""

		if type(end) == str:
			end = [end] # wrap as array

		pos_begin = self.pos
		buffer = ''

		while self.pos < self.length:

			for ee in end:
				if self.starts(ee):
					if not consume_end:
						return buffer.strip()
					else:
						if keep_end:
							# consume end and add it to the value
							buffer += self.consume_exact(ee)
							return buffer.strip()
						else:
							# consume end, but don't add it to the value
							self.consume_exact(ee)
							return buffer.strip()

			char = self.peek()

			if char in ['(', '[']:
				buffer += self.consume_block()
				continue

			elif self.has_string():
				buffer += self.consume_string()
				continue

			elif self.has_char():
				buffer += self.consume_char()
				continue

			elif self.has_block_comment():
				self.consume_block_comment()
				continue

			elif self.has_inline_comment():
				self.consume_inline_comment()
				continue

			buffer += self.consume()

		if eof:
			return buffer.strip()
		else:
			self.set_pos(pos_begin)
			self.error('Expected to find %s, found End Of File.' % end)


	def consume_char(self):
		""" Consume a char literal

		Returns:
			The consumed char literal, including the quotes.

		"""

		pos_begin = self.pos

		self.assert_matches(self.RE_CHAR_QUOTE)

		quote = self.consume()
		buffer = quote

		if self.has_end():
			self.error('Unexpected end of char literal')

		if re.match(r"[\t\n]+", self.peek()):
			self.error('Invalid char literal')

		if self.peek() == '\\':
			buffer += self.consume(2) # the backslash & the following character

		if self.peek() == "'":
			self.error('Empty char literal.')

		else:
			char = self.consume()
			buffer += char

		endq = self.consume()
		buffer += endq

		if endq != quote:
			self.error( 'Invalid char syntax. For strings, use DOUBLE quotes!' )

		return buffer


	def consume_string(self):
		""" Consume a string literal.
		The cursor must be at the opening quote.

		Returns:
			The consumed string literal, including the quotes.

		"""

		pos_begin = self.pos

		self.assert_matches(self.RE_STRING_QUOTE);

		quote = self.consume();

		while not self.has_end():
			char = self.consume()
			if char == '\n':
				self.error('Unterminated string literal - must end on the same line.')

			if char == '\\': # backslash
				self.consume() # consume next character also (even quote)

			elif char == quote:
				return self.from_pos(pos_begin) # end quote

		self.set_pos(pos_begin)
		self.error('Unterminated string literal.')


	def consume_whitespace(self):
		""" Consume any following whitespace

		Returns:
			The consumed whitespace

		"""

		pos_begin = self.pos

		while self.pos < self.length:

			if self.matches(r'[ \n\t]'):
				self.consume() # advance
			else:
				return self.from_pos(pos_begin) # not whitespace anymore

		# end reached
		return self.from_pos(pos_begin) # all till the end


	def consume_inline_whitespace(self):
		""" Consume any following inline whitespace

		Returns:
			The consumed whitespace

		"""

		pos_begin = self.pos

		while self.pos < self.length:

			if self.matches(r'[ \t]'):
				self.consume() # advance
			else:
				return self.from_pos(pos_begin) # not whitespace anymore

		return self.from_pos(pos_begin) # all the rest


	def consume_number(self):
		""" Consume hex, bin or dec number.

		Returns:
			The number literal

		"""

		pos_begin = self.pos

		if self.matches(r'0x[0-9A-Fa-f]+'):
			# hexa
			self.consume(2)
			while self.pos < self.length:
				if self.matches(r'[0-9A-Fa-f]'):
					self.consume()
				else:
					break

		elif self.matches(r'0b[01]+'):
			# hexa
			self.consume(2)
			while self.pos < self.length:
				if self.matches(r'[01]'):
					self.consume()
				else:
					break

		elif self.matches(r'-?[0-9]+'):
			# decimal
			if self.starts('-'):
				self.consume()

			while self.pos < self.length:
				if self.matches(r'[0-9]'):
					self.consume()
				else:
					break

		else:
			self.error('Invalid number literal.')

		return self.from_pos(pos_begin) # whole number


	def consume_operator(self):
		""" Consume an operator.

		Returns:
			The operator

		"""

		# always single so just consume it
		# * / % ~ ^
		if self.matches(r'^[*/%~^]'):
			return self.consume()

		# long ones
		if self.matches(r'^(&&|\|\||<<|>>|>=|<=|==|!=|\+\+|--)'):
			return self.consume(2)

		# < > !
		if self.matches(r'[><!]'):
			return self.consume()

		# - + | &
		if self.matches(r'^[-+|&]'):
			return self.consume()

		self.error('Expected operator, found something else.')


	def consume_rvalue(self):
		""" Consume an rvalue - extended equals and expression.

		The rvalue can be terminated by either , or ;
		This terminator is not consumed.

		Returns:
			The rvalue

		"""

		buffer = ''

		if self.starts('='):
			buffer += self.consume()

		elif self.matches( self.RE_RVALUE_EXTENDED_EQUALS ):
			# extended equals
			buffer += self.consume_until('=') # consume it until the equals

		else:
			self.error('Expected equals or extended equals, found:'+self.peek(2))

		self.sweep()
		buffer += ' '
		buffer += self.consume_code(end=[';', ','], consume_end=False)

		return buffer


	def consume_identifier(self):
		""" Consume next identifier

		An identifier can be eg. a keyword, variable or function name.

		Returns:
			The identifier

		"""

		pos_begin = self.pos

		self.assert_matches(self.RE_IDENTIFIER);

		self.consume() # consume first char

		while self.pos < self.length:

			if self.matches(self.RE_IDENTIFIER_BODY):
				self.consume() # advance
			else:
				return self.from_pos(pos_begin) # not identifier char anymore

		return self.from_pos(pos_begin) # all the rest


	def has_char(self):
		""" Check if next token is a char literal """

		if self.has_end(): return False
		return self.matches( self.RE_CHAR_QUOTE )


	def has_string(self):
		""" Check if next token is a string literal """

		if self.has_end(): return False
		return self.matches( self.RE_STRING_QUOTE )


	def has_number(self):
		""" Check if next token is a number literal """

		if self.has_end():
			return False

		if self.matches(r'0x[a-fA-F0-9]+'):
			return True #hexa

		if self.matches(r'0x[01]+'):
			return True # bin

		if self.matches(r'-?[0-9]+'):
			return True # dec


	def has_operator(self):
		""" Check if next token is an operator """

		if self.has_end(): return False
		return self.matches(self.RE_OPERATOR)


	def has_inline_comment(self):
		""" Check if next token is a line comment """

		if self.has_end(): return False
		return self.starts(self.COMMENT)


	def has_block_comment(self):
		""" Check if next token is a block comment """

		if self.has_end(): return False
		return self.starts(self.COMMENT_OPEN)


	def has_identifier(self):
		""" Check if next token is an identifier
		(may also be keyword, not distinguished here)
		"""

		if self.has_end(): return False
		return self.matches(self.RE_IDENTIFIER)


	def has_label(self):
		""" Check if next token is a label """

		if self.has_end(): return False
		return self.matches(self.RE_LABEL)


	def has_paren(self):
		""" Check if next token is a parenthesis """
		if self.has_end(): return False
		return self.starts('(')


	def has_bracket(self):
		""" Check if next token is a bracket block (array index) """

		if self.has_end(): return False
		return self.starts('[')


	def has_code_block(self):
		""" Check if next token is a brace block (code block) """

		if self.has_end(): return False
		return self.starts('{')


	def has_rvalue(self):
		""" Check if next token is a RValue """

		if self.has_end():
			return False

		if self.starts('='):
			return True

		if self.matches(self.RE_RVALUE_EXTENDED_EQUALS):
			return True

		return False


	def has_end(self):
		""" Check if end of file was reached """
		return self.end_reached()
