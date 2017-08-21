#!/bin/env python3

import re
import os.path
import time
from collections import OrderedDict

from sdscp_errors import *
from readers import CodeReader
from tokens import Token, T_Paren, ParenType


class MacroReader(CodeReader):
	""" Code reader with support for directives

	Args:
		source (str): The source code
		filename (str, optional):
			The name of the file it came from.
			Defaults to None.

	Attributes:
		keep_macro_newlines (bool):
			Config option, whether to keep newlines in
			long macros.
		keep_macro_indent (bool):
			Config option, whether to keep indentation in
			multi-line macros.

	"""

	def __init__(self, source, filename=None):
		super().__init__(source, filename)

		# opts
		self.keep_macro_newlines = True
		self.keep_macro_indent = False


	def _consume_directive_name(self, name):
		""" Consume #<name>

		Args:
			name (str): Name of the consumed directive

		Returns:
			The consumed directive, including the #

		"""

		return self.consume_exact('#' + name)


	def _define_get_whitespace(self, j):
		""" Extract whitespace to keep, from j ("junk")

		Args:
			j (str): Junk (collected using `rd.sweep()`)

		Returns:
			replacement for the junk, based on config options.

		"""

		white = ''

		if self.keep_macro_newlines:

			if len(j) > 0:

				if j.count('\n') >= 2:
					white += '\n\n'

				elif j.count('\n') == 1:
					white += '\n'


				c = len(j) - 1

				if self.keep_macro_indent:
					while c >= 0 and j[c] in ' \t':
						white += j[c]
						c -= 1

		else:
			white = ' '

		return white


	def consume_define_directive(self):
		""" Consume a #define macro

		Filters out comments and useless whitespace, takes
		care of multi-line macros (with backslashes).

		Returns:
			The consumed and cleaned macro, complete with the #define.

		"""

		pos_begin = self.pos

		buffer = self._consume_directive_name('define')
		buffer += ' '
		self.consume_inline_whitespace()

		if not self.has_identifier():
			self.error('Missing identifier.')

		# macro identifier
		buffer += self.consume_identifier()

		# macro parameter list
		if self.has_paren():
			buffer += self.consume_block()
		elif self.has_bracket():
			buffer += self.consume_block()

		buffer += ' '

		trash = self.sweep()

		if trash.count('\n') > 0:
			# was no-body macro
			buffer += '1'  # add '1' as value
			return buffer

		# block macro - no need for annoying backslashes inside.
		if self.has_code_block():
			buffer += self.consume_block()
			self.sweep()
			return buffer

		buffer_before_backslash = buffer
		last_was_backslash = False

		while self.pos < self.length:

			if self.has_inline_comment():
				# consume comment
				j = self.sweep()
				white = self._define_get_whitespace(j)

				if last_was_backslash:
					buffer = buffer_before_backslash.strip() + white
					last_was_backslash = False
					continue
				else:
					return buffer.strip()

			if self.has_block_comment():

				j = self.sweep()

				white = self._define_get_whitespace(j)

				if j.count('\n') > 0:
					# was more lines

					if last_was_backslash:
						buffer = buffer_before_backslash.strip() + white
						last_was_backslash = False
				else:
					buffer += ' '

				continue

			char = self.peek()
			if char == '\\':
				buffer_before_backslash = buffer
				last_was_backslash = True

			elif re.match(r'[ \t]', char):  # whitespace except newline
				pass  # add to macro

			elif char == '\n':  # newline
				if last_was_backslash:
					last_was_backslash = False

					# new line of macro
					j = self.sweep()

					white = self._define_get_whitespace(j)

					buffer = buffer_before_backslash.strip() + white

					continue
				else:
					# end of macro
					return buffer.strip()
			else:
				# this char is valid but not backslash -> the backlash wasnt special
				last_was_backslash = False

			buffer += self.consume()  # advance to next char

		return self.from_pos(pos_begin)


	def consume_include_directive(self):
		""" consume a #include directive

		Returns:
			The #include directive.

		"""

		buffer = self._consume_directive_name('include')
		buffer += ' '
		self.consume_inline_whitespace()
		buffer += self.consume_string()

		return buffer


	def consume_pragma_directive(self):
		""" consume a #pragma directive

		Returns:
			The #pragma directive.

		"""

		buffer = self._consume_directive_name('pragma')

		buffer += ' '
		self.consume_inline_whitespace()

		buffer += self.consume_identifier()

		buffer += ' '
		self.consume_inline_whitespace()

		if self.has_identifier():
			buffer += self.consume_identifier()
		elif self.has_number():
			buffer += self.consume_number()
		elif self.has_string():
			buffer += self.consume_string()

		self.sweep()

		return buffer.strip()


	def consume_ifdef_directive(self):
		""" consume #ifdef

		Returns:
			The #ifdef directive.

		"""

		buffer = self._consume_directive_name('ifdef')
		buffer += ' '
		self.consume_inline_whitespace()
		buffer += self.consume_identifier()

		return buffer


	def consume_ifndef_directive(self):
		""" consume a #ifndef

		Returns:
			The #ifndef directive.

		"""

		buffer = self._consume_directive_name('ifndef')
		buffer += ' '
		self.consume_inline_whitespace()
		buffer += self.consume_identifier()

		return buffer


	def consume_else_directive(self):
		""" consume a #else directive

		Returns:
			The #else directive.

		"""

		if self.has_end():
			return False

		return self._consume_directive_name('else')


	def consume_endif_directive(self):
		""" consume a #endif directive

		Returns:
			The #endif directive.

		"""

		if self.has_end():
			return False

		return self._consume_directive_name('endif')


	def has_directive(self):
		""" Check if next token is a directive

		A directive is a # followed by an identifier.

		Returns:
			True if there is a directive.

		"""

		if self.has_end():
			return False

		return self.matches(r'^#[a-zA-Z_][a-zA-Z0-9_]+(?:[^a-zA-Z0-9_]|$)')


	def has_ifdef_directive(self):
		""" Check if next token is #ifdef """

		if self.has_end():
			return False

		return self.starts('#ifdef')


	def has_ifndef_directive(self):
		""" Check if next token is #ifndef """

		if self.has_end():
			return False

		return self.starts('#ifndef')


	def has_else_directive(self):
		""" Check if next token is #else """

		if self.has_end():
			return False

		return self.starts('#else')


	def has_endif_directive(self):
		""" Check if next token is #endif """

		if self.has_end():
			return False

		return self.starts('#endif')


	def has_include_directive(self):
		""" Check if next token is #include """

		if self.has_end():
			return False

		return self.starts('#include')


	def has_pragma_directive(self):
		""" Check if next token is #pragma """

		if self.has_end():
			return False

		return self.starts('#pragma')


	def has_define_directive(self):
		""" Check if next token is #define """

		if self.has_end():
			return False

		return self.starts('#define')


	def find_directive_block_end(self, can_else=True):
		""" Find #else or #endif position

		The current `pos` should be AFTER the opening
		directive (#ifdef / #ifndef / #else)

		Returns:
			pos at the beginning of the closing directive
			(at the #)

		"""

		pos_begin = self.pos

		nest = 0

		while not self.has_end():

			# print('At: %s' % re.sub(r'[\n\t ]+', ' ', self.peek(20)) )

			self.sweep()  # comments and whitespace

			if self.has_end():
				break

			if not self.has_directive():

				if self.has_string():
					self.consume_string()

				elif self.has_char():
					self.consume_char()

				else:
					self.consume()  # any char...

				continue

			else:
				if self.has_define_directive():
					self.consume_define_directive()

				elif self.has_include_directive():
					self.consume_include_directive()

				elif self.has_ifdef_directive():
					nest += 1
					self.consume_ifdef_directive()

					# skip to end
					self.pos = self.find_directive_block_end(can_else=True)


				elif self.has_ifndef_directive():
					nest += 1
					self.consume_ifndef_directive()

					# skip to end
					self.pos = self.find_directive_block_end(can_else=True)


				elif self.has_else_directive():

					if not can_else:
						self.error('Unexpected #else')

					if nest == 0:
						# found it
						pos = self.pos
						self.pos = pos_begin  # restore to previous pos
						return pos

					else:
						# leave nest unchanged
						# we just left one block and starting another
						self.consume_else_directive()

						# skip to end
						self.pos = self.find_directive_block_end(can_else=False)


				elif self.has_endif_directive():

					if nest == 0:
						# found it
						pos = self.pos
						self.pos = pos_begin  # restore to previous pos
						return pos

					else:
						nest -= 1
						self.consume_endif_directive()
						# go on

		self.error('Reached end of file while looking for end of # branch')



# helper tokens for use within define macro
class DT_Code:
	""" #define sub-token of a code fragment

	Args:
		text (str): The code fragment

	Attributes:
		text (str): The code fragment is stored here

	"""

	def __init__(self, text):
		self.text = text


	def __str__(self):
		return 'DT_Code: ' + self.text



class DT_Var:
	""" #define sub-token of an argument occurence

	Args:
		name (str): The argument name

	Attributes:
		name (str): The name is stored here

	"""

	def __init__(self, name):
		self.name = name


	def __str__(self):
		return 'DT_Var: ' + self.name



class D_Define(Token):
	""" The #define directive

	#define name(args) body

	Takes care of parsing the macro and generating a replacement.

	Args:
		value (str): The macro source (#define ... )

	Attributes:
		name (str): The macro name
		arraylike (bool):
			True if this macro is array-like (square brackets)
		functionlike (bool):
			True if this macro is function-like
		args (str[]):
			List of argument names, None for constant macros
		vararg_pos:
			Index of argument that is variadic.
			None if there is no such argument.
		tokens:
			#define sub-tokens.
			Used to generate the replacements.

	"""


	def __init__(self, value):
		super().__init__(value)

		rd = CodeReader(value)
		rd.consume_exact('#define')
		rd.consume_inline_whitespace()

		# get macro name
		self.name = rd.consume_identifier()

		# arraylike flag
		self.arraylike = False
		self.functionlike = False

		# macro arguments
		self.args = None

		# which argument is variadic
		self.vararg_pos = None

		#print(str(rd.has_bracket()))

		if rd.has_paren():
			tmp = rd.consume_block()[1:-1]  # inside the paren
			self.args = []
			for a in tmp.split(','):
				a = a.strip()
				if len(a) > 0:

					if a[-3:] == '...':
						# a is a variadic argument

						if self.vararg_pos is not None:
							rd.error('Macro can have only one variadic argument!')

						self.vararg_pos = len(self.args)
						a = a[:-3].strip()

					self.args.append(a)

			self.functionlike = True

		elif rd.has_bracket():
			tmp = rd.consume_block()[1:-1].strip()  # inside the bracket

			if not re.match(r'\A[a-zA-Z_][a-zA-Z0-9_]*\Z', tmp):
				rd.error('Invalid argument format for macro "%s": %s' % (self.name, tmp))

			self.args = [tmp]
			self.arraylike = True


		rd.consume_inline_whitespace()

		# macro body
		self.body = rd.consume_all()

		# macro body tokens
		self.tokens = []

		self.__parse_body()


	def __parse_body(self):
		""" parse macro content, store subtokens """

		if self.args is None:
			self.tokens.append( DT_Code(self.body) )
		else:
			rd = CodeReader(self.body)
			buff = ''
			while not rd.has_end():
				if rd.has_identifier():
					ident = rd.consume_identifier()

					# check if macro argument
					if ident in self.args:

						# append collected code fragment
						if len(buff) > 0:
							t = DT_Code(buff)
							buff = ''
							self.tokens.append(t)

						# append the var
						t = DT_Var(ident)
						self.tokens.append(t)

					else:
						buff += ident

				elif rd.has_string():
					buff += rd.consume_string()

				elif rd.has_char():
					buff += rd.consume_char()

				else:
					# just add the character to the currently built DT_Code
					buff += rd.consume()

			# add trailing code fragment
			if len(buff) > 0:
				t = DT_Code(buff)
				buff = ''
				self.tokens.append(t)


	def __str__(self):

		s = 'MACRO: %s' % self.name

		if self.args is None:
			s += ' '
		elif self.arraylike:
			s += '[%s] ' % self.args[0]
		else:
			s += '('
			n=0
			for a in self.args:
				if n > 0:
					s += ', '
				s += a
				if self.vararg_pos == n:
					s += '...'
				n += 1
			s += ') '


		if len(s) < 30:
			s = (s + '.'*35)[:35]
		else:
			s += '...'

		s += ' %s' % self.body

		return s


	def is_arraylike(self):
		""" Get if this macro is array-like (bool) """

		return self.arraylike


	def is_functionlike(self):
		""" Get if this macro is function-like (bool) """

		return self.functionlike


	def is_constant(self):
		""" Get if this macro is constant (bool) """

		return (not self.functionlike) and not (self.arraylike)


	def can_use_args(self, args):
		""" Check if this macro ca work with the given arguments

		Args:
			args (str[]):
				List of arguments to check against.
				Can be Null for use without parentheses (const)

		Returns:
			True if the macro is compatible with the arguments.

		"""

		if (self.args is None) != (args is None):
			return False

		if self.args is not None:

			if self.vararg_pos is None:
				if len(self.args) != len(args):
					return False
			else:
				if len(self.args)-1 > len(args):  # variadic arg can be missing
					return False

		return True


	def equals_signature(self, other):
		""" Test for signature equality

		Compare macro parameters to other macro, test whether
		the other replaces this one.

		Args:
			other (D_Define): Other macro

		Returns:
			True if they are equal in type and attribute count.

		"""

		# the name must be the same
		if self.name != other.name:
			return False

		if (self.args is None) != (other.args is None):
			# one has args and the other not
			return False

		if self.args is not None:

			if len(self.args) != len(other.args):
				# differ in number of args
				return False

			if self.arraylike != other.arraylike:
				return False

			if self.vararg_pos != other.vararg_pos:
				# which argument is variadic
				return False

		if self.functionlike != other.functionlike:
			return False

		return True


	def generate(self, args=None):
		""" Generate replacement for given arguments

		Args:
			args (str[]): List of arguments,
				can be None for const macro.

		Returns:
			code that replaces the macro occurence.

		"""

		if not self.can_use_args(args):
			raise SdscpSyntaxError('Macro %s cannot be used with arguments %s!' % (self.name, ','.join(args)) )


		# no-args macro
		if self.args is None:
			return self.tokens[0].text


		# argument->value map
		a2v = {}

		if self.vararg_pos is None:
			for i in range(0, len(self.args)):
				a2v[ self.args[i] ] = args[i]
		else:

			pre_from = 0
			pre_to = self.vararg_pos

			va_from = pre_to
			va_to = len(args)-(len(self.args) - self.vararg_pos) +1

			post_from = va_to
			post_to = len(args)

			for i in range(pre_from, pre_to):
				a2v[ self.args[i] ] = args[i]

			va = []
			for i in range(va_from, va_to):
				va.append(args[i])
			a2v[ self.args[self.vararg_pos] ] = ', '.join(va)

			# print( 'VA: %s' % (','.join(va)) )

			for i in range(post_from, post_to):
				a2v[ self.args[i-len(va)+1] ] = args[i]

		generated = ''

		for dt in self.tokens:
			if not isinstance(dt, DT_Var):
				generated += dt.text
			else:
				va_empty_done = False

				if self.vararg_pos is not None and dt.name == self.args[self.vararg_pos]:
					# this is variadic argument

					if re.match(r'.*,\s*##\s*\Z', generated, re.S):
						# preceded by a concatenation operator

						if len(a2v[dt.name].strip()) == 0:
							# empty
							generated = generated[:generated.rindex(',')] # remove since last comma
							va_empty_done = True
						else:
							generated = generated[:generated.rindex('#')-1] # just remove the ##

				if not va_empty_done:
					generated += a2v[dt.name]

		return generated



class D_Include(Token):
	""" #include directive

	Args:
		value (str): The directive code

	Attributes:
		file (str): The included filename.

	"""

	def __init__(self, value):
		super().__init__(value)

		rd = CodeReader(value)
		rd.consume_exact('#include')
		rd.consume_inline_whitespace()

		# get file (discard quotes)
		self.file = rd.consume_string()[1:-1]


	def __str__(self):
		return type(self).__name__ + ': File = ' + self.file



class D_Ifdef(Token):
	""" #ifdef directive

	Args:
		value (str): The directive code

	Attributes:
		name (str): Name of the tested macro (the condition)

	"""

	def __init__(self, value):
		super().__init__(value)

		rd = CodeReader(value)
		rd.consume_exact('#ifdef')
		rd.consume_inline_whitespace()

		self.name = rd.consume_identifier()


	def __str__(self):
		return type(self).__name__ + ': Name = ' + self.name



class D_Ifndef(Token):
	""" #ifndef directive

	Args:
		value (str): The directive code

	Attributes:
		name (str): Name of the tested macro (the condition)

	"""

	def __init__(self, value):
		super().__init__(value)

		rd = CodeReader(value)
		rd.consume_exact('#ifndef')
		rd.consume_inline_whitespace()

		self.name = rd.consume_identifier()


	def __str__(self):
		return type(self).__name__ + ': Name = ' + self.name



class D_Pragma(Token):
	""" #pragma directive

	Args:
		value (str): The directive code

	Attributes:
		name (str): Name of the option
		value (mixed): Value for the option

	"""

	def __init__(self, value):
		super().__init__(value)

		rd = CodeReader(value)
		rd.consume_exact('#pragma')
		rd.consume_inline_whitespace()
		self.name = rd.consume_identifier()
		rd.consume_inline_whitespace()

		if rd.has_identifier():
			self.value = rd.consume_identifier()  # identifier without quotes

		elif rd.has_number():

			n = rd.consume_number()

			try:
				self.value = int(n, 10)
			except ValueError:
				try:
					self.value = int(n, 16)
				except ValueError:
					try:
						self.value = int(n, 2)
					except ValueError:
						rd.error('Could not parse number: %s' % n)

		elif rd.has_string():
			self.value = rd.consume_string()[1:-1]  # crop quotes

		else:
			self.value = True  # boolean directive (flag)

		v = self.value
		if type(v) is str:
			self.value = {'true': True, 'false': False}.get(v.lower(), v)


	def __str__(self):
		return '%s: %s = %s' % (type(self).__name__, self.name, self.value)



def _load_file(filename):
	""" Load a file to string

	Args:
		filename (str): The file path to load

	"""

	with open(filename, 'r') as f:
		text = f.read()
		return text



class DirectiveProcessor:
	""" Macro processor

	Interprets and evaluates macros in a source file,
	producing a clean output source code.

	Args:
		main_file (str): The main source file to load
		injected_pragmas (dict): Injected pragmas via command line (name: value)

	Attributes:
		main_file (str): The main file path
		source (str): Text of the main file
		output (str): The output source code
		defines:
			Storage of defined macros.

			It is a dict {"name" -> D_Define[]}, where the list
			contains variants of the macro (overloading)

		pragmas (dict):
			Dict of pragma keys and values

		keep_comments:
			Config option, whether to keep comments in the source code.

	"""

	def __init__(self, main_file, injected_pragmas = None):
		self.main_file = main_file
		self.source = _load_file(main_file)
		self.output = ''
		self.defines = OrderedDict()
		self.keep_comments = True

		self.pragmas = {}

		if injected_pragmas is not None:
			self.pragmas.update(injected_pragmas)
			self.add_defines_for_pragmas(injected_pragmas)

		self.files_once = []  # list of files included with pragma once

		self.defines['__TIME__'] = [D_Define('#define __TIME__ "%s"' % time.strftime("%H:%M:%S"))]
		self.defines['__DATE__'] = [D_Define('#define __DATE__ "%s"' % time.strftime("%b %d %Y"))]

	def add_defines_for_pragmas(self, pragmas):
		for (name, value) in pragmas.items():
			# we add the pragma to defines for use inline as __PRAGMANAME__
			defname = '__%s__' % name.upper()
			d2 = D_Define(
				'#define %s %s' % (defname, value) if isinstance(value, int) or isinstance(value, float) else
				'#define %s "%s"' % (defname, value.replace('"', '\\"'))
				)
			if not defname in self.defines:
				self.defines[defname] = []
			self.defines[defname].append(d2)

	def add_defines(self, new_defines):
		""" Add extra defines to the processor

		If any of the current defines

		Args:
			new_defines: Dict of defines, in the same format as the
				self.defines dict.

		"""

		for (name, macros) in new_defines.items():
			#print('macro name %s' % name)
			if not name in self.defines:

				self.defines[name] = []
				for new_m in macros:
					self.defines[name].append(new_m)

			else:
				#print(new_defines[name])

				# merge
				for new_m in macros:
					#print(new_m)
					self.defines[name].insert(0, new_m)

				# remove duplicates from the list
				for i in range(0, len(self.defines[name]) ):
					for j in range(len(self.defines[name])-1, i, -1):
						if self.defines[name][i].equals_signature( self.defines[name][j] ):
							del self.defines[name][j]


	def get_defines(self):
		""" Get defines

		Returns:
			The dict of defines

		"""

		return self.defines


	def get_output(self):
		""" Get the result of process()

		process() must be called first, otherwise you will get None.

		Returns:
			result of process()

		"""

		return self.output


	def _handle_whitespace(self, rd):
		out = ''
		# handle whitespace
		if self.keep_comments:
			# keep comments, indentation and up to two newlines (at once)
			j = rd.sweep()
			if len(j) > 0:
				out += re.sub(r'\n{2,}', '\n\n', j)

		else:
			# keep up to two newlines and indentation
			j = rd.sweep()
			if len(j) > 0:
				if j.count('\n') >= 2:
					out += '\n\n'

				elif j.count('\n') == 1:
					out += '\n'

				c = len(j)-1
				while c >= 0 and j[c] in ['\t', ' ']:
					out += j[c]
					c -= 1

		return out


	def process(self):
		""" Extract all directives and resolve the # branching.

		Keeps the produced code in `self.output`, and all
		macros in the `self.defines` dict.

		Returns:
			The produced code (before replacing macros)

		"""

		rd = MacroReader(self.source, self.main_file)
		self.built = ''

		# list of skip directions
		# used in conditional branching (#ifdef)
		skip_dict = {}

		out = ''

		while not rd.has_end():

			out += self._handle_whitespace(rd)
			if rd.has_end():
				break

			# jump false # branches
			if rd.pos in skip_dict:

				from_pos = rd.pos
				to_pos = skip_dict[rd.pos]

				from_l = rd.pos2line(from_pos)
				from_c = rd.pos2col(from_pos)

				to_l = rd.pos2line( to_pos )
				to_c = rd.pos2col( to_pos )

				print('=== JUMP in file "%s":  %d:%d --> %d:%d ===' % (self.main_file, from_l, from_c, to_l, to_c))
				rd.pos =  skip_dict[rd.pos]
				continue

			# #define - add a new macro
			if rd.has_define_directive():

				s = rd.consume_define_directive()
				d = D_Define(s)
				if not d.name in self.defines:
					self.defines[d.name] = []

				self.defines[d.name].append(d)

			# #define - add a new macro
			elif rd.has_pragma_directive():

				s = rd.consume_pragma_directive()
				d = D_Pragma(s)

				if d.name == 'once':
					self.files_once.append(self.main_file)
				else:
					if d.name in self.pragmas.keys():
						if not self.pragmas[d.name] == d.value:
							raise SdscpSyntaxError(
								'Cannot overwrite pragma "%s" (old "%s", new "%s")'
								% (
									d.name,
									self.pragmas[d.name],
									d.value
								))

					self.pragmas[d.name] = d.value
					
					self.add_defines_for_pragmas({d.name: d.value})


			# #include - include external file
			elif rd.has_include_directive():

				s = rd.consume_include_directive()
				d = D_Include(s)

				if not os.path.isfile(d.file):
					ff = os.path.join(os.path.dirname(self.main_file), d.file)
					if not os.path.isfile(ff):
						raise SdscpSyntaxError('Could not find included file: %s (nor %s)' % (d.file, ff))
					else:
						d.file = ff

				if d.file in self.files_once:
					# print('skipping %s (#pragma once)' % d.file)
					continue  # end this cycle

				print('including %s' % d.file)

				# create a nested macro processor
				mp = DirectiveProcessor(d.file)

				mp.files_once = self.files_once
				mp.pragmas = self.pragmas
				mp.defines = self.defines  # reference

				# # inject current defines
				# mp.add_defines(self.defines)

				# process the external file
				mp.process()

				out += mp.get_output()

				# # add back defines collected from the external file
				# self.add_defines( mp.get_defines() )


			# #ifdef
			elif rd.has_ifdef_directive() or rd.has_ifndef_directive():

				positive = rd.has_ifdef_directive()

				if positive:
					s = rd.consume_ifdef_directive()
					d = D_Ifdef(s)
				else:
					s = rd.consume_ifndef_directive()
					d = D_Ifndef(s)

				defined = (d.name in self.defines)
				if defined:
					found = False

					# print(','.join([str(m) for m in self.defines[d.name]]))

					for m in self.defines[d.name]:
						if m.is_constant():
							defined = (m.body != '0')
							found = True
							break

					if not found:
						print('[W] Macro %s is not constant.' % (d.name) )
						defined = False

					# print('- Checking # condition: %s is %s' % (d.name, [0,1][defined]) )

				if positive == defined:
					# is defined

					# remember current pos
					pp = rd.pos

					# let's find the end of this branch
					endpos = rd.find_directive_block_end()
					rd.pos = endpos

					if rd.has_endif_directive():
						# there is no else branch to skip
						rd.pos = pp # back to saved pos
						continue

					elif rd.has_else_directive():
						# found start of else branch to skip
						rd.consume_else_directive()

						# find where the else ends
						endpos2 = rd.find_directive_block_end()

						# remember where to skip
						skip_dict[endpos] = endpos2

						rd.pos = pp # back to saved pos
						continue
					else:
						rd.error('Wtf?')

				else:
					# cond not met
					endpos = rd.find_directive_block_end()
					rd.pos = endpos

					# consume the directive
					if rd.has_else_directive():
						rd.consume_else_directive()
					else:
						rd.consume_endif_directive()

					continue

			# #else
			elif rd.has_else_directive():
				rd.error('Unexpected #else')  # is consumed in jump -> cant be here

			# #endif
			elif rd.has_endif_directive():
				rd.consume_endif_directive()  # probably due to jump

			# "..."
			elif rd.has_string():
				out += rd.consume_string()

			# //...
			elif rd.has_inline_comment():
				rd.consume_line()

			# /* ... */
			elif rd.has_block_comment():
				rd.consume_block_comment()

			# any char...
			else:
				out += rd.consume()

		out = out.strip()

		self.output = out

		return out


	def apply_macros(self):
		""" Recursively apply macros to the output of `process()`

		To be called after `process()`.
		The `output` variable is overwritten by this.

		Returns:
			The final source code after applying all
			macro replacements.

		"""

		if len(self.output) == 0:
			print('There is no source code.')
			return

		rd = CodeReader(self.output)

		applied_count = 0
		out = ''
		while not rd.has_end():

			out += self._handle_whitespace(rd)
			if rd.has_end():
				break

			if rd.has_identifier():

				ident = rd.consume_identifier()
				ident_whitesp = rd.consume_inline_whitespace()

				if ident in self.defines:

					macros = self.defines[ident]

					replacement = None

					if rd.has_bracket():
						# array macro

						bracket = rd.consume_block()[1:-1]

						for mm in macros:
							if mm.is_arraylike():
								if mm.can_use_args([bracket]):
									replacement = mm.generate([bracket])
									break

						if replacement is None:
							out += ident + ident_whitesp
							out += '[%s]' % bracket
						else:
							out += replacement
							applied_count += 1

					elif rd.has_paren():
						# func macro

						paren = rd.consume_block()

						t = T_Paren(paren)
						t.set_type(ParenType.ARGVALS)
						t.tokenize()

						args = []
						for a in t.tokens:
							args.append(a.value)

						# print(args)

						for mm in macros:
							if mm.is_functionlike():
								if mm.can_use_args(args):
									replacement = mm.generate(args)
									break

						if replacement is None:
							out += ident + ident_whitesp + paren
							print(
								'[W] Macro "%s" defined, but can\'t use arguments (%s)'
								% (ident, ', '.join(args) ))
						else:
							out += replacement
							applied_count += 1

					else:
						# const macro

						for mm in macros:
							if mm.can_use_args(None):
								replacement = mm.generate(None)
								break

						if replacement is None:
							out += ident + ident_whitesp
						else:
							out += replacement + ident_whitesp
							applied_count += 1

				else:
					out += ident + ident_whitesp  # give it back

			# "...", and "sdgfsd""JOINED"  "This too"
			elif rd.has_string():
				# handle string concatenation
				s = ''
				while rd.has_string():
					s += rd.consume_string()[1:-1]  # drop quotes
					rd.sweep()

				out += '"%s"' % s

			# //...
			elif rd.has_inline_comment():
				rd.consume_line()

			# /* ... */
			elif rd.has_block_comment():
				rd.consume_block_comment()

			# any char...
			else:
				out += rd.consume()

		self.output = out

		# take care of macros in macros
		if applied_count > 0:
			return self.apply_macros()
		else:
			return out


	def get_pragmas(self):
		""" Get dict of collected pragmas """

		return self.pragmas
