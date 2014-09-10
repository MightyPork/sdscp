#!/bin/env python3


def append(arr, added):
	""" Append to array, both array or item """

	if (added is None) or (arr is None):
		return

	if type(added) == list:
		arr.extend(added)
	else:
		arr.append(added)


class CompatibilityError(SyntaxError):
	""" Error caused by incompatibility of the source code
	with SDS-C target syntax. The code may be valid, but not
	supported by the compiler.
	"""


class Obj(object):
	""" Anonymous attribute bundle """

	def __init__(self, **kwargs):
		self.__dict__.update(kwargs)


class SyntaxNode:
	""" Abstract syntactical node.

	Attributes:
		parent (Statement):
			reference to parent statement, used for refactoring.

	"""

	def __init__(self):
		self.parent = None


	def bind_parent(self, parent):
		""" Bind parent statement to this statement,
		bind also child statements.

		"""

		self.parent = parent
		self._bind_children()


	def _bind_children(self):
		""" Bind self to children as parent. """

		pass  # stub


	def get_parent(cls=None):
		""" Get parent of given type (skips all parents of different types)

		Args:
			cls (Class): required class for the parent

		Returns: parent of the given type
		Throws: error if no such parent found.

		"""

		if self.parent is None:
			raise Exception('No parent of type %s found!' % str(cls))

		if isinstance(self.parent, cls):
			return self.parent

		return self.parent.get_parent(cls)

