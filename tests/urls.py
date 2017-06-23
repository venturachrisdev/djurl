#Test

import sys

if sys.version_info >= (2,7):
	import unittest
else:
	from django.utils import unittest

from djurl import register_pattern, Djurl

def build(pattern, exact=True):
		return Djurl(pattern, exact=exact).build()

class TestRegexBuilding(unittest.TestCase):

	def test_building_without_pattern(self):
		"""
		If it's not broken, don't fix it.
		Testing: If I don't provide a pattern to replace in my route, Djurl doesn't need
		to touch it. Just adding '^' and|or '$' if they weren't provided. Also, if you provide a pattern not registed in djurl default pattern, the library should keep it there and not parse it.
		"""
		self.assertEqual(build('^$'), '^$')
		self.assertEqual(build('^blog/$'), '^blog/$')
		self.assertEqual(build('^me/15/$'), '^me/15/$')
		self.assertEqual(build('^father/', exact=False), '^father/')
		self.assertEqual(build('comments/:comment'), '^comments/:comment/$')
		self.assertEqual(build('/', exact=False), '^')
		self.assertEqual(build('^*.jpg|png|gif|jpeg$'), '^*.jpg|png|gif|jpeg$')
		self.assertEqual(build('^/', exact=False), '^/')

	def test_strip_slashes_at_beginning(self):
		"""
		When you're working with a Django url, you don't use '/' at the beginning of the
		route, you start with '^' instead. If we are not working with regex, it's common
		to put '/' at the beginning of a route. Djurl should strip that slashes so the translation to django urlpatterns becomes easy.
		"""
		self.assertEqual(build('/about'), '^about/$')
		self.assertEqual(build('/hello/world'), '^hello/world/$')
		self.assertEqual(build('/articles/:article/comments/:comment', exact=False), '^articles/:article/comments/:comment')
		self.assertEqual(build('/me', exact=False), '^me')

	def test_add_slash_at_end_for_exact_routes(self):
		"""
		The exact url only matches with one path. Example: '^hello$' only matches with 'hello', not with 'hhello', 'helloo' nor, '.hello'. So we could say, it doesn't matter if an exact route ends with '/' because only will matches with one path ('^hello$' or '^hello/$' don't match with '/hello/3').
		But if our route is not exact. Then should be able to match with more than one path. Example: '^hello' matches with 'hellooooo', hello/4', 'hello/hello/h' and so on.
		Then, we should only add a '/' if it's an exact pattern.
		"""
		self.assertEqual(build('/about'), '^about/$')
		self.assertEqual(build('/about/'), '^about/$')
		self.assertEqual(build('/about', exact=False), '^about')
		self.assertEqual(build('/about/', exact=False), '^about/')

	def test_normalize_url(self):
		self.assertEqual(build(''), '^$')
		self.assertEqual(build('/'), '^$')
		self.assertEqual(build('hello/world'), '^hello/world/$')
		self.assertEqual(build('/hello/world'),'^hello/world/$')
		self.assertEqual(build('/hello/world', exact=False), '^hello/world')

		self.assertEqual(build('/articles'), build('articles'))
		self.assertEqual(build('  news/today  '), build('news/today'))
