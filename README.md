![DjUrl - Django urls](/djurlheader.png) [![Build Status](https://travis-ci.org/venturachrisdev/djurl.svg?branch=master)](https://travis-ci.org/venturachrisdev/djurl)
===
Define your django urls as simple as possible.

Why should I use DjUrl?
---
Django routing urls aren't easy to deal with, regular expressions can become a nightmare sometimes. Just imagine dealing with such routes in your `django app`:
```python
from django.conf.urls import url
from core import BlogView, SinglePostView, SearchResultsView, ArchiveView

urlpatterns = [
	# => /blog/
	url(r'^blog/$', BlogView.as_view(), name="blog"),
	# => /blog/5
	url(r'^blog/(?P<post_id>[0-9]+)/$', SinglePostView.as_view(), name="singlepost"),
	# => /blog/search/sometitle
	url(r'^blog/search/(?P<search_query>[A-Za-z0-9_-]+)/$', SearchResultsView.as_view(), name="search"),
	# => /blog/archive/2017/02/12
	url(r'^blog/archive/(?P<date>[0-9]{4}-(0?([1-9])|10|11|12)-((0|1|2)?([1-9])|[1-3]0|31))/$',
		ArchiveView.as_view(), name="archive")
]
```
That's too much work and you lost me in those regex. With **DjUrl** this comes easy, you just need to *express what you want*, **DjUrl will handle the regular expressions for you**:

```python
from djurl import url
from core import BlogView, SinglePostView, SearchResultsView, ArchiveView

urlpatterns = [
	url('/blog', BlogView, name="blog"),
	url('/blog/:id', SinglePostView, name="singlepost"),
	url('/blog/search/:query', SearchResultsView, name="search"),
	url('/blog/archive/:date', ArchiveView, name="archive")
]
```
No regex, just clean paths and param names. You can now pass the regex work to DjUrl and concentrate in the *bussiness logic*. It saves you a lot of time and code. *You don't need to worry about the routes anymore*. **Note you don't need to call `as_view` in your CBV's.** DjUrl does this for you as well.

Usage
---
Now you know what you should use `DjUrl`, It's time to learn how to use it. DjUrl has a list of known/default pattern that you can use in your routes, these are:

* `id`: A secuence of characters from 0 to 9. Ej: `1, 12, 454545, 8885500, 8`
* `pk`: A primary key, it's like `id` but needed for `Class Based Views`.
* `page`: falls in the same category, but you'd use `page` for a better param name.
* `slug`: A simple string (alphanumeric characters).
* `day`: A number between 0,01,..., 31.
* `month`: A number between 0, 01,...,12.
* `year`: A four digits number: `1998, 2017, 2018, 3015, 2020, 1406...`
* `date`: An expression with `year-month-day` format: `2017-06-23, 1998-10-20, 1492-10-12`

That means, wherever you put `/:id` you can use it in your view as param (named `id`).
```python
url('post/:pk/comment/:id', myview, name="post_comment")
```
Your view:
```python
def myview(request, pk, id):
	# Use `pk` (post's) and `id` (comment's)
```

But what if I have two or more id's, or two slugs? What if I wanted to use a custom name for my id's? - Ok, you can use custom names if you end it with `_` + the pattern type. - What?...
```python
url('post/:post_pk/comment/:comment_id', myview, ...)
# ...
def myview(request, post_pk, comment_id):
	# `post_pk` is parsed as a :pk and `comment_id` like an :id

```
Yeah, it sounds good!, but... What if I wanted to use my own patterns? - Easy, you can register many patterns as you want:
```python
from djurl import url, register_pattern
register_pattern('hash', '[a-f0-9]{9}')
# use it
url('/:hash', myview)
```

Install
---
If you want to have fun with this library and integrate it to your project, just type in your terminal:
```
$ pip install djurl
```
or, clone the repo and type:
```
$ python setup.py install
```
Enjoy it!

Contributions
---
If you've found a bug/error or just have questions, feel free to open an **issue**. And, **Pull requests** are welcome as well.

License
=======

    Copyright 2017 Christopher Ventura

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
