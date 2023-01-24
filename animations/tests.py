""" unittest module """
import unittest


class TestBasic(unittest.TestCase):
	def test_constructor(self):
		"""Test the  constructor"""

		self.assertEqual(2 + 2, 4)
