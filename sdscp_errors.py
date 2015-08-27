#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class SdscpSyntaxError(Exception):
	""" A syntax error in source code """
	pass

class CompatibilityError(SyntaxError):
	""" Error caused by incompatibility of the source code
	with SDS-C target syntax. The code may be valid, but not
	supported by the compiler.
	"""
	pass
