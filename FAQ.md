FAQ
====

* **How do I replace django urls with DjUrl in my current project?**

Easy, just change the Django default `url()` method:
```python
from django.conf.urls import url
```
with DjUrl's `url()`:
```python
from djurl import url
```
Then, be sure to replace all the regular expression with Djurl's syntax and if you're using `Class Based Views`, feel free to remove the `as_view()` call.

* **If there's a new version of Djurl, how do I reinstall it?**

You can reinstall Djurl via pip typing:
```
$ python -m pip install djurl -U --force-reinstall --no-cache-dir
```
