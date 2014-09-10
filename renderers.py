#!/bin/env python3

import re
from statements import *
from expressions import *
from mutators import *


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

	"""

	def __init__(self, program):
		self._source = program
		self._prepared = None
		self.indent = '    '


	def render(self):
		""" Convert the statements to the output source code.

		Returns:
			the rendered source code as string.

		"""

		if self._prepared is None:
			self._prepared = self._prepare(self._source)

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



class BasicRenderer(Renderer):
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
		src = self._do_render_any(s)

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

		if s.text.count('\n') == 0:
			return '// %s' % s.text
		else:
			return '/* %s */' % s.text


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
			src += '\n'
			src += self._render_any(
				s.then_st,
				level=1,  # indent the statement
				indent_first=True,
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

		raise Exception('Cannot render expr token %s' % str(e))


	def _render_expr_literal(self, e):  # E_Literal
		return e.value


	def _render_expr_operator(self, e):  # E_Operator
		return e.value


	def _render_expr_group(self, e):  # E_Group
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



class BasicSdsRenderer(BasicRenderer):
	""" SDS-C code renderer
	Takes care of SDS-C pecularities &
	refuses to render illegar statements / structures.

	"""

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

			if s.count("'") > 0:
				raise CompatibilityError(
					'Can\'t use single quote in SDS-C string, at %s'
					% str(e))

			s = s.replace('\\"', '"')

			return "'%s'" % s

		return super()._render_expr_literal(e)


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
						'Can\'t use expression as array index in SDS-C, at %s' %
						str(e))

			src += '[%s]' % self._render_expr(e.index)

		return src


	def _render_return(self, s):  # S_Return

		if self._render_expr(s.value) != '0':
			raise CompatibilityError(
				'SDS-C does not support return values, at %s' %
				str(s))

		return 'return;'


	def _render_expr_call(self, e):  # E_Call
		if e.name in self._userfuncs:
			raise CompatibilityError(
				'Can\'t use user-func in expression in SDS-C, at %s' %
				str(e))

		return super()._render_expr_call(e)



class SdsRenderer(BasicSdsRenderer):
	""" Final SDS renderer

	Attrs:
		same as parent, +
		mutators (Mutator[]): mutators applied during prepare

	"""

	def __init__(self, program):
		super().__init__(program)

		self.mutators = []
		self.mutators.append(M_AddBraces())
		self.mutators.append(M_CollectVars())


	def _prepare(self, code):

		for mut in self.mutators:
			code = mut.transform(code);

		return code



class SdsRenderer2(BasicSdsRenderer):
	""" Final SDS renderer

	Attrs:
		same as parent, +
		mutators (Mutator[]): mutators applied during prepare

	"""

	def __init__(self, program):
		super().__init__(program)

		self.mutators = []
		self.mutators.append(M_AddBraces())
		self.mutators.append(M_Grande())


	def _prepare(self, code):

		for mut in self.mutators:
			code = mut.transform(code);

		return code
