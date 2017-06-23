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
		self.assertEqual(build('home'), build('/home/'))
		self.assertEqual(build('home/user/documents'), build('/home/user/documents/'))
		self.assertEqual(build('  news/today  '), build('news/today'))

	def test_pattern_pk(self):
		self.assertEqual(build('/:pk'), '^(?P<pk>[0-9]+)/$')
		self.assertEqual(build('/articles/:pk'), '^articles/(?P<pk>[0-9]+)/$')
		self.assertEqual(build('/articles/:pk/comments'), '^articles/(?P<pk>[0-9]+)/comments/$')

	def test_custom_patten_pk(self):
		self.assertEqual(build('/:user_pk'), '^(?P<user_pk>[0-9]+)/$')
		self.assertEqual(build('/articles/:article_pk'), '^articles/(?P<article_pk>[0-9]+)/$')
		self.assertEqual(build('/articles/:article_pk/comments'), '^articles/(?P<article_pk>[0-9]+)/comments/$')

	def test_pattern_id(self):
		self.assertEqual(build('/:id'), '^(?P<id>[0-9]+)/$')
		self.assertEqual(build('/user/:id'), '^user/(?P<id>[0-9]+)/$')
		self.assertEqual(build('/user/:id/friends'), '^user/(?P<id>[0-9]+)/friends/$')

	def test_custom_pattern_id(self):
		self.assertEqual(build('/:user_id'), '^(?P<user_id>[0-9]+)/$')
		self.assertEqual(build('/user/:user_id'), '^user/(?P<user_id>[0-9]+)/$')
		self.assertEqual(build('/user/:user_id/friends'), '^user/(?P<user_id>[0-9]+)/friends/$')

	def test_pattern_slug(self):
		self.assertEqual(build('/:slug'), '^(?P<slug>[A-Za-z0-9_-]+)/$')
		self.assertEqual(build('/articles/:slug'), '^articles/(?P<slug>[A-Za-z0-9_-]+)/$')
		self.assertEqual(build('/post/:slug/comments'), '^post/(?P<slug>[A-Za-z0-9_-]+)/comments/$')

	def test_custom_pattern_slug(self):
		self.assertEqual(build('/:post_slug'), '^(?P<post_slug>[A-Za-z0-9_-]+)/$')
		self.assertEqual(build('/articles/:article_slug'), '^articles/(?P<article_slug>[A-Za-z0-9_-]+)/$')
		self.assertEqual(build('/post/:post_slug/comments'), '^post/(?P<post_slug>[A-Za-z0-9_-]+)/comments/$')

	def test_pattern_page(self):
		self.assertEqual(build('/:page'),'^(?P<page>\d+)/$')
		self.assertEqual(build('/articles/:page'),'^articles/(?P<page>\d+)/$')

	def test_custom_pattern_page(self):
		self.assertEqual(build('/:blog_page'),'^(?P<blog_page>\d+)/$')
		self.assertEqual(build('/articles/:article_page'),'^articles/(?P<article_page>\d+)/$')

	def test_combined_patterns_in_same_route(self):
		self.assertEqual(build('/articles/:slug/comments/:id'), '^articles/(?P<slug>[A-Za-z0-9_-]+)/comments/(?P<id>[0-9]+)/$')
		self.assertEqual(build('/articles/:article_id/comments/:comment_id'), '^articles/(?P<article_id>[0-9]+)/comments/(?P<comment_id>[0-9]+)/$')
		self.assertEqual(build('/user/:user_pk/status/:status_id'), '^user/(?P<user_pk>[0-9]+)/status/(?P<status_id>[0-9]+)/$')
		self.assertEqual(build('/item/:pk/color/:slug'), '^item/(?P<pk>[0-9]+)/color/(?P<slug>[A-Za-z0-9_-]+)/$')

	def test_pattern_day(self):
		pass

	def test_pattern_month(self):
		pass

	def test_pattern_year(self):
		pass

	def test_pattern_date(self):
		pass
