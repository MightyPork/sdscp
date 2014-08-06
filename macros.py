#!/bin/env python3

import re
from readers import CodeReader
from tokens import Token, T_Paren, ParenType
import os.path
from collections import OrderedDict


class MacroReader(CodeReader):
	""" Code reader with support for directives """

	# opts
	keep_macro_newlines = True
	keep_macro_indent = False

	def _consume_directive_name(self, name):
		""" Consume #<name> """
		return self.consume_exact('#'+name)


	def __define_get_whitespace(self, j):
		""" Extract whitespace to keep, from j ("junk") """

		white = ''

		if self.keep_macro_newlines:

			if len(j) > 0:

				if j.count('\n') >= 2:
					white += '\n\n'

				elif j.count('\n') == 1:
					white += '\n'


				c = len(j)-1

				if self.keep_macro_indent:
					while c >= 0 and j[c] in ['\t', ' ']:
						white += j[c]
						c -= 1

		else:
			white = ' '

		return white



	def consume_define_directive(self):
		""" consume a #define macro """

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
			buffer += '1' # add '1' as value
			return buffer

		buffer_before_backslash = buffer
		last_was_backslash = False

		while self.pos < self.length:

			if self.has_inline_comment():
				# consume comment
				j = self.sweep()
				white = self.__define_get_whitespace(j)

				if last_was_backslash:
					buffer = buffer_before_backslash.strip() + white
					last_was_backslash = False
					continue
				else:
					return buffer.strip()


			if self.has_block_comment():

				j = self.sweep()

				white = self.__define_get_whitespace(j)

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

			elif re.match(r'[ \t]', char): # whitespace except newline
				pass # add to macro

			elif char == '\n': # newline
				if last_was_backslash:
					last_was_backslash = False

					# new line of macro
					j = self.sweep()

					white = self.__define_get_whitespace(j)

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
		""" consume a #include directive """

		buffer = self._consume_directive_name('include')
		buffer += ' '
		self.consume_inline_whitespace()
		buffer += self.consume_string()

		return buffer



	def consume_ifdef_directive(self):
		""" consume #ifdef """

		buffer = self._consume_directive_name('ifdef')
		buffer += ' '
		self.consume_inline_whitespace()
		buffer += self.consume_identifier()

		return buffer



	def consume_ifndef_directive(self):
		""" consume a #ifndef """

		buffer = self._consume_directive_name('ifndef')
		buffer += ' '
		self.consume_inline_whitespace()
		buffer += self.consume_identifier()

		return buffer



	def consume_else_directive(self):
		""" consume a #else directive """

		if self.has_end():
			return False

		return self._consume_directive_name('else')



	def consume_endif_directive(self):
		""" consume a #endif directive """

		if self.has_end():
			return False

		return self._consume_directive_name('endif')



	def has_directive(self):
		""" Check if next token is #<something> """

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



	def has_define_directive(self):
		""" Check if next token is #define """

		if self.has_end():
			return False

		return self.starts('#define')


	def find_directive_block_end(self, can_else=True):
		""" Find #else or #endif position """

		pos_begin = self.pos

		nest = 0

		while not self.has_end():

			# print('At: %s' % re.sub(r'[\n\t ]+', ' ', self.peek(20)) )

			self.sweep() # comments and whitespace

			if self.has_end():
				break

			if not self.has_directive():

				if self.has_string():
					self.consume_string()

				elif self.has_char():
					self.consume_char()

				else:
					self.consume() # any char...

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
						self.pos = pos_begin # restore to previous pos
						return pos

					else:
						# leave nest unchanged
						# we just left one block and starting another
						self.consume_else_directive()

						# skip to end
						self.pos = self.find_directive_block_end(can_else = False)


				elif self.has_endif_directive():

					if nest == 0:
						# found it
						pos = self.pos
						self.pos = pos_begin # restore to previous pos
						return pos

					else:
						nest -= 1
						self.consume_endif_directive()
						# go on


		self.error('Reached end of file while looking for end of # branch')




# helper tokens for use within define macro
class DT_Code:
	""" Define macro code fragment sub-token """
	def __init__(self, text):
		self.text = text

	def is_var(self):
		return False

	def __str__(self):
		return 'DT_Code: ' + self.text





class DT_Var:
	""" Define macro argument-occurence sub-token """

	def __init__(self, name):
		self.name = name

	def is_var(self):
		return True

	def __str__(self):
		return 'DT_Var: ' + self.name





class D_Define(Token):
	""" #define name(args) body """


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
			tmp = rd.consume_block()[1:-1] # inside the paren
			self.args = []
			for a in tmp.split(','):
				a = a.strip()
				if len(a) > 0:

					if a[-3:] == '...':
						# a is a variadic argument

						if self.vararg_pos != None:
							rd.error('Macro can have only one variadic argument!')

						self.vararg_pos = len(self.args)
						a = a[:-3].strip()

					self.args.append(a)

			self.functionlike = True

		elif rd.has_bracket():
			tmp = rd.consume_block()[1:-1].strip() # inside the bracket

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
		""" parse macro content """

		if self.args == None:
			self.tokens.append( DT_Code(self.body) )
		else:
			rd = CodeReader(self.body)
			buff = ''
			while not rd.has_end():
				if rd.has_identifier():
					tmp = rd.consume_identifier()

					# check if macro argument
					if tmp in self.args:

						# append collected code fragment
						if len(buff) > 0:
							t = DT_Code(buff)
							buff = ''
							self.tokens.append(t)

						# append the var
						t = DT_Var(tmp)
						self.tokens.append(t)

					else:
						buff += tmp

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

		if self.args == None:
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
		""" Get if this macro is array-like """

		return self.arraylike


	def is_functionlike(self):
		""" Get if this macro is function-like """

		return self.functionlike


	def is_constant(self):
		""" Get if this macro is constant """

		return (not self.functionlike) and not (self.arraylike)


	def can_use_args(self, args):
		""" Check if this macro could be used with the given arguments """

		if (self.args == None) != (args == None):
			return False

		if self.args != None:

			if self.vararg_pos == None:
				if len(self.args) != len(args):
					return False
			else:
				if len(self.args)-1 > len(args): # variadic arg can be missing
					return False

		return True



	def equals_signature(self, other):
		""" Check if this macro can seamlessly substitute another macro """

		# the name must be the same
		if self.name != other.name:
			return False

		if (self.args == None) != (other.args == None):
			# one has args and the other not
			return False

		if self.args != None:

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
		""" Generate replacement for given arguments """

		if not self.can_use_args(args):
			raise Exception('Macro %s cannot be used with arguments %s!' % (self.name, ','.join(args)) )


		# no-args macro
		if self.args == None:
			return self.tokens[0].text


		# argument->value map
		a2v = {}

		if self.vararg_pos == None:
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
			if not dt.is_var():
				generated += dt.text
			else:
				va_empty_done = False

				if self.vararg_pos != None and dt.name == self.args[self.vararg_pos]:
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
	""" #include "file" """

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
	""" #ifdef NAME """

	def __init__(self, value):
		super().__init__(value)

		rd = CodeReader(value)
		rd.consume_exact('#ifdef')
		rd.consume_inline_whitespace()

		self.name = rd.consume_identifier()

	def __str__(self):
		return type(self).__name__ + ': Name = ' + self.name



class D_Ifndef(Token):
	""" #ifndef NAME """

	def __init__(self, value):
		super().__init__(value)

		rd = CodeReader(value)
		rd.consume_exact('#ifndef')
		rd.consume_inline_whitespace()

		self.name = rd.consume_identifier()

	def __str__(self):
		return type(self).__name__ + ': Name = ' + self.name



def _load_file(filename):
	""" load a file """

	f = open(filename, 'r')
	text = f.read()
	f.close()
	return text


class MacroProcessor:
	""" Macro processor """

	def __init__(self, main_file):
		self.main_file = main_file
		self.source = _load_file(main_file)
		self.output = ''
		self.defines = OrderedDict()
		self.keep_comments = True



	def add_defines(self, new_defines):
		""" Add extra defines to the processor """

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
		""" Get defines """

		return self.defines



	def get_output(self):
		""" Get the result of process() """

		return self.output


	def __handle_whitespace(self, rd):
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
		""" Process all the directives in the source """

		rd = MacroReader(self.source, self.main_file)
		self.built = ''

		# list of skip directions
		# used in conditional branching (#ifdef)
		skip_dict = {}

		out = ''

		while not rd.has_end():

			out += self.__handle_whitespace(rd)
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
				rd.move_to( skip_dict[rd.pos] )
				continue


			# #define - add a new macro
			if rd.has_define_directive():

				s = rd.consume_define_directive()
				d = D_Define(s)
				if not d.name in self.defines:
					self.defines[d.name] = []

				self.defines[d.name].append(d)


			# #include - include external file
			elif rd.has_include_directive():

				s = rd.consume_include_directive()
				d = D_Include(s)

				if not os.path.isfile(d.file):
					ff = os.path.join(os.path.dirname(self.main_file), d.file)
					if not os.path.isfile(ff):
						raise Exception('Could not find file: %s (nor %s)' % (d.file, ff))
					else:
						d.file = ff


				print('including %s' % d.file)

				# create a nested macro processor
				mp = MacroProcessor(d.file)

				# inject current defines
				mp.add_defines(self.defines)

				# process the external file
				mp.process()
				out += mp.get_output()

				# add back defines collected from the external file
				self.add_defines( mp.get_defines() )


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

					print('- Checking # condition: %s is %s' % (d.name, [0,1][defined]) )

				if positive == defined:
					# is defined

					# remember current pos
					pp = rd.get_pos()

					# let's find the end of this branch
					endpos = rd.find_directive_block_end()
					rd.move_to(endpos)

					if rd.has_endif_directive():
						# there is no else branch to skip
						rd.move_to(pp) # back to saved pos
						continue

					elif rd.has_else_directive():
						# found start of else branch to skip
						rd.consume_else_directive()

						# find where the else ends
						endpos2 = rd.find_directive_block_end()

						# remember where to skip
						skip_dict[endpos] = endpos2

						rd.move_to(pp) # back to saved pos
						continue
					else:
						rd.error('Wtf?')

				else:
					# cond not met
					endpos = rd.find_directive_block_end()
					rd.move_to(endpos)

					# consume the directive
					if rd.has_else_directive():
						rd.consume_else_directive()
					else:
						rd.consume_endif_directive()

					continue


			# #else
			elif rd.has_else_directive():
				rd.error('Unexpected #else') # is consumed in jump -> cant be here


			# #endif
			elif rd.has_endif_directive():
				rd.consume_endif_directive() # probably due to jump


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



	def apply_macros(self):
		""" Apply macros in the output """

		if len(self.output) == 0:
			print('There is no source code.')
			return

		applied_count = 0

		rd = CodeReader(self.output)

		out = ''

		while not rd.has_end():

			out += self.__handle_whitespace(rd)
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

						if replacement == None:
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

						if replacement == None:
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

						if replacement == None:
							out += ident + ident_whitesp
						else:
							out += replacement + ident_whitesp
							applied_count += 1

				else:
					out += ident + ident_whitesp # give it back

			# "...", and "sdgfsd""JOINED"  "This too"
			elif rd.has_string():
				# handle string concatenation
				s = ''
				while rd.has_string():
					s += rd.consume_string()[1:-1] # drop quotes
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
