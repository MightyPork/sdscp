#!/bin/env python3

from statements import *
from expressions import *
from utils import CompatibilityError, Obj

class Mutator:
	""" Code mutator

	Takes source code and generates some other code,
	applying transformations.

	"""

	def transform(self, code):
		""" Apply transformations to the code

		Args:
			code (Statement[]): source code

		Returns:
			code transformed by the mutator.

		"""

		return self._transform(code)


	def _transform(self, code):
		""" Do the stuff

		Args:
			code (Statement[]): source

		Returns:
			transformed code

		"""

		return code



class M_AddBraces(Mutator):
	""" Adds braces to control structures """

	def _transform(self, code):
		processed = []
		for s in code:
			processed.append(self._add_braces(s))

		return processed


	def _add_braces(self, s):

		if isinstance(s, S_If):

			# wrap THEN
			if isinstance(s.then_st, S_Block):
				s.then_st = self._add_braces(s.then_st)
			else:  # not a block
				ss = S_Block(None)
				ss.children = [self._add_braces(s.then_st)]
				s.then_st = ss

			# wrap ELSE
			if (not isinstance(s.else_st, S_Empty)):
				if isinstance(s.else_st, S_Block):
					s.else_st = self._add_braces(s.else_st)
				else:
					ss = S_Block(None)
					ss.children = [self._add_braces(s.else_st)]
					s.else_st = ss

		elif isinstance(s, S_Block):
			c = []
			for ss in s.children:
				c.append(self._add_braces(ss))

			s.children = c

		elif (isinstance(s, S_For) or
			isinstance(s, S_While) or
			isinstance(s, S_Switch) or
			isinstance(s, S_Function) or
			isinstance(s, S_DoWhile)):

			if not isinstance(s.body_st, S_Block):
				# wrap body
				ss = S_Block(None)
				ss.children = [self._add_braces(s.body_st)]
				s.body_st = ss
			else:
				s.body_st = self._add_braces(s.body_st)

		return s



class M_CollectVars(Mutator):
	""" Collect global vars at the top """

	def _transform(self, code):
		""" Move all global variables to the top of the code.
		Global = outside functions. Also validates that in root
		scope only functions and variables are used.

		"""

		variables = []
		functions = []

		for s in code:
			if isinstance(s, S_Var):
				variables.append(s)
			elif isinstance(s, S_Function):
				functions.append(s)
			else:
				raise CompatibilityError(
					'Illegal statement in root scope: %s' %
					str(s))

		return variables + functions



class TmpVarPool:
	""" Pool of temporary variables """

	def __init__(self):
		self.used_cnt = 0
		self.locks = {}


	def _gen_name(self, index):
		return "__tmp_%d" % (index)


	def acquire(self):
		""" Acquire a free temporary variable """

		for (name, used) in self.locks:
			if not used:
				self.locks[name] = True
				return name

		name = self._gen_name(self.used_cnt)
		self.used_cnt += 1

		self.locks[name] = True

		return name


	def release(self, name):
		""" Release a temporary variable """

		self.locks[name] = False


	def get_names(self):
		return self.locks.keys()



class ArgPool:
	""" Pool of transport variables for arguments """

	def __init__(self):
		self.used_cnt = 0
		self.ptr = 0
		self.vars = []


	def _gen_name(self, index):
		return "__arg_%d" % (index)


	def rewind(self):
		""" Rewind to start """
		self.ptr = 0


	def acquire(self):
		""" Get a free arg variable """
		if self.ptr >= self.used_cnt:
			# must add new one
			self.vars.append(self._gen_name(self.ptr))
			self.used_cnt += 1

		name = self.vars[self.ptr]
		self.ptr += 1

		return name



class LabelPool:
	""" Generates unique label names """

	def __init__(self):
		self.counters = {}
		self.used = []


	def make(self, prefix='label'):
		""" Make a unique label with given prefix """
		if prefix in self.counters:
			self.counters[prefix] += 1
		else:
			self.counters[prefix] = 0

		name = '__%s_%d' % (prefix, self.counters[prefix])
		self.register(name)

		return name


	def register(self, name):
		""" Add a label name to the list - for checking existence
		Used also for user labels.
		"""

		self.used.append(name)


	def exists(self, name):
		""" Check if given label exists in the program """

		return name in self.used



class M_Grand(Mutator):
	""" The master mutator for SDSCP extra features """

	def _transform(self, code):

		self.globals_declare = []
		self.globals_assign = []

		self.functions = []
		self.tmp_pool = TmpVarPool()
		self.arg_pool = ArgPool()
		self.labels = LabelPool()

		self.init_generated = []
		self.main_generated = []

		init_userfn = None
		main_userfn = None

		# register return value
		self._add_global_var('__retval')

		# iterate through top level statements
		for s in code:
			if isinstance(s, S_Var):
				self._add_global_var(s.var.name, s.value)

			elif isinstance(s, S_Function):
				if s.name == 'main':
					self.main_userfn = s
				elif s.name == 'init':
					self.init_userfn = s
				else:
					functions.append(s)

			else:
				raise CompatibilityError(
					'Illegal statement in root scope: %s' %
					str(s))


		# == TODO == prepate boilerplate (trampoline, stack utils etc)


		if init_userfn is not None:
			init_userfn_processed = self._process_fn(init_userfn, naked=True)

		if main_userfn is not None:
			main_userfn_processed = self._process_fn(main_userfn, naked=True)


		# == TODO == process all other functions, create trampolines etc.
		functions_processed = []



		# Add used tmps to globals declare
		for name in self.tmp_pool.get_names():
			self._add_global_var(name)

		# Compose output code
		output_code = self.globals_declare

		# main func body statements
		sts = []
		sts.append(self._mk_label('__reset'))

		# assign global vars default values
		sts += self.globals_assign

		# extra generated stuff
		if len(self.init_generated) > 0:
			sts += self.init_generated

		# user init function
		if init_userfn is not None:
			sts += init_userfn_processed

		# infinite main loop
		sts.append(self._mk_label('__main_loop'))
		if main_userfn is not None:
			sts += main_userfn_processed
		sts.append(self._mk_goto('__main_loop'))

		# other user functions
		for fn in functions_processed:
			sts += fn  # func already contains header, return handler etc


		main = S_Function()
		main.name = 'main'
		main.body_st = S_Block()
		main.body_st.children = sts

		output_code.append(main)

		return output_code


	def _process_fn(self, fn, naked=False):
		""" linearize a func. naked = do not push / pop used tmp vars """

		self._decorate_fn(fn)

		# TODO process the func & contents

		# return linearized code

		raise NotImplementedError('TODO')

		return []


	def _add_global_var(self, name, value=None):
		""" Add a global variable; split to declaration & assignment """

		v = self._mk_var(name)
		self.globals_declare.append(v)

		if value is not None:
			a = self._mk_assign(name, value)
			self.globals_assign.append(a)


	def _decorate_fn(self, fn):
		""" Add meta fields to a function statement """

		fn.meta = Obj()

		# list of tmp vars modified within the scope of this function
		# to be pushed / popped at the beginning / end of the function
		fn.meta.changed_tmps = []

		# dict of translations of "local" var names to acquired tmp vars used instead
		# better than making global variable that's used as local.
		fn.meta.local_tmp_dict = {}

		# mapping arguments to tmp vars (order is kept)
		# vars are also added to local_tmp_dict
		fn.meta.arg_tmps = []


	def _mk_label(self, name):
		s = S_Label()
		s.name = name
		return s


	def _mk_goto(self, name):
		s = S_Goto()
		s.name = name
		return s


	def _mk_assign(self, name, value):
		s = S_Assign()
		s.var = E_Variable(name)
		s.value = value
		return s


	def _mk_var(self, name):
		s = S_Var()
		s.var = E_Variable(name)
		return s
