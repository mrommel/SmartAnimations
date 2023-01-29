""" unittest module """
import unittest

from animations.models import AnimationModel


class TestBasic(unittest.TestCase):
	def test_constructor(self):
		"""Test the  constructor"""

		self.assertEqual(2 + 2, 4)


class TestBasic2(unittest.TestCase):
	def test_constructor(self):
		"""Test the  constructor"""

		animation = AnimationModel()
		animation.name = 'dummy'
		animation.width = 100
		animation.height = 100
		animation.start = 0
		animation.end = 10