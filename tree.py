#!/bin/env python3


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
