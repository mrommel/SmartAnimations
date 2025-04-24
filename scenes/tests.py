import os
import shutil

from django.test import TestCase


class SassProcessorTest(TestCase):

	def setUp(self):
		super(SassProcessorTest, self).setUp()
		try:
			os.mkdir(settings.STATIC_ROOT)
		except OSError:
			pass

	def tearDown(self):
		shutil.rmtree(settings.STATIC_ROOT)

	def test_sass_processor(self):
		from sass_processor.processor import sass_processor

		css_file = sass_processor('scenes/css/bootstrap/bootstrap.scss')
		self.assertEqual('/static/tests/css/bluebox.css', css_file)
		css_file = os.path.join(settings.STATIC_ROOT, 'scenes/css/bootstrap/bootstrap.scss')
		self.assertTrue(os.path.exists(css_file))
		with open(css_file, 'r') as f:
			output = f.read()
		expected = '.bluebox{background-color:#0000ff;margin:10.0px 5.0px 20.0px 15.0px;color:#fa0a78}\n\n/*# sourceMappingURL=bluebox.css.map */'
		self.assertEqual(expected, output)
