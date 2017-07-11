#!/bin/env python3

import re
import os
from statements import *
from expressions import *
from mutators import *
from time import localtime, strftime
from utils import *


class Renderer:
	""" Abstract code renderer.

	Takes a list of statements and composes a final source code.
	The final code should keep the functionality, but may have a different
	structure.

	Args:
		program (Statement[]): Program root level of statements

	Attributes:
		_source (Statement[]):
			The "program" argument is stored here
		_prepared (Statement[]):
			The source prepared for rendering
		indent (str):
			The used indent
		pragmas (dict):
			Pragmas to follow

	"""

	def __init__(self, program):
		self._source = program
		self._prepared = None
		self.indent = '    '
		self.pragmas = {}


	def _get_name(self):
		return type(self).__name__


	def set_pragmas(self, pragmas):
		self.pragmas = pragmas

		indent = self.pragmas.get('indent', 'tabs')

		if indent == 'tabs' or indent == '\t':
			self.indent = '\t'
		elif indent == 'spaces':
			self.indent = '    '
		else:
			self.indent = indent

		self._on_pragmas_set()


	def _on_pragmas_set(self):
		""" Called after self.pragmas got assigned """
		pass


	def render(self):
		""" Convert the statements to the output source code.

		Returns:
			the rendered source code as string.

		"""

		if self._prepared is None:
			self._prepared = self._prepare(self._source)

			# resolve header comment
			if self.pragmas.get('header', True):
				logo_file = os.path.join(os.path.dirname(__file__), 'logo.txt')

				if 'logo' in self.pragmas:
					f = self.pragmas.get('logo')

					if os.path.isfile(f):
						logo_file = f
					else:
						f = os.path.join(os.path.dirname(self.pragmas.get('main_file')), f)
						if os.path.isfile(f):
							logo_file = f
						else:
							print('[WARN] Could not locate logo file: %s' % self.pragmas.get('logo'))

				banner_text = ''
				if logo_file is not None:
					with open(logo_file, "r") as myfile:
						banner_text = myfile.read()


				f = os.path.join(os.path.dirname(__file__), 'header.txt')
				with open(f, "r") as myfile:
					header_text = myfile.read()

				header_text = header_text % {
					'name': self.pragmas.get('name', '?'),
					'author': self.pragmas.get('author', '?'),
					'version': self.pragmas.get('version', '?'),
					'time': strftime('%Y-%m-%d, %H:%M:%S', localtime()),
					'renderer': self._get_name(),
					'sdscp_version': self.pragmas.get('sdscp_version', '?'),
				}

				banner_text	= banner_text.strip('\n')
				header_text = header_text.strip('\n')

				longest = 0
				for line in banner_text.splitlines() + header_text.splitlines():
					l = len(line)
					if l > longest:
						longest = l

				bar = '\n\n' + ('=' * longest) + '\n\n'

				banner = S_Comment((bar + banner_text + bar + header_text + bar).strip('\n'))
				banner._header_comment = True

				self._prepared = [banner] + self._prepared

		return self._render(self._prepared)


	def _prepare(self, code):
		""" Prepare the statements for rendering.

		The renderer may change the statement order, modify them etc.

		Args:
			code (Statement[]): The statements to prepare

		Returns:
			the statements ready for the `_render()` method.

		"""

		return code  # stub


	def _render(self, code):
		""" Convert the statements to output source.

		Args:
			code (Statement[]): The statements to convert

		Returns:
			the rendered source code as string.

		"""

		raise Exception('Not implemented.')



class CSyntaxRenderer(Renderer):
	""" Renderer that produces C-like syntax.

	Extensible by overriding the individual `_render_?` methods.

	Args:
		program (Statement[]): the program to render

	Attributes:
		(attrs inherited from Renderer)
		_render_dict:
			dict (Statement class -> rendering func)
			Can be used to add new statement renderers or remove
			current ones.

	"""

	def _get_name(self):
		return 'csyntax'


	def __init__(self, program):
		super().__init__(program)

		# a list of statement-rendering private methods.
		self._render_dict = {
			S_Block:	self._render_block,
			S_Empty:	self._render_empty,
			S_Function:	self._render_function,
			S_Call:		self._render_call,
			S_Return:	self._render_return,
			S_Goto:		self._render_goto,
			S_Label:	self._render_label,
			S_If:		self._render_if,
			S_Switch:	self._render_switch,
			S_Case:		self._render_case,
			S_Default:	self._render_default,
			S_While:	self._render_while,
			S_DoWhile:	self._render_dowhile,
			S_For:		self._render_for,
			S_Break:	self._render_break,
			S_Continue:	self._render_continue,
			S_Var:		self._render_var,
			S_Assign:	self._render_assign,
			S_Comment:	self._render_comment
		}


	def _render(self, code):
		""" Overrides render stub from Renderer """

		src = ''

		for s in code:
			src += self._render_any(s)

		return src.strip() + '\n'  # One trailing newline


	def _render_any(self, s, level=0, indent_first=True, append_newline=True):
		""" Render a statement by type

		Args:
			s (Statement):
				Statement to render
			level (int, optional):
				Indentation level to render at
			indent_first (bool):
				Whether to indent first line
			append_newline (bool):
				Whether to append a trailing newline

		Returns:
			statement rendered, ending with a newline.

		"""

		# remove whitespace at ends
		src = self._do_render_any(s).strip('\n')
		if src == '':
			return src

		if indent_first:
			# add newline in front of it, to trigger indentation
			src = '\n' + src

		# Add indents
		tab = (self.indent * level)
		src = src.replace('\n', '\n' + tab)

		if indent_first:
			# remove the added newline
			src = src[1:]

		if append_newline or isinstance(s, S_Function):
			# add trailing newline
			src += '\n'

		if isinstance(s, S_Function):
			src = '\n' + src

		if hasattr(s, '_header_comment'):
			src += '\n'

		return src


	def _do_render_any(self, s):
		""" Render a statement by type.

		Args:
			s (Statement): Statement to render

		Returns:
			statement rendered

		"""

		try:
			return self._render_dict[type(s)](s)
		except KeyError:
			raise Exception(
				'Cannot render statement %s (type %s)' %
				(
					str(s),
					str(type(s))
				))


	def _render_block(self, s):  # S_Block
		src = '{\n'

		for c in s.children:
			src += self._render_any(c, 1)

		src += '}'

		return src


	def _render_switch_block(self, s):  # S_Block
		src = '{\n'

		for c in s.children:
			if isinstance(c, S_Case) or isinstance(c, S_Default):
				src += self._render_any(c, 1)
			else:
				src += self._render_any(c, 2)

		src += '}'

		return src


	def _render_empty(self, s):  # S_Empty
		return ';'


	def _render_comment(self, s):  # S_Comment

		if self.pragmas.get('comments', True) or hasattr(s, '_header_comment'):
			if s.text.count('\n') == 0:
				return '// %s' % s.text
			else:
				return '/*\n%s\n*/' % s.text.rstrip('\n').lstrip('\n')
		else:
			return ''


	def _render_function(self, s):  # S_Function

		src = '%s(%s)\n' % (
			s.name,
			', '.join(s.args)
		)

		src += self._render_any(s.body_st)

		return src


	def _render_call(self, s):  # S_Call
		src = s.name
		src += '('

		exprs = [self._render_expr(e) for e in s.args]
		src += ', '.join(exprs)

		src += ');'

		return src


	def _render_return(self, s):  # S_Return
		return 'return %s;' % self._render_expr(s.value)


	def _render_goto(self, s):  # S_Goto
		return 'goto %s;' % s.name


	def _render_label(self, s):  # S_Label
		return 'label %s:' % s.name


	def _render_if(self, s):  # S_If

		src = 'if (%s) ' % self._render_expr(s.cond)

		# Try to evaluate condition
		if not hasattr(self, '_erndr'):
			self._erndr = CSyntaxRenderer([])

		condorigstr = self._erndr._render_expr(s.cond)

		if type(s.cond) is E_Group:
			try:
				as_str = self._erndr._render_expr(s.cond)
				val = eval_expr(as_str)

				s.cond = E_Literal( T_Number( str( round(val) ) ) )

			except (ValueError, TypeError, SyntaxError, KeyError):
				pass

		# Optimization for dead branch
		if type(s.cond) is E_Literal:

			st = None
			src = ''

			if int(str(s.cond)) == 0:
				# always False
				st = s.else_st
				src += self._render_comment(S_Comment('(IF always false: else only)')) + '\n'
				print('IF always false at if(%s)' % condorigstr)
			else:
				# always True
				st = s.then_st
				src += self._render_comment(S_Comment('(IF always true: then only)')) + '\n'
				print('IF always true at if(%s)' % condorigstr)

			if type(st) is S_Block:
				for c in st.children:
					src += self._render_any(c)
			else:
				src = self._render_any(st)

			return src.rstrip('\n')

		# normalize empty code block to empty statement
		if type(s.else_st) is S_Block and len(s.else_st.children) == 0:
			s.else_st = S_Empty()

		if type(s.then_st) is S_Block and len(s.then_st.children) == 0:
			s.then_st = S_Empty()

		is_two_goto = True
		is_two_goto &= (
			(type(s.then_st) is S_Goto) or
			(type(s.then_st) is S_Block and len(s.then_st.children) == 1 and type(s.then_st.children[0]) is S_Goto))
		is_two_goto &= (
			(type(s.else_st) is S_Goto) or
			(type(s.else_st) is S_Block and len(s.else_st.children) == 1 and type(s.else_st.children[0]) is S_Goto))

		if is_two_goto:
			g1 = s.then_st
			if type(g1) is S_Block:
				g1 = g1.children[0]

			g2 = s.else_st
			if type(g2) is S_Block:
				g2 = g2.children[0]

			src += 'goto %s else goto %s;' % (g1.name, g2.name)

			return src

		small_then = True

		if isinstance(s.then_st, S_Block):
			# big THEN
			small_then = False
			src += self._render_any(
				s.then_st,
				append_newline=False)
			src += ' '
		else:
			# small THEN
			indent = not isinstance(s.else_st, S_Empty)

			if indent:
				src += '\n'

			src += self._render_any(
				s.then_st,
				level=1,  # indent the statement
				indent_first=indent,
				append_newline=False)


		if not isinstance(s.else_st, S_Empty):
			# there is some ELSE

			if small_then:
				src += '\n'

			src += 'else '

			if isinstance(s.else_st, S_Block):
				# big ELSE
				src += self._render_any(
					s.else_st,
					append_newline=False)
			else:
				# small ELSE
				src += '\n'
				src += self._render_any(
					s.else_st,
					level=1,  # indent the statement
					indent_first=True,
					append_newline=False)

		return src


	def _render_switch(self, s):  # S_Switch
		src = 'switch (%s) ' % self._render_expr(s.value)

		src += self._render_switch_block(s.body_st)

		return src


	def _render_case(self, s):  # S_Case
		return 'case %s:' % self._render_expr(s.value)


	def _render_default(self, s):  # S_Case
		return 'default:'


	def _render_while(self, s):  # S_While
		src = 'while (%s) ' % self._render_expr(s.cond)

		if isinstance(s.body_st, S_Block):
			src += self._render_any(s.body_st)
		else:
			src += '\n' + self._render_any(
				s.body_st,
				level=1)

		return src


	def _render_dowhile(self, s):  # S_While
		src = 'do '

		if isinstance(s.body_st, S_Block):
			src += self._render_any(
				s.body_st,
				append_newline=False)
			src += ' '
		else:
			src += '\n' + self._render_any(
				s.body_st,
				level=1)

		src += 'while (%s);' % self._render_expr(s.cond)

		return src


	def _render_for(self, s):  # S_For

		inits = ', '.join( [self._do_render_any(i) for i in s.init] )
		inits = inits.replace(';,', ',')

		iters = ', '.join( [self._do_render_any(i) for i in s.iter] )
		iters = iters.replace(';,', ',')

		# remove trailing semicolon
		if iters.endswith(';'):
			iters = iters[:-1]

		src = 'for ('
		src += inits + ' '
		src += self._render_expr(s.cond) + '; '
		src += iters
		src += ') '
		if isinstance(s.body_st, S_Block):
			src += self._render_any(s.body_st)
		else:
			src += '\n' + self._render_any(
				s.body_st,
				level=1)


		return src


	def _render_break(self, s):  # S_Break
		return 'break;'


	def _render_continue(self, s):  # S_Continue
		return 'continue;'


	def _render_var(self, s):  # S_Var
		src = 'var '

		src += s.var.name

		if s.value is not None:
			src += ' = '
			src += self._render_expr(s.value)

		src += ';'

		return src


	def _render_assign(self, s):  # S_Assign

		src = self._render_expr_variable(s.var)

		src += ' %s ' % s.op.value
		src += self._render_subexpr(s.value)
		src += ';'

		return src


	def _render_expr(self, e):  # Expression

		if isinstance(e, E_Group):
			# a paren
			# return only what is inside
			src = ''
			for ee in e.children:
				src += ' ' + self._render_subexpr(ee)
			return src.strip()

		else:
			return self._render_subexpr(e)


	def _render_subexpr(self, e):  # Expression nested in another
		if isinstance(e, E_Literal):
			return self._render_expr_literal(e)

		if isinstance(e, E_Operator):
			return self._render_expr_operator(e)

		if isinstance(e, E_Group):
			return self._render_expr_group(e)

		if isinstance(e, E_Variable):
			return self._render_expr_variable(e)

		if isinstance(e, E_Call):
			return self._render_expr_call(e)

		raise Exception('Cannot render expr token %s (type %s)' % (e, type(e)))


	def _render_expr_literal(self, e):  # E_Literal
		return e.value


	def _render_expr_operator(self, e):  # E_Operator
		#special treatment for unary
		if e.value == '@+':
			return '+'

		if e.value == '@-':
			return '-'

		return e.value


	def _render_expr_group(self, e):  # E_Group

		if len(e.children) == 1:
			return self._render_subexpr(e.children[0])

		src = ''
		for ee in e.children:
			src += ' ' + self._render_subexpr(ee)

		return '(%s)' % src.strip()


	def _render_expr_variable(self, e):  # E_Variable
		src = e.name

		if e.index is not None:
			src += '[%s]' % self._render_expr(e.index)

		return src


	def _render_expr_call(self, e):  # E_Call
		inner = []
		for a in e.args:
			inner.append(self._render_expr(a))

		src = e.name + '(%s)' % ', '.join(inner)

		return src



class BaseSdsRenderer(CSyntaxRenderer):
	""" SDS-C code renderer
	Takes care of SDS-C pecularities &
	refuses to render illegar statements / structures.

	"""

	def _get_name(self):
		return 'basic_sds'

	def __init__(self, program):
		super().__init__(program)

		# disable illegal statement renderers for SDS-C
		del self._render_dict[S_Switch]
		del self._render_dict[S_Case]
		del self._render_dict[S_Default]
		del self._render_dict[S_While]
		del self._render_dict[S_DoWhile]
		del self._render_dict[S_For]
		del self._render_dict[S_Break]
		del self._render_dict[S_Continue]

		# find all user funcs (for detecting invalid use in exprs)
		self._userfuncs = []
		for s in program:
			if isinstance(s, S_Function):
				self._userfuncs.append(s.name)


	def _render_expr_literal(self, e):

		# convert quotes for string
		if e.is_string():
			s = e.value[1:-1]

			s = s.replace("'", "\\'")
			s = s.replace('\\"', '"')

			return "'%s'" % s

		elif e.is_char():
			print('Converting char to ascii value @ %s' % e.value)

			e.token = T_Number(str(ord(e.value[1:-1])))
			e.value = e.token.value

		return super()._render_expr_literal(e)


	# Raise error if trying to assign string to variable
	def _render_assign(self, s):  # S_Assign
		if self._find_string_literal(s.value):
			raise CompatibilityError(
				'SDS-C does not support string variables, at %s' % super()._render_assign(s))

		return super()._render_assign(s)


	def _find_string_literal(self, e):
		if isinstance(e, E_Literal):
			return e.is_string()

		if isinstance(e, E_Group):
			for ee in e.children:
				if self._find_string_literal(ee):
					return True

		return False

	def _render_function(self, s):  # S_Function

		if len(s.args) > 0:
			raise CompatibilityError(
				'SDS-C does not support function arguments, at %s()' %
				str(s.name))

		# only name and block, no paren.
		src = s.name + '\n'
		src += self._render_any(s.body_st)

		return src


	def _render_expr_variable(self, e):  # E_Variable
		src = e.name

		if e.index is not None:

			if isinstance(e.index, E_Group):
				if len(e.index.children) > 1:
					raise CompatibilityError(
						'Can\'t use expression as array index in SDS-C, at %s'
						% e)

			src += '[%s]' % self._render_expr(e.index)

		return src


	def _render_return(self, s):  # S_Return

		if self._render_expr(s.value) != '0':
			raise CompatibilityError(
				'SDS-C does not support return values, at %s'
				% s)

		return 'return;'


	def _render_expr_call(self, e):  # E_Call
		if e.name in self._userfuncs:
			raise CompatibilityError(
				'Can\'t use user-func in expression in SDS-C, at %s'
				% e)

		return super()._render_expr_call(e)

	def _render_expr_operator(self, e):  # E_Operator

		if e.value in ['++', '--']:
			raise CompatibilityError('Can\'t use ++ and -- SDS-C expressions!')

		return super()._render_expr_operator(e)



class SimpleSdsRenderer(BaseSdsRenderer):
	""" Final SDS renderer

	Attrs:
		same as parent, +
		mutators (Mutator[]): mutators applied during prepare

	"""

	def _get_name(self):
		return 'simple'


	def __init__(self, program):
		super().__init__(program)

		self.mutators = [
			M_AddBraces(),
			M_CollectVars()
		]


	def _prepare(self, code):

		for mut in self.mutators:
			code = mut.transform(code)

		return code



class AsmSdsRenderer(BaseSdsRenderer):
	""" Final SDS renderer

	Attrs:
		same as parent, +
		mutators (Mutator[]): mutators applied during prepare

	"""

	def _get_name(self):
		return 'asm'


	def __init__(self, program):
		super().__init__(program)

		self.mutators = []

		self.mutators.append(M_Grande())
		self.mutators.append(M_AddBraces())
		self.mutators.append(M_RemoveDeadCode())


	def _on_pragmas_set(self):

		for m in self.mutators:
			m.read_pragmas(self.pragmas)


	def _prepare(self, code):

		for mut in self.mutators:
			code = mut.transform(code)

		return code
