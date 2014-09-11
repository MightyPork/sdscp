#!/bin/env python3

import statements
from tokens import Tokenizer
from statements import *
from expressions import *
from utils import *

def synth(source):
	""" Parse source & convert to statements """

	tk = Tokenizer(source)
	tokens = tk.tokenize()
	return statements.parse(tokens)


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


		for (name, used) in self.locks.items():
			if not used:
				self.used_cnt += 1
				self.locks[name] = True
				return name

		name = self._gen_name(self.used_cnt)
		self.used_cnt += 1

		self.locks[name] = True

		return name


	def release(self, name):
		""" Release a temporary variable """

		if not name in self.locks.keys():
			raise Exception('Cannot release %s, not defined.' % name)

		self.locks[name] = False
		self.used_cnt -= 1


	def release_all(self):
		""" Release all tmp vars """

		for n in self.locks.keys():
			self.locks[n] = False
		self.used_cnt = 0


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


	def get_names(self):
		return self.vars



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



class FnRegistry:
	""" Registry of function labels and translations """

	def __init__(self, label_pool):
		self.counter = 0
		self.name2index = {}

		self.index2label = {}

		self.labels = label_pool

		self.call_counter = 0


	def register(self, name):
		""" Register a function. Returns index. """

		i = self.counter

		begin = self.get_begin(i)
		end = self.get_end(i)

		self.name2index[name] = i
		self.index2label[i] = begin

		self.labels.register(begin)
		self.labels.register(end)

		self.counter += 1
		return i


	def register_call(self):
		""" Register a call. Returns index. """

		i = self.counter
		label = self.get_call_label(i)

		self.index2label[i] = label

		self.labels.register(label)

		self.counter += 1;

		return i


	def get_begin(self, index):
		""" Get start label for a function

		Args:
			index: name or function index

		Returns:
			label name

		"""

		if type(index) == str:
			index = self.name2index[index]

		return "__fn_begin_%d" % index


	def get_end(self, index):
		""" Get end label of a function (for return)

		Args:
			index: name or function index

		Returns:
			label name

		"""

		if type(index) == str:
			index = self.name2index[index]

		return "__fn_end_%d" % index


	def get_call_label(self, index):
		""" Get return-from-call label

		Args:
			index: index of the call

		Returns:
			label name

		"""

		return "__retpos_%s" % index


	def get_trampoline_map(self):
		""" Get index -> label map """

		return self.index2label


	def get_addr(self, name):
		""" Get address for name """

		if not name in self.name2index.keys():
			raise Exception('Function not found, cannot call: %s' % name)

		return self.name2index[name]



class M_Grande(Mutator):
	""" The master mutator for SDSCP extra features """

	def __init__(self):

		# list of builtin functions
		self.builtin_fn = [
			'echo',
			'echoinline',
			'echoclear',
			'smtp_send',
			'ping',
			'dns_resolv',
			'wait',
			'http_get',
			'lcd_echo',
			'lcd_clear',
			'lcd_newline',
			'lcd_setpixel',
			'serial_set',
			'serial_write',
			'serial_text_out',
			'read_dataflash',
			'write_dataflash',
			'read_dataflash_page_to_ram',
			'write_ram_block_to_dataflash_page',
			'atoi',
			'sprintf',
			'snmp_send_trap',
			'send_udp',
			'onewire_rescan',
		]

		self.builtin_var = [
			'sys',
			'ram',
			'text',
		]



	def _transform(self, code):

		self.globals_declare = []
		self.globals_assign = []

		functions = []
		func_names = []

		self.tmp_pool = TmpVarPool()
		self.arg_pool = ArgPool()
		self.labels = LabelPool()
		self.fn_pool = FnRegistry(self.labels)

		init_userfn = None
		main_userfn = None

		# register helper vars
		self._add_global_var('__retval')  # return value
		self._add_global_var('__sp', 512)  # stack pointer at RAMEND (grows towards lower addrs)
		self._add_global_var('__addr')  # jump address pointer

		# iterate through top level statements
		for s in code:
			if isinstance(s, S_Var):
				self._add_global_var(s.var.name, s.value)

			elif isinstance(s, S_Function):

				if s.name in func_names:
					raise Exception('Duplicate function: %s()' % s.name)

				func_names.append(s.name)

				if s.name == 'main':
					main_userfn = s

				elif s.name == 'init':
					init_userfn = s

				else:
					func_names.append(s.name)
					functions.append(s)
					self.fn_pool.register(s.name)

			else:
				raise CompatibilityError(
					'Illegal statement in root scope: %s' %
					str(s))


		# == TODO == prepate boilerplate (trampoline, stack utils etc)


		# process init()
		if init_userfn is not None:
			init_userfn_processed = self._process_fn(init_userfn, naked=True)

		# process main()
		if main_userfn is not None:
			main_userfn_processed = self._process_fn(main_userfn, naked=True)


		# process user functions except main() & init()
		functions_processed = []
		for fn in functions:
			functions_processed.append(self._process_fn(fn))


		# Add used tmps to globals declare
		for name in self.tmp_pool.get_names():
			self._add_global_var(name)

		# Add args to globals
		for name in self.arg_pool.get_names():
			self._add_global_var(name)

		# Compose output code
		output_code = []
		append(output_code, S_Comment('Globals declaration'))
		append(output_code, self.globals_declare)

		# main func body statements
		sts = []

		# goto reset (skip trampolines)
		append(sts, self._mk_goto('__reset'))


		# trampoline
		append(sts, S_Comment('Redirection vector'))
		append(sts, self._mk_label('__trampoline'))

		for (i, n) in self.fn_pool.get_trampoline_map().items():
			append(sts, synth("""
				if (__addr == %d) goto %s;
			""" % (i, n)))

		append(sts, S_Comment('Fall-through for invalid address'))
		append(sts, self._mk_error('Bad address!'))

		# reset label
		append(sts, S_Comment('### FUNC: init() ###'))
		append(sts, self._mk_label('__reset'))

		# assign global vars default values
		append(sts, self.globals_assign)

		# user init function
		if init_userfn is not None:
			append(sts, init_userfn_processed)

		# infinite main loop
		append(sts, S_Comment('### FUNC: main() ###'))
		append(sts, self._mk_label('__main_loop'))
		if main_userfn is not None:
			sts += main_userfn_processed
		append(sts, self._mk_goto('__main_loop'))


		# other user functions
		for fn in functions_processed:
			append(sts, fn)  # func already contains header, return handler etc


		# compose main function with all the code
		main = S_Function()
		main.name = 'main'
		main.body_st = S_Block()
		main.body_st.children = sts

		output_code.append(main)

		return output_code


	def _process_fn(self, fn, naked=False):
		""" linearize a function. naked = do not push / pop used tmp vars """

		self._decorate_fn(fn)
		self.tmp_pool.release_all()

		if naked:
			return self._process_block(fn, fn.body_st.children)

		body = []

		self.arg_pool.rewind()

		# assign arguments to tmps
		append(body, S_Comment('Store args to tmp vars'))
		for n in fn.args:
			arg = self.arg_pool.acquire()
			tmp = self.tmp_pool.acquire()
			fn.meta.changed_tmps.append(tmp)
			fn.meta.local_tmp_dict[n] = tmp
			fn.meta.arg_tmps.append(tmp)

			append(body, synth("""
				%s = %s;
			""" % (tmp, arg)))

		append(body, S_Comment('Function body'))
		append(body, self._process_block(fn, fn.body_st.children))

		out = []

		# begin label
		append(out, S_Comment('### FUNC %s(%s) ###' % (fn.name, ','.join(fn.args))))

		label = self._mk_label(self.fn_pool.get_begin(fn.name))
		append(out, label)

		# push all changed tmp vars
		append(out, S_Comment('Push used tmp vars'))

		fn.meta.changed_tmps = list(set(fn.meta.changed_tmps))

		for n in fn.meta.changed_tmps:
			append(out, self._mk_push(n))

		append(out, body)

		# end label
		label = self._mk_label(self.fn_pool.get_end(fn.name))
		append(out, label)

		append(out, S_Comment('Pop used tmp vars'))
		for n in reversed(fn.meta.changed_tmps):
			append(out, self._mk_pop(n))

		append(out, S_Comment('Return to caller'))
		append(out, self._mk_pop('__addr'))  # pop a return address
		append(out, self._mk_goto('__trampoline'))

		return out


	def _process_block(self, fn, sts):
		""" Process a statement block

		Args:
			fn: The parent S_Function
			sts: list of statements in the block

		Returns block linearized.

		"""

		out = []

		for s in sts:
			tmps = []

			# local var
			if isinstance(s, S_Var):
				repl = self.tmp_pool.acquire()
				fn.meta.local_tmp_dict[s.var.name] = repl

				value = s.value

				if value is None:
					value = 0
				else:
					(init, tmps, value) = self._process_expr(fn, s.value)
					append(out, init)

				append(out, self._mk_assign(repl, value))

			elif isinstance(s, S_Assign):

				(init, _tmps, value) = self._process_expr(fn, s.value)
				append(out, init)
				append(tmps, _tmps)

				index = s.var.index

				if index is not None:
					# assign to array
					ind = self.tmp_pool.acquire()
					tmps.append(ind)

					(init, _tmps, ind_val) = self._process_expr(fn, index)
					append(out, init)
					append(tmps, _tmps)
					append(out, self._mk_assign(ind, ind_val))

					index = E_Variable(ind)

				append(out, self._mk_assign(name=s.var.name, value=value, op=s.op, index=index))

			elif isinstance(s, S_Call):  # func call with no return value assignment

				if s.name in self.builtin_fn:
					# a builtin function,
					# take care of complex arguments (SDS-C bug workaround)

					args = []
					for a in s.args:
						(init, _tmps, a_val) = self._process_expr(fn, a)
						append(out, init)
						append(tmps, _tmps)

						if isinstance(a_val, E_Group):
							# must use helper tmp
							tmp = self.tmp_pool.acquire()
							append(tmps, tmp)
							append(out, self._mk_assign(tmp, a_val))

							a_val = E_Variable(tmp)

						args.append(a_val)

					c = S_Call()
					c.name = s.name
					c.args = args

					append(out, c)

				else:
					# call to user func

					self.arg_pool.rewind()

					arg_assignments = []

					for a in s.args:

						arg_name = self.arg_pool.acquire()

						(init, _tmps, a_val) = self._process_expr(fn, a)
						append(out, init)
						append(tmps, _tmps)

						append(arg_assignments, self._mk_assign(arg_name, a_val))

					append(out, arg_assignments)

					# get return label index
					return_idx = self.fn_pool.register_call()

					# callee address
					addr = self.fn_pool.get_addr(s.name)
					append(out, self._mk_assign('__addr', addr))
					append(out, self._mk_push(return_idx))
					append(out, self._mk_goto('__trampoline'))

					# return label
					lbl = self.fn_pool.get_call_label(return_idx)
					append(out, self._mk_label(lbl))

			else:
				out.append(s)

			for t in tmps:
				fn.meta.changed_tmps.append(t)
				self.tmp_pool.release(t)

		# TODO: Handle other statements


		return out


	def _process_expr(self, fn, e):
		init = []
		tmps = []

		if isinstance(e, E_Group):
			new_children = []

			for c in e.children:
				(_init, _tmps, _e) = self._process_expr(fn, c)

				append(init, _init)
				append(tmps, _tmps)
				append(new_children, _e)

			return (init, tmps, E_Group(new_children))

		if isinstance(e, E_Variable):

			if fn is None:
				name = e.name
			else:
				name = fn.meta.local_tmp_dict.get(e.name, e.name)

			if e.index is None:
				return (init, tmps, E_Variable(name))

			elif isinstance(e.index, E_Literal):
				return (init, tmps, E_Variable(name, e.index))

			else:
				tmp = self.tmp_pool.acquire()

				(_init, _tmps, _e) = self._process_expr(fn, e.index)

				append(init, _init)
				append(tmps, _tmps)
				append(tmps, tmp)

				s = self._mk_assign(tmp, _e)
				init.append(s)

				return (init, tmps, E_Variable(name, E_Variable(tmp)))

		# TODO: handle call & return value, handle function arguments etc.

		return (init, tmps, e)


	def _add_global_var(self, name, value=None):
		""" Add a global variable; split to declaration & assignment """

		v = self._mk_var(name)
		self.globals_declare.append(v)

		if value is not None:

			(init, tmps, value) = self._process_expr(None, value)
			append(self.globals_assign, init)

			append(self.globals_assign, self._mk_assign(name, value))

			for t in tmps:
				self.tmp_pool.release(t)


	def _decorate_fn(self, fn):
		""" Add meta fields to a function statement """

		fn.bind_parent(None)

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

		return fn


	def _mk_label(self, name):
		s = S_Label()
		s.name = name
		return s


	def _mk_goto(self, name):
		s = S_Goto()
		s.name = name
		return s


	def _mk_assign(self, name, value, op='=', index=None):
		s = S_Assign()
		s.var = E_Variable(name, index)

		if type(value) == int:
			value = E_Literal(T_Number(str(value)))

		if type(value) == str:
			value = E_Variable(value)

		s.value = value

		if type(op) == str:
			op = T_AssignOperator(op)

		s.op = op

		return s


	def _mk_var(self, name):
		s = S_Var()
		s.var = E_Variable(name)
		return s


	def _mk_push(self, name):

		return synth("""
			__sp -= 1;
			ram[__sp] = %s;
		""" % name)


	def _mk_pop(self, name):

		return synth("""
			%s = ram[__sp];
			__sp += 1;
		""" % name)


	def _mk_error(self, message):

		return synth("""
			echo("%s");
			goto __reset;
		""" % message)
