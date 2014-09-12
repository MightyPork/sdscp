#!/bin/env python3

import statements
from tokens import Tokenizer
from statements import *
from expressions import *
from utils import *
import math

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

			has_else = (not isinstance(s.else_st, S_Empty))

			# wrap THEN
			if isinstance(s.then_st, S_Block):
				s.then_st = self._add_braces(s.then_st)
			else:  # not a block
				if type(s.then_st) is S_Goto and not has_else:
					pass
				else:
					ss = S_Block(None)
					ss.children = [self._add_braces(s.then_st)]
					s.then_st = ss

			# wrap ELSE
			if has_else:
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


	def acquire(self, prefix='label'):
		""" Make a unique label with given prefix """
		if prefix in self.counters:
			self.counters[prefix] += 1
		else:
			self.counters[prefix] = 1

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
		self.counter = 1
		self.name2index = {}
		self.index2name = {}

		self.index2label = {}

		self.label_pool = label_pool

		self.call_counter = 1

		self.function_labels = {}


	def register(self, name):
		""" Register a function. Returns index. """

		i = self.counter

		begin = self.get_begin(i)
		end = self.get_end(i)

		self.name2index[name] = i
		self.index2name[i] = name
		self.index2label[i] = begin

		self.label_pool.register(begin)
		self.label_pool.register(end)

		self.function_labels[i] = [begin, end]

		self.counter += 1
		return i


	def register_call(self):
		""" Register a call. Returns index. """

		i = self.counter
		label = self.get_call_label(i)

		self.index2label[i] = label

		self.label_pool.register(label)

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


	def get_name(self, addr):
		""" Get name from address """

		if not addr in self.index2name.keys():
			return None

		return self.index2name[addr]



class M_Grande(Mutator):
	""" The master mutator for SDSCP extra features

	Attrs:
		TODO

	"""

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

		self.stack_start = 300
		self.stack_end = 511

		self._halt_used = False

		self.do_check_stack_bounds = True

		self.banner_text = r"""
============================================
   _____ ____  _____ __________
  / ___// __ \/ ___// ____/ __ \
  \__ \/ / / /\__ \/ /   / /_/ /
 ___/ / /_/ /___/ / /___/ ____/
/____/_____//____/\____/_/

This SDS-C code was generated by SDSCP.

If you found a bug, please submit an issue
at https://github.com/MightyPork/sdscp

============================================
"""


	def _transform(self, code):

		self.globals_declare = []
		self.globals_assign = []

		functions = []
		self.user_fn = []

		self.tmp_pool = TmpVarPool()
		self.arg_pool = ArgPool()
		self.label_pool = LabelPool()
		self.fn_pool = FnRegistry(self.label_pool)

		self.functions_called = []

		init_userfn = None
		main_userfn = None

		# register helper vars
		self._add_global_var('__retval')  # return value
		self._add_global_var('__sp', self.stack_end + 1)  # stack pointer at RAMEND (grows towards lower addrs)
		self._add_global_var('__addr')  # jump address pointer

		# iterate through top level statements
		for s in code:
			if isinstance(s, S_Var):
				self._add_global_var(s.var.name, s.value)

			elif isinstance(s, S_Function):

				if s.name in self.user_fn:
					raise Exception('Duplicate function: %s()' % s.name)

				self.user_fn.append(s.name)

				if s.name == 'main':
					main_userfn = s

				elif s.name == 'init':
					init_userfn = s

				else:
					self.user_fn.append(s.name)
					functions.append(s)
					self.fn_pool.register(s.name)

			else:
				raise Exception('Illegal statement in root scope: %s' % s)


		# process init()
		if init_userfn is not None:
			init_userfn_processed = self._process_fn(init_userfn, naked=True)

		# process main()
		if main_userfn is not None:
			main_userfn_processed = self._process_fn(main_userfn, naked=True)


		# process user functions except main() & init()
		functions_processed = {}
		for fn in functions:
			functions_processed[fn.name] = self._process_fn(fn)


		# Add used tmps to globals declare
		for name in self.tmp_pool.get_names():
			self._add_global_var(name)

		# Add args to globals
		for name in self.arg_pool.get_names():
			self._add_global_var(name)

		# Compose output code
		output_code = []
		append(output_code, S_Comment(self.banner_text))
		append(output_code, S_Comment('Globals declaration'))
		append(output_code, self.globals_declare)

		# main func body statements
		sts = []

		# goto reset (skip trampolines)
		append(sts, S_Comment('Disable speed limit'))
		append(sts, synth('sys[63] = 128;'))

		append(sts, S_Comment('Jump to init vector'))
		append(sts, self._mk_goto('__init'))

		# trampoline
		append(sts, self._build_trampoline())

		# ERRORS
		append(sts, self._build_error_handlers())

		if self._halt_used:
			# Shutdown trap
			append(sts, self._build_shutdown_trap())

		# reset label
		append(sts, self._banner('FUNC: init()'))

		append(sts, self._mk_goto('__init'))
		append(sts, self._mk_label('__reset'))
		append(sts, self._mk_echo('[INFO] Program reset.'))
		append(sts, self._mk_label('__init'))
		append(sts, self._mk_echo('[INFO] Initialization...'))

		# assign global vars default values
		append(sts, self.globals_assign)

		# user init function
		if init_userfn is not None:
			append(sts, init_userfn_processed)

		# infinite main loop
		append(sts, self._banner('FUNC: main()'))
		append(sts, self._mk_echo('[INFO] main() started.'))
		append(sts, self._mk_label('__main_loop'))

		if main_userfn is not None:
			sts += main_userfn_processed

		append(sts, self._mk_goto('__main_loop'))


		# other user functions (already processed)
		for (name, fn_sts) in functions_processed.items():
			if not name in self.functions_called:
				print('INFO: Unused function %s(), removing from code.' % name)
			else:
				append(sts, fn_sts)

			# note: This optimization fails if dead function is called from
			# another dead function or from itself.


		# compose main function with all the code
		main = S_Function()
		main.name = 'main'
		main.body_st = S_Block()
		main.body_st.children = sts

		output_code.append(main)

		return output_code


	def _build_trampoline(self):
		""" Build redirection vector """

		sts = []
		append(sts, self._banner('Redirection vector'))
		append(sts, self._mk_label('__trampoline'))

		for (i, n) in self.fn_pool.get_trampoline_map().items():

			name = self.fn_pool.get_name(i)

			if (name is not None) and (not name in self.functions_called):
				print('INFO: Removing unused func from trampoline: %s' % name)
				continue

			append(sts, synth("""
				if (__addr == %d) goto %s;
			""" % (i, n)))

		append(sts, S_Comment('Fall-through for invalid address'))
		append(sts, self._mk_goto('__err_bad_addr'))

		return sts


	def _build_error_handlers(self):
		""" Build error handlers """

		sts = []
		append(sts, self._banner('Error handlers'))

		if self.do_check_stack_bounds:
			# stack overflow
			append(sts, self._mk_label('__err_so'))
			append(sts, self._mk_error('[ERROR] Stack overflow!'))
			# stack underflow
			append(sts, self._mk_label('__err_su'))
			append(sts, self._mk_error('[ERROR] Stack underflow!'))

		# bad address
		append(sts, self._mk_label('__err_bad_addr'))
		append(sts, self._mk_error('[ERROR] Bad address!'))

		return sts


	def _build_shutdown_trap(self):
		""" Build a shutdown trap """

		sts = []
		append(sts, self._banner('Shutdown trap'))
		append(sts, synth("""
			label __halt:
			echo("[INFO] Program halted.");
			label __halt_loop:
			wait(1000);
			goto __halt_loop;
		"""))

		return sts


	def _process_fn(self, fn, naked=False):
		""" linearize a function. naked = do not push / pop used tmp vars """

		self._decorate_fn(fn)
		self.tmp_pool.release_all()

		if naked:
			return self._process_block(fn, fn.body_st.children)

		body = []

		self.arg_pool.rewind()

		if len(fn.args) > 0:
			# assign arguments to tmps
			append(body, S_Comment('Store args to tmp vars'))
			for n in fn.args:
				arg = self.arg_pool.acquire()
				tmp = self.tmp_pool.acquire()
				fn.meta.changed_tmps.append(tmp)
				fn.meta.local_tmp_dict[n] = tmp
				fn.meta.arg_tmps.append(tmp)

				append(body, self._mk_assign(tmp, arg))

		append(body, self._mk_assign('__retval', 0))

		append(body, S_Comment('Function body'))
		append(body, self._process_block(fn, fn.body_st.children))

		out = []

		# begin label
		append(out, self._banner('FUNC %s(%s)' % (fn.name, ','.join(fn.args))))

		label = self._mk_label(self.fn_pool.get_begin(fn.name))
		append(out, label)

		# push all changed tmp vars
		if len(fn.meta.changed_tmps) > 0:
			append(out, S_Comment('Push used tmp vars'))

			fn.meta.changed_tmps = list(set(fn.meta.changed_tmps))

			for n in fn.meta.changed_tmps:
				append(out, self._mk_push(n))

		append(out, body)

		# end label
		label = self._mk_label(self.fn_pool.get_end(fn.name))
		append(out, label)

		if len(fn.meta.changed_tmps) > 0:
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

		if isinstance(sts, S_Block):
			sts = sts.children

		if isinstance(sts, Statement):
			sts = [sts]

		# init transformer dict on demand
		if not hasattr(self, '_statement_transformers'):

			self._statement_transformers = {
				S_Empty:	None,
				S_Goto:		self._transform_noop,
				S_Label:	self._transform_noop,
				S_Return:	self._transform_return,
				S_Var:		self._transform_var,
				S_Assign:	self._transform_assign,
				S_Call:		self._transform_call,
				S_If:		self._transform_if,
				S_While:	self._transform_while,
				S_DoWhile:	self._transform_dowhile,
				S_For:		self._transform_for,
				S_Break:	self._transform_break,
				S_Continue:	self._transform_continue,
				S_Switch:	self._transform_switch  # also handles case and default.
			}

		out = []

		for s in sts:
			try:
				transformer = self._statement_transformers[type(s)]

				if transformer is not None:
					(_init, _tmps) = transformer(fn, s)
					append(out, _init)
					self._fn_release_tmps(fn, _tmps)

			except KeyError:
				print('WARN: Unhandled statement %s (type %s)' % (s, type(s)))
				append(out, s)

		return out


	def _transform_noop(self, fn, s):
		""" No change """
		return (s, [])


	def _transform_var(self, fn, s):
		out = []
		tmps = []

		# reuse if already declared in the function
		if s.var.name in fn.meta.local_tmp_dict.keys():
			repl = fn.meta.local_tmp_dict[s.var.name]
		else:
			repl = self.tmp_pool.acquire()
			fn.meta.local_tmp_dict[s.var.name] = repl

		value = s.value

		if value is None:
			value = 0
		else:
			(_init, _tmps, value) = self._process_expr(fn, s.value)
			append(out, _init)
			append(tmps, _tmps)

		append(out, self._mk_assign(repl, value))

		return (out, tmps)


	def _transform_assign(self, fn, s):
		out = []
		tmps = []

		(_init, _tmps, value) = self._process_expr(fn, s.value)
		append(out, _init)
		append(tmps, _tmps)

		if not isinstance(s.var, E_Variable):
			raise Exception('Cannot assign to %s (type %s)' % (args[0], type(args[0])))

		(_init, _tmps, var) = self._process_expr(fn, s.var)
		append(out, _init)
		append(tmps, _tmps)

		append(out, self._mk_assign(name=var, value=value, op=s.op))

		return (out, tmps)


	def _transform_call(self, fn, s):
		out = []
		tmps = []

		if s.name in self.builtin_fn:
			# a builtin function,
			# take care of complex arguments (SDS-C bug workaround)

			(_init, _tmps, args) = self._prepare_builtin_func_args(fn, s.args)
			append(out, _init)
			append(tmps, _tmps)

			c = S_Call()
			c.name = s.name
			c.args = args

			append(out, c)

		else:
			# call to user func
			append(out, self._call_user_func(fn, s.name, s.args))
			self.functions_called.append(s.name)

		return (out, tmps)


	def _transform_return(self, fn, s):
		out = []
		tmps = []

		(_init, _tmps, rval) = self._process_expr(fn, s.value)
		append(out, _init)
		append(tmps, _tmps)

		append(out, self._mk_assign('__retval', rval))
		append(out, self._mk_goto(self.fn_pool.get_end(fn.name)))

		return (out, tmps)


	def _transform_if(self, fn, s):
		out = []
		tmps = []

		append(out, S_Comment('IF begin'))

		(_init, _tmps, cond) = self._process_expr(fn, s.cond)
		append(out, _init)
		append(tmps, _tmps)

		ss = S_If()
		ss.cond = cond
		ss.then_st = S_Block()
		ss.then_st.children = self._process_block(fn, s.then_st)
		ss.else_st = S_Block()
		ss.else_st.children = self._process_block(fn, s.else_st)

		append(out, ss)

		append(out, S_Comment('IF end'))

		return (out, tmps)


	def _transform_while(self, fn, s):
		out = []
		tmps = []

		append(out, S_Comment('WHILE begin'))

		l_continue = self.label_pool.acquire('while_continue')
		l_body = self.label_pool.acquire('while_body')
		l_break = self.label_pool.acquire('while_break')

		# add meta to the loop
		s.meta = Obj()
		s.meta.l_continue = l_continue
		s.meta.l_body = l_body
		s.meta.l_break = l_break

		# continue label
		append(out, self._mk_label(l_continue))

		(_init, _tmps, cond) = self._process_expr(fn, s.cond)
		append(out, _init)
		append(tmps, _tmps)

		# condition
		ss = S_If()
		ss.cond = cond
		ss.then_st = self._mk_goto(l_body)
		ss.else_st = self._mk_goto(l_break)
		append(out, ss)

		# body
		append(out, self._mk_label(l_body))

		append(out, self._process_block(fn, s.body_st))

		# end of body
		append(out, self._mk_goto(l_continue))
		append(out, self._mk_label(l_break))

		append(out, S_Comment('WHILE end'))

		return (out, tmps)


	def _transform_dowhile(self, fn, s):
		out = []
		tmps = []

		append(out, S_Comment('DO_WHILE begin'))

		l_continue = self.label_pool.acquire('dowhile_continue')
		l_body = self.label_pool.acquire('dowhile_body')
		l_break = self.label_pool.acquire('dowhile_break')

		# add meta to the loop
		s.meta = Obj()
		s.meta.l_continue = l_continue
		s.meta.l_body = l_body
		s.meta.l_break = l_break

		# body
		append(out, self._mk_label(l_body))

		append(out, self._process_block(fn, s.body_st))

		# continue label
		append(out, self._mk_label(l_continue))

		(_init, _tmps, cond) = self._process_expr(fn, s.cond)
		append(out, _init)
		append(tmps, _tmps)

		# condition
		ss = S_If()
		ss.cond = cond
		ss.then_st = self._mk_goto(l_body)
		ss.else_st = self._mk_goto(l_break)
		append(out, ss)

		# end of body
		append(out, self._mk_label(l_break))

		append(out, S_Comment('DO_WHILE end'))

		return (out, tmps)


	def _transform_for(self, fn, s):
		out = []
		tmps = []

		append(out, S_Comment('FOR begin'))

		l_continue = self.label_pool.acquire('for_continue')
		l_cond = self.label_pool.acquire('for_condition')
		l_body = self.label_pool.acquire('for_body')
		l_break = self.label_pool.acquire('for_break')

		# add meta to the loop
		s.meta = Obj()
		s.meta.l_continue = l_continue
		s.meta.l_body = l_body
		s.meta.l_break = l_break
		s.meta.l_cond = l_cond

		# the init
		append(out, self._process_block(fn, s.init))

		# condition check
		append(out, self._mk_label(l_cond))

		(_init, _tmps, cond) = self._process_expr(fn, s.cond)
		append(out, _init)
		append(tmps, _tmps)

		ss = S_If()
		ss.cond = cond
		ss.then_st = self._mk_goto(l_body)
		ss.else_st = self._mk_goto(l_break)
		append(out, ss)

		# body
		append(out, self._mk_label(l_body))

		append(out, self._process_block(fn, s.body_st))

		# continue (iter)
		append(out, self._mk_label(l_continue))
		append(out, self._process_block(fn, s.iter))
		append(out, self._mk_goto(l_cond))

		# break
		append(out, self._mk_label(l_break))
		append(out, S_Comment('FOR end'))

		return (out, tmps)


	def _transform_break(self, fn, s):
		out = []

		p = s
		while True:
			p = p.get_parent()

			if p is None:
				raise Exception('Break outside loop or switch!')

			if type(p) in [S_For, S_While, S_DoWhile, S_Switch]:

				# a loop or switch
				append(out, self._mk_goto(p.meta.l_break))
				break

		return (out, [])


	def _transform_continue(self, fn, s):
		out = []

		p = s
		while True:
			p = p.get_parent()

			if p is None:
				raise Exception('Continue outside loop!')

			if type(p) in [S_For, S_While, S_DoWhile]:

				# a loop or switch
				append(out, self._mk_goto(p.meta.l_continue))
				break

		return (out, [])


	def _transform_switch(self, fn, s):
		out = []
		tmps = []

		append(out, S_Comment('SWITCH begin'))

		l_break = self.label_pool.acquire('switch_break')

		# add meta to the switch
		s.meta = Obj()
		s.meta.l_break = l_break

		compared = self.tmp_pool.acquire()
		tmps.append(compared)

		append(out, self._mk_assign(compared, s.value))

		case_active = False
		l_next_case = self.label_pool.acquire('case')

		for ss in s.body_st.children:
			if type(ss) is S_Case:


				l_skip_case = self.label_pool.acquire('case_skip')

				# already in case, skip the test
				if case_active:
					append(out, self._mk_goto(l_skip_case))

				# add case label
				append(out, self._mk_label(l_next_case))

				# prepare label for next case
				l_next_case = self.label_pool.acquire('case')

				# prepare the if
				st = S_If()
				st.cond = E_Group([E_Variable(compared), E_Operator('=='), ss.value])
				st.then_st = self._mk_goto(l_skip_case)
				st.else_st = self._mk_goto(l_next_case)
				append(out, st)

				# skip case label
				append(out, self._mk_label(l_skip_case))

				case_active = True

			elif type(ss) is S_Default:
				append(out, self._mk_label(l_next_case))
				l_next_case = self.label_pool.acquire('case')

				case_active = True

			else:
				append(out, self._process_block(fn, ss))

		# label for last case false jump
		append(out, self._mk_label(l_next_case))
		append(out, self._mk_label(l_break))

		append(out, S_Comment('SWITCH end'))

		return (out, tmps)


	def _fn_release_tmps(self, fn, tmps):
		""" Release tmps used in a function & mark them as dirty in the function """

		for t in tmps:
			fn.meta.changed_tmps.append(t)
			self.tmp_pool.release(t)


	def _process_expr(self, fn, e):

		if type(e) == int:
			e = E_Literal(T_Number(str(e)))
		elif type(e) == str:
			e = E_Variable(e)

		init = []
		tmps = []
		expr = e

		if isinstance(e, E_Group):
			new_children = []

			for c in e.children:
				(_init, _tmps, _e) = self._process_expr(fn, c)

				append(init, _init)
				append(tmps, _tmps)
				append(new_children, _e)

			expr = E_Group(new_children)

		elif isinstance(e, E_Variable):

			# translate name to tmp name
			if fn is None:
				name = e.name
			else:
				name = fn.meta.local_tmp_dict.get(e.name, e.name)

			if e.index is None:
				expr = E_Variable(name)

			elif isinstance(e.index, E_Literal):  #
				expr = E_Variable(name, e.index)

			elif isinstance(e.index, E_Variable) and (e.index.index is None):  # simple var

				(_init, _tmps, _e) = self._process_expr(fn, e.index)
				append(init, _init)
				append(tmps, _tmps)

				expr = E_Variable(name, _e)

			else:
				tmp = self.tmp_pool.acquire()

				(_init, _tmps, _e) = self._process_expr(fn, e.index)
				append(init, _init)
				append(tmps, _tmps)
				append(tmps, tmp)

				s = self._mk_assign(tmp, _e)
				init.append(s)

				expr = E_Variable(name, E_Variable(tmp))

		elif isinstance(e, E_Call):
			if e.name in self.builtin_fn:
				# a builtin func
				(_init, _tmps, args) = self._prepare_builtin_func_args(fn, e.args)
				append(init, _init)
				append(tmps, _tmps)

				expr = E_Call(e.name, args)
			else:
				# user func
				append(init, self._call_user_func(fn, e.name, e.args))

				tmp = self.tmp_pool.acquire()
				append(init, self._mk_assign(tmp, '__retval'))

				expr = E_Variable(tmp)

				self.functions_called.append(e.name)

		elif isinstance(e, E_Literal) or isinstance(e, E_Operator):
			expr = e

		else:
			print('WARN: Unhandled expression %s (type %s)' % (e, type(e)))

		# TODO: handle other stuff?

		return (init, tmps, expr)


	def _call_user_func(self, fn, name, args):
		""" Generate statements for calling a user function.
		__retval may contain the return value, if any.

		Args:
			fn (S_Function): Function wrapping the call
			name (str): Name of the called function
			args (Expression[]): array of original arguments

		Returns:
			list of statements

		"""
		if not name in self.user_fn:
			raise Exception('Call to undefined function %s()' % name)

		out = []
		tmps = []

		append(out, S_Comment('CALL: %s()' % name))

		# magic functions
		if name == 'reset':
			return self._mk_goto('__reset')

		elif name == 'end':
			self._halt_used = True
			return self._mk_goto('__halt')

		elif name == 'push':

			(_init, _tmps, a_val) = self._process_expr(fn, args[0])
			append(out, _init)
			append(tmps, _tmps)

			append(out, self._mk_push(a_val))

		elif name == 'pop':

			if not isinstance(args[0], E_Variable):
				raise Exception('Cannot pop to %s (type %s)' % (args[0], type(args[0])))

			(_init, _tmps, a) = self._process_expr(fn, args[0])
			append(out, _init)
			append(tmps, _tmps)

			append(out, self._mk_pop(a))

		else:
			# regular user function call
			self.arg_pool.rewind()

			arg_assignments = []

			for a in args:

				arg_name = self.arg_pool.acquire()

				(_init, _tmps, a_val) = self._process_expr(fn, a)
				append(out, _init)
				append(tmps, _tmps)

				append(arg_assignments, self._mk_assign(arg_name, a_val))

			append(out, arg_assignments)

			# get return label index
			return_idx = self.fn_pool.register_call()

			# callee address
			addr = self.fn_pool.get_addr(name)
			append(out, self._mk_assign('__addr', addr))
			append(out, self._mk_push(return_idx))
			append(out, self._mk_goto('__trampoline'))

			# return label
			lbl = self.fn_pool.get_call_label(return_idx)
			append(out, self._mk_label(lbl))

			self._fn_release_tmps(fn, tmps)

		return out


	def _prepare_builtin_func_args(self, fn, orig_args):
		"""
		Prepare arguments for a builtin function call

		Args:
			fn (S_Function): wrapping function - decorated
			orig_args (Expression[]): original arguments

		Returns:
			(_init, _tmps, args)
			_init ... statements used to init the arguments (tmp code)
			_tmps ... list of used tmp variables
			args ... output arguments

		"""

		args = []
		out = []
		tmps = []
		for a in orig_args:
			(_init, _tmps, a_val) = self._process_expr(fn, a)
			append(out, _init)
			append(tmps, _tmps)

			if isinstance(a_val, E_Group):
				# must use helper tmp
				tmp = self.tmp_pool.acquire()
				append(tmps, tmp)
				append(out, self._mk_assign(tmp, a_val))

				a_val = E_Variable(tmp)

			args.append(a_val)

		return (out, tmps, args)


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
		""" Add meta fields to a function statement

		Args:
			fn (S_Function): the function

		"""

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

		if type(index) == str:
			index = E_Variable(index)

		if isinstance(name, E_Variable):
			s.var = name
		else:
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


	def _mk_push(self, what):

		out = []
		append(out, self._mk_assign('__sp', 1, op='-='))

		if self.do_check_stack_bounds:
			append(out, synth("""
				if(__sp < %d) goto __err_so;
			""" % self.stack_start))

		append(out, self._mk_assign('ram', what, index='__sp'))
		return out


	def _mk_pop(self, name):

		out = []

		if self.do_check_stack_bounds:
			append(out, synth("""
				if(__sp > %d) goto __err_su;
			""" % self.stack_end))

		append(out, self._mk_assign(name, E_Variable('ram', E_Variable('__sp'))))
		append(out, self._mk_assign('__sp', 1, op='+='))
		return out


	def _mk_error(self, message):

		return synth("""
			echo("%s");
			goto __reset;
		""" % message)


	def _mk_echo(self, message):

		return synth('echo("%s");' % message)


	def _banner(self, text, fill='-', length=60):
		""" Show a banner line """
		blob = (fill*length + ' ' + text + ' ' + fill*length)
		overlap = len(blob)-80
		return S_Comment(blob[ math.floor(overlap/2) : math.floor(-overlap/2)])

