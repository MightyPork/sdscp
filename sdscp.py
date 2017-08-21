#!/bin/env python3

import sys
import argparse
import math
import re
import traceback

from directives import DirectiveProcessor, D_Pragma
from tokens import Tokenizer
from renderers import *
from sdscp_errors import *
import statements
import getpass

VERSION = '1.5.0'

# ==================== Command Line Arguments processing =======================

parser = argparse.ArgumentParser(
	description='SDS-C macro preprocessor v%s' % VERSION,
	formatter_class=argparse.RawDescriptionHelpFormatter,
	epilog="""
+-------------------------------------------------------+
| For bug reporting and more info, please visit:        |
|   https://github.com/MightyPork/sdscp                 |
|                                                       |
| Complete documentation in Czech can be viewed here:   |
|   https://goo.gl/mZ1oOg  (Google Docs)                |
|                                                       |
| SDSCP (c) Ondřej Hruška, 2014-2017                    |
+-------------------------------------------------------+
"""
	)

parser.add_argument(
		'source',
		help='The source file to process'
)

parser.add_argument(
		'-V', '--version',
		help='Show the SDSCP version.',
		action='version',
		version=VERSION
)

parser.add_argument(
		'-o', '--output',
		help='The output file; %%v in the name will be replaced with the \
		      program\'s version. To just print the output, use -d instead.',
		action='store',
)

parser.add_argument(
		'-p', '--pragma',
		help='Set a pragma value (syntax like #pragma). All pragmas are \
		      also accessible to the program as defines named __NAME__',
		action='append',
		nargs='+',
		default=[]
)

parser.add_argument(
		'-d', '--display',
		action='store_true',
		default=False,
		help='Show the final source (Works together with -o)'
)

parser.add_argument(
		'-v', '--verbose',
		action='store_true',
		default=False,
		help='Show all optional debug info.'
)

parser.add_argument(
		'-G', '--show-generated',
		action='store_true',
		default=False,
		help='Show the code generated from statements.'
)

parser.add_argument(
		'-O', '--show-original',
		action='store_true',
		default=False,
		help='Show original source (only main file)'
)

parser.add_argument(
		'-M', '--show-macros',
		action='store_true',
		default=False,
		help='List all macros'
)

parser.add_argument(
		'-R', '--show-resolved',
		action='store_true',
		default=False,
		help='Show code after processing includes and # branching.'
)

parser.add_argument(
		'-P', '--show-processed',
		action='store_true',
		default=False,
		help='Show code after replacing macros'
)

parser.add_argument(
		'-T', '--show-tokens',
		action='store_true',
		default=False,
		help='Show tokens (source divided to pieces).'
)

parser.add_argument(
		'-S', '--show-statements',
		action='store_true',
		default=False,
		help='Show statements (high-level code abstraction).'
)

parser.add_argument(
		'-x', '--error-trace',
		action='store_true',
		default=False,
		help='Show stack trace for SDSCP syntax errors (for debugging)'
)

args = parser.parse_args()


SRC		= args.source
DEST	= args.output


SHOW_ORIGINAL	= args.verbose or args.show_original

SHOW_RESOLVED	= args.verbose or args.show_resolved
SHOW_MACROS		= args.verbose or args.show_macros
SHOW_PROCESSED	= args.verbose or args.show_processed
SHOW_TOKENS		= args.verbose or args.show_tokens
SHOW_STATEMENTS	= args.verbose or args.show_statements
SHOW_GENERATED	= args.verbose or args.show_generated
SHOW_OUTPUT		= args.verbose or args.display

SHOW_STRACE     = args.error_trace

pragmas_args = {}

for p in args.pragma:
	pr = D_Pragma('#pragma ' + ' '.join(p))
	pragmas_args[pr.name] = pr.value


# ==================== Utils =======================


def banner(text, fill='-', length=80):
	""" Show a banner line """
	blob = (fill*length + ' ' + text + ' ' + fill*length)
	overlap = len(blob)-80
	print('\n' + blob[ math.floor(overlap/2) : math.floor(-overlap/2)] + '\n')


def prep4disp(code):
	c = '  ' + re.sub(r'\n', '\n  ', code)
	c = re.sub(r'\t', '    ', c)
	return c


# ==================== MAIN TASK =======================

try:
	banner('SDS-C Preprocessor', ':')

	print('Reading file:', SRC)

	# read the file
	dproc = DirectiveProcessor(SRC, pragmas_args)

	if SHOW_ORIGINAL:
		banner('SOURCE', '-')
		print(prep4disp( dproc.source ) + '\n')

	# ---------------- Resolve directives ------------------

	print('Resolving directives...')
	# include files, resolve branching, find macros...
	dproc.process()


	# -------------------- Apply macros --------------------

	pragmas = dproc.get_pragmas()

	pragmas['main_file'] = SRC
	pragmas['sdscp_version'] = VERSION

	if 'name' not in pragmas.keys():
		pragmas['name'] = SRC

	if 'author' not in pragmas.keys():
		try:
			pragmas['author'] = getpass.getuser()
		except Exception:
			pass


	if SHOW_MACROS:
		banner('MACROS', '-')
		print('List of all found macros, in definition order:\n')
		for d in dproc.get_defines().values():
			for m in d:
				print('  ' + str(m))
		print()

		banner('PRAGMAS', '-')
		print('List of all #pragma config key-value pairs\n')
		for (k, v) in dproc.get_pragmas().items():
			print('%s = %s' % (k, v))

		print()


	if SHOW_RESOLVED:
		banner('RESOLVED', '-')
		print('Code after resolving includes, # branching, and extracting macros:\n')
		print(prep4disp( dproc.get_output() ) + '\n')

	print('Applying macros...')
	# perform macro replacements
	dproc.apply_macros()
	# get output code
	processed = dproc.get_output()


	if SHOW_PROCESSED:
		banner('PROCESSED', '-')
		print('Code after replacing macros:\n')

		print(prep4disp(processed) + '\n')


	print('Tokenizing code...')
	tk = Tokenizer(processed)
	tokens = tk.tokenize()
	sts = statements.parse(tokens)


	if SHOW_TOKENS:
		banner('TOKENIZED', '-')
		print('Tokenization of the processed code:\n')
		tk.show()
		print('')


	if SHOW_STATEMENTS:
		banner('STATEMENTS', '-')
		print('Source code abstraction:\n')


		for s in sts:
			print(str(s))


	if SHOW_GENERATED:
		banner('GENERATED', '-')
		print('Code generated from statements:\n')

		rndr = CSyntaxRenderer(sts)
		print(prep4disp(rndr.render()))


	if DEST != None or SHOW_OUTPUT:

		# perform tweaks to match some of SDS-C's broken syntax

		rtype = pragmas.get('renderer', 'asm')

		if rtype in ['sds', 'simple']:
			rtype = 'simple'
			rndr = SimpleSdsRenderer(sts)
		elif rtype in ['sds2', 'asm']:
			rtype = 'asm'
			rndr = AsmSdsRenderer(sts)
		elif rtype in ['debug']:
			rndr = CSyntaxRenderer(sts)
		else:
			raise Exception('Unknown renderer: "%s"' % rtype)

		rndr.set_pragmas(pragmas)

		print('Rendering to SDS-C using "%s" renderer...' % rtype)
		for_sds = rndr.render()

		if SHOW_OUTPUT:
			banner('OUTPUT SDS-C CODE', '-')
			print(prep4disp(for_sds) + '\n')

		if DEST != None:
			if 'version' in pragmas:
				DEST = DEST.replace("%V", pragmas.get('version'))
			print('Writing to file: %s' % DEST)
			f = open(DEST, 'w')
			f.write(for_sds)
			f.close()
		else:
			print('No output file specified.')

	print('\nDone.\n')

except Exception as e:
	errname = type(e).__name__
	disp_errname = errname

	is_custom = False

	if errname == 'SdscpSyntaxError':
		disp_errname = 'SYNTAX ERROR'
		is_custom = True

	elif errname == 'CompatibilityError':
		disp_errname = 'COMPATIBILITY ERROR'
		is_custom = True
	elif errname == 'IsADirectoryError':

		disp_errname = 'INVALID INPUT FILE'
		is_custom = True

	elif errname == 'FileNotFoundError':
		disp_errname = 'FILE NOT FOUND'
		is_custom = True

	else:
		disp_errname = 'COMPILATION FAILED'

	banner(disp_errname, '#')

	# Extra debug info requested
	if SHOW_STRACE or not is_custom:
		type_, value_, traceback_ = sys.exc_info()
		ex = traceback.format_exception(type_, value_, traceback_)
		for line in ex:
			# discard useless junk
			if (('raise %s' % errname) in line) or ('File "<string>", line None' in line):
				continue
			print(line)
	else:
		print(str(e) + '\n')
		print('To see debug info, please use the -x flag.\n')
