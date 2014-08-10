#!/bin/env python3

import re
from statements import *
from expressions import *

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

	"""

	def _render(self, code):

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
		src = src.strip()

		if indent_first:
			# add newline in front of it, to trigger indentation
			src = '\n' + src

		# Add indents
		tab = (self.indent * level)
		src = src.replace('\n', '\n' + tab)

		if indent_first:
			# remove the added newline
			src = src[1:]

		if append_newline:
			# add trailing newline
			src += '\n'

		return src


	def _do_render_any(self, s):
		""" Render a statement by type.

		Args:
			s (Statement): Statement to render

		Returns:
			statement rendered

		"""

		# code block (used in structures)
		if isinstance(s, S_Block):
			return self._render_block(s)

		# empty statemenr
		if isinstance(s, S_Empty):
			return self._render_empty(s)

		# a function declaration
		if isinstance(s, S_Function):
			return self._render_function(s)

		# a function call
		if isinstance(s, S_Call):
			return self._render_call(s)

		# return statement
		if isinstance(s, S_Return):
			return self._render_return(s)

		# GOTO statement
		if isinstance(s, S_Goto):
			return self._render_goto(s)

		# LABEL
		if isinstance(s, S_Label):
			return self._render_label(s)

		# IF
		if isinstance(s, S_If):
			return self._render_if(s)

		# a switch statement
		if isinstance(s, S_Switch):
			return self._render_switch(s)

		# a CASE
		if isinstance(s, S_Case):
			return self._render_case(s)

		# a DEFAULT
		if isinstance(s, S_Default):
			return self._render_default(s)

		# while
		if isinstance(s, S_While):
			return self._render_while(s)

		# do-while
		if isinstance(s, S_DoWhile):
			return self._render_dowhile(s)

		# for
		if isinstance(s, S_For):
			return self._render_for(s)

		# break
		if isinstance(s, S_Break):
			return self._render_break(s)

		# continue
		if isinstance(s, S_Continue):
			return self._render_continue(s)

		# var declaration
		if isinstance(s, S_Var):
			return self._render_var(s)

		# var assignment
		if isinstance(s, S_Assign):
			return self._render_assign(s)

		raise Exception('Cannot render statement %s' % str(s))


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


	def _render_function(self, s):  # S_Function

		src = s.name + '('
		src += ', '.join(s.args)
		src += ')\n'
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
		return 'return ' + self._render_expr(s.value) + ';'


	def _render_goto(self, s):  # S_Goto
		return 'goto ' + s.name + ';'


	def _render_label(self, s):  # S_Label
		return s.name + ':'


	def _render_if(self, s):  # S_If
		src = 'if ('
		src += self._render_expr(s.cond)
		src += ') '

		if isinstance(s.then_st, S_Block):
			# big THEN
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
			src += '\n'


		if not isinstance(s.else_st, S_Empty):
			# there is some ELSE

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
		src = 'switch ('
		src += self._render_expr(s.value)
		src += ') '
		src += self._render_switch_block(s.body_st)

		return src



	def _render_case(self, s):  # S_Case
		return 'case ' + self._render_expr(s.value) + ':'



	def _render_default(self, s):  # S_Case
		return 'default:'



	def _render_while(self, s):  # S_While
		src = 'while ('
		src += self._render_expr(s.cond)
		src += ') '

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

		src += 'while ('
		src += self._render_expr(s.cond)
		src += ');'

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

		src += ' = '
		src += self._render_expr(s.value)
		src += ';'

		return src


	def _render_assign(self, s):  # S_Assign

		src = s.var.name
		if s.var.index is not None:
			src += '[%s]' % self._render_expr(s.var.index)

		src += ' %s ' % s.op.value
		src += self._render_expr(s.value)
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

	def _render_subexpr(self, e):  # Expression

		if isinstance(e, E_Literal):
			return e.value

		if isinstance(e, E_Operator):
			return e.value

		if isinstance(e, E_Group):
			src = ''
			for ee in e.children:
				src += ' ' + self._render_subexpr(ee)

			return '(%s)' % src.strip()

		if isinstance(e, E_Variable):
			src = e.name

			if e.index is not None:
				src += '[%s]' % self._render_subexpr(e.index)

			return src

		if isinstance(e, E_Call):

			inner = []
			for a in e.args:
				inner.append(self._render_expr(a))

			src = e.name + '(%s)' % ', '.join(inner)

			return src

		raise Exception('Cannot render expr token %s' % str(e))
