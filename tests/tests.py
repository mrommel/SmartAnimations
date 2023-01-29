""" unittest module """
import unittest

from animations.models import AnimationModel, ObjectType, ObjectModel, AnimationType, ObjectAnimationModel


class TestBasic(unittest.TestCase):
	def test_constructor(self):
		"""Test the  constructor"""

		self.assertEqual(2 + 2, 4)
