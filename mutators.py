#!/bin/env python3

import statements
from tokens import Tokenizer
from statements import *
from expressions import *
from utils import *
from sdscp_errors import *

# for evaluation of expr
import renderers
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


	def read_pragmas(self, pragmas):
		""" The mutator here can configure itself based on pragmas """
		pass


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
			append(processed, self._add_braces(s))

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


class M_RemoveDeadCode(Mutator):
	""" Removes obvious dead code, unused labels etc. """

	def read_pragmas(self, pragmas):
		self.keep_banner_comments = pragmas.get('comments', True)


	def _transform(self, code):

		print('Removing dead code...')
		p = 1
		while True:
			print('Cleaning: Pass %d' % p)
			p += 1

			self.removed = False
			self.used_labels = set()
			self.existing_labels = set()

			self.do_rm_labels = False
			code = self._rm_dead(code)

			self.do_rm_labels = True
			code = self._rm_dead(code)

			if not self.removed:
				break

		return code


	def _rm_dead(self, code):
		out = []

		was_alone = isinstance(code, Statement)

		if was_alone:
			code = [code]

		length = len(code)

		i = 0
		while i < length:

			s = code[i]

			if type(s) is S_Label:
				self.existing_labels.add(s.name)

				if self.do_rm_labels:
					if s.name not in self.used_labels:
						i += 1 # skip
						self.removed = True
						# print('INFO: Removing unused label %s' % s.name)
						continue

			if type(s) is S_Goto:
				self.used_labels.add(s.name)

				if self.do_rm_labels:
					if s.name not in self.existing_labels:
						raise SdscpSyntaxError('GOTO to undefined label %s!' % s.name)

				# Discard all until next label.
				# If the label is the target for this goto, discard the goto too.

				cmt = None

				j = i
				while j < length:
					j += 1

					if j == length:
						out.append(s)
						# print('eof, appending '+str(s))
						i = j + 1
						break

					ss = code[j]
					# print('ss code[j] ' + str(ss))

					# UGLY HACK to avoid removing of FUNC banner comments.
					if self.keep_banner_comments:
						if type(ss) is S_Comment and 'FUNC' in ss.text:
							out.append(s)
							out.append(ss)
							i = j
							break

					if type(ss) is S_Label:

						if self.do_rm_labels and ss.name not in self.used_labels:
							self.removed = True
							continue

						if ss.name == s.name:
							self.removed = True
						else:
							append(out, s)
							if j > i + 1:
								self.removed = True

						out.append(ss)
						self.existing_labels.add(ss.name)

						i = j

						break

			elif type(s) is S_If:
				# go into if's branches
				s.then_st = self._rm_dead(s.then_st)
				s.else_st = self._rm_dead(s.else_st)
				out.append(s)

			elif isinstance(s, S_Block):
				# handle block contents
				s.children = self._rm_dead(s.children)
				out.append(s)

			elif (isinstance(s, S_For) or
				isinstance(s, S_While) or
				isinstance(s, S_Switch) or
				isinstance(s, S_Function) or
				isinstance(s, S_DoWhile)):

				s.body_st = self._rm_dead(s.body_st)
				out.append(s)

			else:
				out.append(s)

			i += 1  # advance counter

		# collapse if was single at start
		if was_alone:
			if len(out) == 0:
				return S_Empty()
			elif len(out) == 1:
				return out[0]
			else:
				s = S_Block()
				s.children = out
				return s
		else:
			return out


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
				raise CompatibilityError('Illegal statement in root scope: %s' % str(s))

		return variables + functions



class TmpVarPool:
	""" Pool of temporary variables """

	def __init__(self):
		self.used_cnt = 0
		self.locks = {}


	def _gen_name(self, index):
		return "__t%d" % (index)


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
		return "__a%d" % (index)


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

		# function name to index
		self.fnname2fnindex = {}

		# function index to name
		self.fnindex2fnname = {}

		# name of retpos for call with given index
		self.callindex2calllabel = {}

		self.label_pool = label_pool

		# index of call -> function name
		self.callindex2fnname = {}

		# call index 2 origin func name
		self.callindex2origin = {}

		self.call_counter = 1

		self.function_labels = {}

		self.gr = None  # reference to Grande Mutator


	def register(self, name):
		""" Register a function. Returns index. """

		i = self.counter

		self.fnname2fnindex[name] = i
		self.fnindex2fnname[i] = name

		begin = self.get_begin(i)
		end = self.get_end(i)

		self.label_pool.register(begin)
		self.label_pool.register(end)

		self.function_labels[i] = [begin, end]

		self.counter += 1
		return i


	def register_call(self, called, from_):
		""" Register a call. Returns index. """

		i = self.counter
		label = self.get_call_label(i)

		self.callindex2calllabel[i] = label

		self.label_pool.register(label)
		self.callindex2fnname[i] = self.get_name(called)
		self.callindex2origin[i] = from_

		self.counter += 1;

		return i


	def get_begin(self, index):
		""" Get start label for a function

		Args:
			index: name or function index

		Returns:
			label name

		"""

		if self.gr is not None and self.gr.do_preserve_names:
			name = index

			if type(index) == str:
				index = self.fnname2fnindex[index]
			else:
				name = self.fnindex2fnname[index]

			return "__fn%s_%s" % (index, name)

		else:
			if type(index) == str:
				index = self.fnname2fnindex[index]

			return "__fn%s" % index


	def get_end(self, index):
		""" Get end label of a function (for return)

		Args:
			index: name or function index

		Returns:
			label name

		"""

		if type(index) == str:

			if index == 'main':
				return '__main_loop_end';

			if index == 'init':
				return '__init_end';

			index = self.fnname2fnindex[index]

		return "__fn%d_end" % index


	def get_ns_label(self, index, label):
		""" Get namespaced label in function

		Args:
			index: name or function index
			label: label name

		Returns:
			label name with namespace prefix

		"""

		if index == 'main' or index == 'init':
			return "__fn%sL_%s" % (index, label)

		if type(index) == str:
			index = self.fnname2fnindex[index]

		return "__fn%sL_%s" % (index, label)


	def get_call_label(self, index):
		""" Get return-from-call label

		Args:
			index: index of the call

		Returns:
			label name

		"""

		return "__rp%s" % index


	def get_fn_addr(self, name):
		""" Get address for name """

		if not name in self.fnname2fnindex.keys():
			raise SdscpSyntaxError('Function not found, cannot call: %s' % name)

		return self.fnname2fnindex[name]


	def get_name(self, addr):
		""" Get name from address """

		if not addr in self.fnindex2fnname.keys():
			if addr in self.callindex2fnname.keys():
				return self.callindex2fnname[addr]
			else:
				return None

		return self.fnindex2fnname[addr]



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

		self._halt_used = False


	def read_pragmas(self, pragmas):
		self.do_check_stack_bounds	= pragmas.get('safe_stack', True)
		self.stack_start			= pragmas.get('stack_start', 300)
		self.stack_end				= pragmas.get('stack_end', 511)
		self.do_preserve_names		= pragmas.get('keep_names', False)
		self.add_debug_trace_logging = pragmas.get('show_trace', False)


	def _transform(self, code):

		self.globals_declare = []
		self.globals_assign = []
		self.globals_vars = set()
		self.global_rename = {}

		functions = []
		self.user_fn = set()

		self.tmp_pool = TmpVarPool()
		self.arg_pool = ArgPool()
		self.label_pool = LabelPool()
		self.fn_pool = FnRegistry(self.label_pool)
		self.fn_pool.gr = self

		self.functions_called = set()

		self.labels_used = set()

		init_userfn = None
		main_userfn = None

		# register helper vars
		self._add_global_var('__rval')  # return value
		self._add_global_var('__sp', self.stack_end + 1)  # stack pointer at RAMEND (grows towards lower addrs)
		self._add_global_var('__addr')  # jump address pointer

		# iterate through top level statements
		for s in code:
			if isinstance(s, S_Var):
				self._add_global_var(s.var.name, s.value, user=True)

			elif isinstance(s, S_Function):

				if s.name in self.user_fn:
					raise SdscpSyntaxError('Duplicate function: %s()' % s.name)

				self.user_fn.add(s.name)

				if s.name == 'main':
					main_userfn = s

				elif s.name == 'init':
					init_userfn = s

				else:
					self.user_fn.add(s.name)
					functions.append(s)
					self.fn_pool.register(s.name)

			else:
				raise SdscpSyntaxError('Illegal statement in root scope: %s' % s)

		if main_userfn is None:
			raise SdscpSyntaxError('Missing main function!')

		# process init()
		pr_init = None
		if init_userfn is not None:
			pr_init = self._process_fn(init_userfn, naked=True)

		pr_main = self._process_fn(main_userfn, naked=True)

		# process user functions except main() & init()
		pr_userfuncs = {}
		for fn in functions:
			# now we get
			pr_userfuncs[fn.name] = self._process_fn(fn)

		# find out what funcs are needed
		_labels = set()
		_gotos = set()
		_calls = set()


		_labels.update(pr_main.labels)
		_calls.update(pr_main.calls)
		_gotos.update(pr_main.gotos)

		if pr_init is not None:
			_labels.update(pr_init.labels)
			_calls.update(pr_init.calls)
			_gotos.update(pr_init.gotos)

		_unresolved_calls = set()
		_unresolved_calls.update(_calls)
		# _unresolved_calls.remove('main')
		# _unresolved_calls.remove('init')

		_resolved_calls = set()
		# _resolved_calls.add('main')
		# _resolved_calls.add('init')

		try:
			while len(_unresolved_calls) > 0:
				for name in list(_unresolved_calls):
					if name in _resolved_calls:
						continue

					fn = pr_userfuncs[name]
					_resolved_calls.add(name)
					_unresolved_calls.remove(name)

					_labels.update(fn.labels)
					_calls.update(fn.calls)
					_gotos.update(fn.gotos)

					_unresolved_calls.update(_calls.difference(_resolved_calls))

		except KeyError as e:
			raise Exception('Error while resolving calls', e)

		self.used_labels = _gotos
		self.defined_labels = _labels

		_calls.add('main')
		_calls.add('init')
		self.functions_called = _calls


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
		append(sts, S_Comment('Disable speed limit'))
		append(sts, synth('sys[63] = 128;'))


		append(sts, self._mk_label('__reset'))
		append(sts, self._mk_echo('[INFO] Program reset.'))
		append(sts, self._banner('FUNC: init()'))
		append(sts, self._mk_label('__init'))
		append(sts, self._mk_echo('[INFO] Initialization...'))

		# assign global vars default values
		append(sts, self.globals_assign)

		# user init function
		if init_userfn is not None:
			append(sts, pr_init.code)

		append(sts, self._mk_label('__init_end'))

		# infinite main loop
		append(sts, self._banner('FUNC: main()'))
		append(sts, self._mk_echo('[INFO] main() started.'))
		append(sts, self._mk_label('__main_loop'))

		if main_userfn is not None:
			append(sts, pr_main.code)

		append(sts, self._mk_label('__main_loop_end'))
		append(sts, self._mk_goto('__main_loop'))


		# other user functions (already processed)
		for name in _resolved_calls:
			func = pr_userfuncs[name]
			append(sts, func.code)
			append(sts, self._build_trampoline_for_func(func.name))


		# ERRORS
		append(sts, self._build_error_handlers())

		if self._halt_used:
			# Shutdown trap
			append(sts, self._build_shutdown_trap())


		# compose main function with all the code
		main = S_Function()
		main.name = 'main'
		main.body_st = S_Block()
		main.body_st.children = sts

		output_code.append(main)

		return output_code


	def _build_trampoline_for_func(self, name):
		""" Build redirection vector for return from func """

		sts = []
		append(sts, self._mk_pop('__addr'))  # pop a return address

		rpvm = self.fn_pool.callindex2calllabel

		for (i, called_name) in self.fn_pool.callindex2fnname.items():
			if called_name == name:
				# print('Func %s called with RP %d' % (name, i))

				origin = self.fn_pool.callindex2origin[i]

				if not origin in self.functions_called:
					# print('Discarding return to call in unused func %s' % origin)
					continue

				n = rpvm.get(i)

				append(sts, synth("""
					if (__addr == %d) goto %s;
				""" % (i, n)))

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
			out = []

			if self.add_debug_trace_logging:
				append(out, synth("""
					echo("[TRACE] in %s()");
				""" % fn.name))

			append(out, self._process_block(fn, fn.body_st.children))
			return self._compose_func_obj(fn, out)

		body = []

		self.arg_pool.rewind()

		passed_arg_names = []

		if len(fn.args) > 0:
			# assign arguments to tmps
			append(body, S_Comment('Store args to tmp vars'))
			for n in fn.args:
				arg = self.arg_pool.acquire()
				tmp = self.tmp_pool.acquire()
				fn.meta.changed_tmps.append(tmp)
				fn.meta.local_tmp_dict[n] = tmp
				fn.meta.arg_tmps.append(tmp)

				append(passed_arg_names, arg)

				append(body, self._mk_assign(tmp, arg))


		if self.add_debug_trace_logging:
			argstr = ''

			for i in range(0, len(passed_arg_names)):

				argstr += ['", ', '"'][i==0] + '%s=", %s, ' % (fn.args[i], passed_arg_names[i])

			append(body, synth('echo("[TRACE] in: %(name)s(", %(params)s ")");' % {
				'name': fn.name,
				'params': argstr
			}))

		append(body, self._mk_assign('__rval', 0))

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

		if self.add_debug_trace_logging:
			append(out, synth('echo("[TRACE] return from %(name)s, with: ", %(rval)s);' % {
				'name': fn.name,
				'rval': '__rval'
			}))

		append(out, S_Comment('Return to caller'))
		# append(out, self._mk_goto('__r_vect'))

		return self._compose_func_obj(fn, out)


	def _compose_func_obj(self, fn, code):

		ret = Obj()
		ret.name = fn.name
		ret.code = code
		ret.labels = fn.meta.labels
		ret.gotos = fn.meta.gotos
		ret.calls = fn.meta.calls

		return ret


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
				S_Goto:		self._transform_goto,
				S_Block:	self._transform_alone_block,
				S_Label:	self._transform_label,
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
			transformer = None

			try:
				transformer = self._statement_transformers[type(s)]
			except KeyError:
				print('WARN: Unhandled statement %s (type %s)' % (s, type(s)))
				append(out, s)
				continue

			if transformer is not None:
				(_init, _tmps) = transformer(fn, s)
				append(out, _init)
				self._fn_release_tmps(fn, _tmps)

		return out


	def _transform_noop(self, fn, s):
		""" No change """
		return (s, [])


	def _transform_alone_block(self, fn, s):
		""" Transform the insides """
		return (self._process_block(fn, s), [])


	def _transform_goto(self, fn, s):

		s.name = self.fn_pool.get_ns_label(fn.name, s.name)

		self.labels_used.add(s.name)
		fn.meta.gotos.add(s.name)

		return (s, [])

	def _transform_label(self, fn, s):

		s.name = self.fn_pool.get_ns_label(fn.name, s.name)
		fn.meta.labels.add(s.name)

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

		fn.meta.changed_tmps.append(repl)

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
			raise SdscpSyntaxError('Cannot assign to %s (type %s)' % (args[0], type(args[0])))

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
			self.functions_called.add(s.name)

		return (out, tmps)


	def _transform_return(self, fn, s):
		out = []
		tmps = []

		(_init, _tmps, rval) = self._process_expr(fn, s.value)
		append(out, _init)
		append(tmps, _tmps)

		# This really shouldn't be in mutator, but in renderer
		# it can't provide good debugging info
		if type(rval) is E_Literal and rval.is_string():
			raise CompatibilityError('Can\'t return a string literal, at: %s' % str(rval))

		append(out, self._mk_assign('__rval', rval))
		append(out, self._mk_goto(self.fn_pool.get_end(fn.name)))

		return (out, tmps)


	def _transform_if(self, fn, s):
		out = []
		tmps = []

		(_init, _tmps, cond) = self._process_expr(fn, s.cond)
		append(out, _init)
		append(tmps, _tmps)

		if type(s.cond) is E_Literal:
			if int(str(s.cond)) == 0:
				# always False
				append(out, S_Comment('(IF always false: else only)'))
				append(out, self._process_block(fn, s.else_st))
			else:
				# always True
				st = s.then_st
				append(out, S_Comment('(IF always true: then only)'))
				append(out, self._process_block(fn, s.then_st))
		else:
			ss = S_If()
			ss.cond = cond
			ss.then_st = S_Block()
			ss.then_st.children = self._process_block(fn, s.then_st)
			ss.else_st = S_Block()
			ss.else_st.children = self._process_block(fn, s.else_st)
			append(out, ss)

		return (out, tmps)


	def _transform_while(self, fn, s):
		out = []
		tmps = []

		append(out, S_Comment('WHILE begin'))

		l_continue = self.label_pool.acquire('wh_cont')
		l_body = self.label_pool.acquire('wh_body')
		l_break = self.label_pool.acquire('wh_break')

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

		l_continue = self.label_pool.acquire('dowh_cont')
		l_body = self.label_pool.acquire('dowh_body')
		l_break = self.label_pool.acquire('dowh_break')

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

		l_continue = self.label_pool.acquire('for_cont')
		l_cond = self.label_pool.acquire('for_test')
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

		parent_func = None
		p = s
		while True:
			p = p.get_parent()

			if p is None:
				raise SdscpSyntaxError('Break outside loop or switch! (In function: %s)' % parent_func.name)

			if type(p) in [S_For, S_While, S_DoWhile, S_Switch]:

				# a loop or switch
				append(out, self._mk_goto(p.meta.l_break))
				break

			# for error reporting
			if type(p) is S_Function:
				parent_func = p

		return (out, [])


	def _transform_continue(self, fn, s):
		out = []

		parent_func = None
		p = s
		while True:
			p = p.get_parent()

			if p is None:
				raise SdscpSyntaxError('Continue outside loop! (In function: %s)' % parent_func.name)

			if type(p) in [S_For, S_While, S_DoWhile]:

				# a loop or switch
				append(out, self._mk_goto(p.meta.l_continue))
				break

			# for error reporting
			if type(p) is S_Function:
				parent_func = p

		return (out, [])


	def _transform_switch(self, fn, s):
		out = []
		tmps = []

		append(out, S_Comment('SWITCH begin'))

		l_break = self.label_pool.acquire('sw_break')

		# add meta to the switch
		s.meta = Obj()
		s.meta.l_break = l_break

		compared = self.tmp_pool.acquire()
		tmps.append(compared)

		# resolve compared value
		(_init, _tmps, cond) = self._process_expr(fn, s.value)
		append(out, _init)
		append(tmps, _tmps)

		append(out, self._mk_assign(compared, cond))

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

		# try to evaluate it
		if not hasattr(self, '_erndr'):
			self._erndr = renderers.CSyntaxRenderer([])

		if type(e) is E_Group:
			try:
				as_str = self._erndr._render_expr(e)
				val = eval_expr(as_str)

				e = E_Literal(T_Number(str(round(val))))

				print('Expression "%s" simplified to "%s"' % (as_str, val))

			except (ValueError, TypeError, SyntaxError, KeyError):
				pass


		if isinstance(e, E_Group):
			new_children = []

			group_with_next = False

			for c in e.children:
				(_init, _tmps, _e) = self._process_expr(fn, c)

				append(init, _init)
				append(tmps, _tmps)
				append(new_children, _e)

			expr = E_Group(new_children)

		elif isinstance(e, E_Variable):

			# translate name to tmp name
			if fn is None:
				name = e.name # global
			else:
				if e.name in fn.meta.local_tmp_dict:
					name = fn.meta.local_tmp_dict[e.name]
				elif e.name in self.global_rename:
					name = self.global_rename[e.name]
				else:
					name = e.name

				if not name in self.builtin_var:
					if not name in self.tmp_pool.get_names():
						if not name in self.globals_vars:
							raise SdscpSyntaxError('Use of undefined variable %s' % name)

			if e.index is None:
				expr = E_Variable(name)

			elif isinstance(e.index, E_Literal):
				expr = E_Variable(name, e.index)

			elif isinstance(e.index, E_Variable) and (e.index.index is None):  # simple var

				# translate var to local tmp
				(_init, _tmps, _e) = self._process_expr(fn, e.index)
				append(init, _init)
				append(tmps, _tmps)

				expr = E_Variable(name, _e)

			else:
				(_init, _tmps, _e) = self._process_expr(fn, e.index)
				append(init, _init)
				append(tmps, _tmps)

				if type(_e) is E_Literal:
					# was evaluated to value
					expr = E_Variable(name, _e)
				else:
					tmp = self.tmp_pool.acquire()

					append(tmps, tmp)

					s = self._mk_assign(tmp, _e)
					append(init, s)

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
				append(init, self._mk_assign(tmp, '__rval'))

				expr = E_Variable(tmp)

				self.functions_called.add(e.name)

		elif isinstance(e, E_Literal) or isinstance(e, E_Operator):
			expr = e

		else:
			print('WARN: Unhandled expression %s (type %s)' % (e, type(e)))

		if type(expr) is E_Group:
			# group parts by operator precedence (SDS-C bug! awww)
			expr.children = self._group_expr_operators(expr.children)

		return (init, tmps, expr)

	def _group_expr_operators(self, exprs):

		# print(str(E_Group(exprs)))

		# 1. group highest level, then lower etc.
		order = ['!', '~', '*', '/', '%', '+', '-', '>>', '<<', '<', '<=', '>', '>=', '==', '!=', '&', '^', '|', '&&', '||']

		for o in order:
			# print('Collecting operator %s' % o)

			if o in ['!', '~']:
				arity = 1
			else:
				arity = 2

			while True:
				out = []
				last2 = None
				last1 = None
				collecting = False
				times = 0
				for e in exprs:
					if type(e) is E_Operator and e.value == o:
						# print('Collecting for %s' % e)

						if last2 is not None:
							append(out, last2)

						if arity == 2:
							if last1 is None:
								last1 = e
								continue

							last2 = last1
						else:
							if last1 is not None:
								append(out, last1)

						last1 = e
						collecting = True

						# print("HIT")
						continue

					if collecting:
						times += 1
						if arity == 2:
							out.append(E_Group([last2, last1, e]))
						else:
							out.append(E_Group([last1, e]))

						collecting = False
						last2 = None
						last1 = None
					else:
						if last2 is not None:
							append(out, last2)

						last2 = last1
						last1 = e

				if last2 is not None:
						append(out, last2)

				if last1 is not None:
						append(out, last1)

				exprs = out

				if times == 0:
					break

			# print(str(E_Group(exprs)))


		return exprs # TODO


	def _call_user_func(self, fn, name, args):
		""" Generate statements for calling a user function.
		__ret may contain the return value, if any.

		Args:
			fn (S_Function): Function wrapping the call
			name (str): Name of the called function
			args (Expression[]): array of original arguments

		Returns:
			list of statements

		"""

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
				raise SdscpSyntaxError('Cannot pop to %s (type %s)' % (args[0], type(args[0])))

			(_init, _tmps, a) = self._process_expr(fn, args[0])
			append(out, _init)
			append(tmps, _tmps)

			append(out, self._mk_pop(a))

		else:
			if not name in self.user_fn:
				raise SdscpSyntaxError('Call to undefined function %s()' % name)

			fn.meta.calls.add(name)

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


			# callee address
			target_fn = self.fn_pool.get_begin(name)

			# get return label index
			addr = self.fn_pool.get_fn_addr(name)
			return_idx = self.fn_pool.register_call(addr, fn.name)

			# append(out, self._mk_assign('__addr', addr))
			append(out, self._mk_push(return_idx))
			append(out, self._mk_goto(target_fn))

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


	def _add_global_var(self, name, value=None, user=False):
		""" Add a global variable; split to declaration & assignment """

		if user:
			if name in self.global_rename.keys():
				raise SdscpSyntaxError('Duplicate global var declaration (%s)' % name)

			if not self.do_preserve_names:
				nm = 'u1'
				cnt=1
				while nm in self.global_rename.values():
					cnt += 1
					nm = 'u%d' % cnt

				self.global_rename[name] = nm
				name = nm
			else:
				if name[:2] == '__':
					# user defined
					nm = 'u'+name
					cnt=1
					while nm in self.global_rename.values():
						nm = 'u'+name+cnt
						cnt += 1

					self.global_rename[name] = nm
					name = nm


		v = self._mk_var(name)
		self.globals_declare.append(v)
		self.globals_vars.add(name)

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

		# list of labels inside the function
		fn.meta.labels = set()

		# list of gotos inside the function
		fn.meta.gotos = set()

		# list of called funcs
		fn.meta.calls = set()

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
		self.labels_used.add(name)
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

