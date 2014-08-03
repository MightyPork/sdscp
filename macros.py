#!/bin/env python3

import re
from readers import CodeReader
from tokens import Token, T_Paren, ParenType
import os.path


class MacroReader(CodeReader):
	""" Code reader with support for directives """

	def _consume_directive_name(self, name):
		""" Consume #<name> """
		return self.consume_exact('#'+name)



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

		buffer += ' '

		trash = self.consume_non_code()

		if trash.count('\n') > 0:
			# was no-body macro
			buffer += '1' # add '1' as value
			return buffer

		buffer_before_backslash = buffer
		last_was_backslash = False

		while self.pos < self.length:

			if self.has_inline_comment():
				# consume comment
				self.consume_non_code()

				if last_was_backslash:
					buffer = buffer_before_backslash.strip() + ' '
					last_was_backslash = False
					continue
				else:
					return buffer


			if self.has_block_comment():
				trash = self.consume_non_code()
				if trash.count('\n') > 0:
					# was more lines

					if last_was_backslash:
						buffer = buffer_before_backslash.strip() + ' '
						last_was_backslash = False

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
					self.consume_non_code()
					buffer = buffer_before_backslash.strip() + ' '

					continue
				else:
					# end of macro
					return buffer
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

		return self.matches(r'#[a-zA-Z][a-zA-Z_]+(?:[^a-zA-Z_]|$)')



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

		self.save_pos()

		nest = 0

		while not self.has_end():

			# print('At: %s' % re.sub(r'[\n\t ]+', ' ', self.peek(20)) )

			self.consume_non_code() # comments and whitespace

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
					nest += 1
					self.consume_define_directive()

				elif self.has_include_directive():
					nest += 1
					self.consume_define_directive()

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
						self.undo() # restore to previous pos
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
						self.undo() # restore to previous pos
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

		# macro parameters
		self.args = None

		if rd.has_paren():
			tmp = rd.consume_block()[1:-1] # inside the paren
			self.args = [i.strip() for i in tmp.split(',')] # trim whitespace from arguments

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
		return type(self).__name__ + \
			': Name = ' + self.name + \
			', Args = ' + str(self.args) + \
			', Body = ' + self.body


	def generate(self, arguments=None):

		if self.args == None:
			if arguments != None:
				raise Exception('Macro %s is not function-like, cannot call with ()!')

			return self.tokens[0].text

		# ensure not None
		if arguments == None:
			arguments = []

		if len(self.args) != len(arguments):
			raise Exception('Macro %s takes %d arguments, %d given! (%s)'
				% (self.name, len(self.args), len(arguments), ','.join(arguments) ))


		# argument->value map
		a2v = {}

		for i in range(0, len(self.args)):
			a2v[ self.args[i] ] = arguments[i]

		generated = ''

		for dt in self.tokens:
			if not dt.is_var():
				generated += dt.text
			else:
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


class D_Else(Token): pass

class D_Endif(Token): pass



def _load_file(filename):
	""" load a file """

	f = open(filename, 'r')
	text = f.read()
	f.close()
	return text


def _show_tokenlist(tokens, level='\t'):
	for tok in tokens:

		print(level + str(tok))

		if tok.is_composite():
			_show_tokenlist(tok.tokenize(), level+'\t')




class MacroProcessor:
	""" Macro processor """

	def __init__(self, main_file):
		self.main_file = main_file
		self.source = _load_file(main_file)
		self.output = ''
		self.defines = {}



	def add_defines(self, new_defines):
		""" Add extra defines to the processor """

		self.defines.update( new_defines )



	def get_defines(self):
		""" Get defines """

		return self.defines



	def get_output(self):
		""" Get the result of process() """

		return self.output


	def apply_macros(self):
		""" Apply macros in the output """

		if len(self.output) == 0:
			raise Exception('There\'s no text to work with. Did you run process()?')

		applied_count = 0

		rd = CodeReader(self.output)

		out = ''

		while not rd.has_end():

			junk = rd.consume_non_code()
			if len(junk) > 0:
				if junk.count('\n') > 0:
					out += '\n'
				else:
					out += ' '
				continue

			if rd.has_identifier():

				rd.save_pos()
				ident = rd.consume_identifier()
				if ident in self.defines:

					macro = self.defines[ident]
					applied_count += 1

					try:
						if rd.has_paren():
							paren = rd.consume_block()

							t = T_Paren(paren)
							t.set_type(ParenType.ARGS)
							t.tokenize()

							args = []
							for a in t.tokens:
								args.append(t.value)

							replacement = macro.generate(args)
						else:
							replacement = macro.generate(None)
					except Exception as e:
						rd.undo() # rewind to the identifier
						rd.error(str(e))


					out += replacement

				else:
					out += ident # give it back

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

		self.output = out


		# take care of macros in macros
		if applied_count > 0:
			return self.apply_macros()



	def process(self):
		""" Process all the macros in the source """

		rd = MacroReader(self.source, self.main_file)
		self.built = ''

		# list of skip directions
		# used in conditional branching (#ifdef)
		skip_dict = {}

		out = ''

		while not rd.has_end():

			# handle whitespace
			junk = rd.consume_non_code()
			if len(junk) > 0:

				if junk.count('\n') > 0:
					out += '\n'
				else:
					out += ' '
				continue


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
				self.defines[d.name] = d


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

				if positive == (d.name in self.defines):
					# is defined


					# remember current pos
					rd.save_pos()

					# let's find the end of this branch
					endpos = rd.find_directive_block_end()
					rd.move_to(endpos)

					if rd.has_endif_directive():
						# there is no else branch to skip
						rd.undo() # back to saved pos
						continue

					elif rd.has_else_directive():
						# found start of else branch to skip
						rd.consume_else_directive()

						# find where the else ends
						endpos2 = rd.find_directive_block_end()

						# remember where to skip
						skip_dict[endpos] = endpos2

						rd.undo() # back to saved pos
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



	# def tokenize(self):
	# 	""" Tokenize and evaluate macros """

	# 	self._tk = Tokenizer(self.source, main_file)
	# 	self.tokens = None
	# 	self.tokens = self._tk.tokenize()


	# def show(self):
	# 	""" Print tokens to console """

	# 	if self.tokens == None:
	# 		raise Esception('Not parsed yet.')

	# 	_show_tokenlist(self.tokens)
