#Test

import sys

if sys.version_info >= (2,7):
	import unittest
else:
	from django.utils import unittest

if sys.version_info >= (3,4):
	from re import fullmatch
else:
	import re
	"""
	Emulate python-3.4 re.fullmatch().

	https://stackoverflow.com/questions/30212413/backport-python-3-4s-regular-expression-fullmatch-to-python-2
	"""
	def fullmatch(pattern, string):
		return re.match("(?:%s)\Z" % pattern, string)

from djurl import register_pattern, Djurl

def build(pattern, exact=True):
		return Djurl(pattern, exact=exact).build()

def evaluate(pattern, path, exact=True):
	# Return True if the path matches with the given pattern, False otherwise
	p = build(pattern, exact=exact)
	if exact and len(path) > 1:
		path = path + '/'

	return fullmatch(p, path)

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
		self.assertEqual(build('/:pk'), '^(?P<pk>\d+)/$')
		self.assertEqual(build('/articles/:pk'), '^articles/(?P<pk>\d+)/$')
		self.assertEqual(build('/articles/:pk/comments'), '^articles/(?P<pk>\d+)/comments/$')

	def test_custom_patten_pk(self):
		self.assertEqual(build('/:user_pk'), '^(?P<user_pk>\d+)/$')
		self.assertEqual(build('/articles/:article_pk'), '^articles/(?P<article_pk>\d+)/$')
		self.assertEqual(build('/articles/:article_pk/comments'), '^articles/(?P<article_pk>\d+)/comments/$')

	def test_pattern_id(self):
		self.assertEqual(build('/:id'), '^(?P<id>\d+)/$')
		self.assertEqual(build('/user/:id'), '^user/(?P<id>\d+)/$')
		self.assertEqual(build('/user/:id/friends'), '^user/(?P<id>\d+)/friends/$')

	def test_custom_pattern_id(self):
		self.assertEqual(build('/:user_id'), '^(?P<user_id>\d+)/$')
		self.assertEqual(build('/user/:user_id'), '^user/(?P<user_id>\d+)/$')
		self.assertEqual(build('/user/:user_id/friends'), '^user/(?P<user_id>\d+)/friends/$')

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
		self.assertEqual(build('/articles/:slug/comments/:id'), '^articles/(?P<slug>[A-Za-z0-9_-]+)/comments/(?P<id>\d+)/$')
		self.assertEqual(build('/articles/:article_id/comments/:comment_id'), '^articles/(?P<article_id>\d+)/comments/(?P<comment_id>\d+)/$')
		self.assertEqual(build('/user/:user_pk/status/:status_id'), '^user/(?P<user_pk>\d+)/status/(?P<status_id>\d+)/$')
		self.assertEqual(build('/item/:pk/color/:slug'), '^item/(?P<pk>\d+)/color/(?P<slug>[A-Za-z0-9_-]+)/$')

	def test_pattern_day(self):
		self.assertEqual(build('/day/:day'), '^day/(?P<day>(([0-2])?([1-9])|[1-3]0|31))/$')
		self.assertEqual(build('/report/:id/day/:day'), '^report/(?P<id>\d+)/day/(?P<day>(([0-2])?([1-9])|[1-3]0|31))/$')

	def test_pattern_month(self):
		self.assertEqual(build('/month/:month'), '^month/(?P<month>(0?[1-9]|10|11|12))/$')
		self.assertEqual(build('/report/:id/month/:month/day/:day'), '^report/(?P<id>\d+)/month/(?P<month>(0?[1-9]|10|11|12))/day/(?P<day>(([0-2])?([1-9])|[1-3]0|31))/$')

	def test_pattern_year(self):
		self.assertEqual(build('/archive/year/:year'), '^archive/year/(?P<year>\w{4})/$')
		self.assertEqual(build('/report/:id/date/:year/:month/:day'), '^report/(?P<id>\d+)/date/(?P<year>\w{4})/(?P<month>(0?[1-9]|10|11|12))/(?P<day>(([0-2])?([1-9])|[1-3]0|31))/$')

	def test_pattern_date(self):
		self.assertEqual(build('/archive/date/:date'), '^archive/date/(?P<date>\w{4}-(0?([1-9])|10|11|12)-((0|1|2)?([1-9])|[1-3]0|31))/$')

	"""
	Evaluation Tests
	"""

	def test_evaluate_basic(self):
		self.assertTrue(evaluate('/', ''))
		self.assertTrue(evaluate('/hello', 'hello'))
		self.assertTrue(evaluate('/home/', 'home'))
		self.assertTrue(evaluate('/article/:article', 'article/:article'))
		self.assertTrue(evaluate('  /users/  ', 'users'))

		self.assertFalse(evaluate('/blog','blogggg'))
		self.assertFalse(evaluate('/article/:article', 'article/3'))
		self.assertFalse(evaluate('/blog/:blog', 'blog/hello-world'))

	def test_evaluate_pk(self):
		self.assertTrue(evaluate('/:pk', '10'))
		self.assertTrue(evaluate('/post/:pk', 'post/4'))
		self.assertTrue(evaluate('/post/:pk', 'post/2345454'))

		self.assertFalse(evaluate('/post/:pk', 'post/hello-universe'))

	def test_evaluate_id(self):
		self.assertTrue(evaluate('/:id', '19090'))
		self.assertTrue(evaluate('/user/:id', 'user/3'))
		self.assertTrue(evaluate('/user/:id', 'user/53723'))

		self.assertFalse(evaluate('/user/:id', 'user/2017-10-20'))
		self.assertFalse(evaluate('/user/:id', 'post/96jhn869y6j'))

	def test_evaluate_slug(self):
		self.assertTrue(evaluate('/:slug', 'hello-world_3'))
		self.assertTrue(evaluate('/article/:slug', 'article/sherlock-holmes-season-2-episode-3-review'))
		self.assertTrue(evaluate('/article/:slug', 'article/58jtgj689hy'))

		self.assertFalse(evaluate('/item/:slug', 'item/2%20p40501rg%207#ktgi-10-20'))

	def test_evaluate_page(self):
		self.assertTrue(evaluate('/:page', '10'))
		self.assertTrue(evaluate('/magazine/page/:page', 'magazine/page/4'))
		self.assertTrue(evaluate('/magazine/page/:page', 'magazine/page/23'))

		self.assertFalse(evaluate('/magazine/:page', 'magazine/under-the-red_hood'))

	def test_evaluate_date(self):
		self.assertTrue(evaluate('/day/:day', 'day/02'))
		self.assertTrue(evaluate('/day/:day', 'day/2'))
		self.assertTrue(evaluate('/day/:day', 'day/31'))

		self.assertFalse(evaluate('/day/:day', 'day/32'))

		self.assertTrue(evaluate('/month/:month', 'month/01'))
		self.assertTrue(evaluate('/month/:month', 'month/2'))
		self.assertTrue(evaluate('/month/:month', 'month/12'))

		self.assertFalse(evaluate('/month/:month', 'month/13'))


		self.assertTrue(evaluate('/year/:year', 'year/1492'))
		self.assertTrue(evaluate('/year/:year', 'year/2016'))
		self.assertTrue(evaluate('/year/:year', 'year/4096'))

		self.assertFalse(evaluate('/year/:year', 'year/56000'))

		self.assertTrue(evaluate('/date/:day/:month/:year', 'date/31/10/2017'))
		self.assertTrue(evaluate('/date/:day/:month/:year', 'date/09/1/2017'))
		self.assertTrue(evaluate('/date/:day/:month/:year', 'date/3/01/2017'))
		self.assertTrue(evaluate('/date/:day/:month/:year', 'date/11/11/2011'))

		self.assertFalse(evaluate('/date/:day/:month/:year', 'date/32/10/2017'))
		self.assertFalse(evaluate('/date/:day/:month/:year', 'date/3/15/2017'))
		self.assertFalse(evaluate('/date/:day/:month/:year', 'date/11/11/20114'))


		self.assertTrue(evaluate('/date/:date', 'date/2017-10-31'))
		self.assertTrue(evaluate('/date/:date', 'date/2017-09-1'))
		self.assertTrue(evaluate('/date/:date', 'date/2017-01-3'))
		self.assertTrue(evaluate('/date/:date', 'date/2011-11-11'))


		self.assertFalse(evaluate('/date/:date', 'date/2011-11/11'))
		self.assertFalse(evaluate('/date/:date', 'date/2011_11_11'))
		self.assertFalse(evaluate('/date/:date', 'date/2011/11-11'))
		self.assertFalse(evaluate('/date/:date', 'date/2017-10-32'))
		self.assertFalse(evaluate('/date/:date', 'date/2017-15-3'))
		self.assertFalse(evaluate('/date/:date', 'date/20114-11-11'))

