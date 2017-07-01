VERSION = (0, 1, 3)


def get_version():
    return ".".join(map(str, VERSION))


_default_patterns_ = {
    # Keys
    'pk': r'\d+',
    'id': r'\d+',
    'slug': r'[A-Za-z0-9_-]+',
    # Date
    'day': r'(([0-2])?([1-9])|[1-3]0|31)',
    'month': r'(0?[1-9]|10|11|12)',
    'year': r'\w{4}',
    'date': r'\w{4}-(0?([1-9])|10|11|12)-((0|1|2)?([1-9])|[1-3]0|31)',
    # filters
    'page': r'\d+',
    'filename': r'[\w,\s-]+\.[A-Za-z]{2,4}',
    'uuid': r'([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}){1}',
}


class Djurl():
    """
    Classname: Djurl
    Description: Django Url
    Author: Christopher Ventura Aguiar <venturachrisdev@gmail.com>
    Date: Jun 22, 2017
    Long description:
    """
    def __init__(self, pattern, exact=True, father=False):
        self.pattern = pattern
        self.father = father
        self.exact = exact
        if self.pattern.startswith('/'):
            self.pattern = self.pattern[1:]

    def normalize(self, path):
        stpath = path.lstrip("^\n")
        if len(stpath) > 1:
            stpath = stpath.lstrip("//")
        stpath = stpath.rstrip(" $\n")
        result = "^%s"
        if self.exact:
            result += "$"

        # Trim
        return result % stpath

    def trim(self, path):
        return path.replace(" ", "")

    def create_pattern(self, key, pattern):
        return "(?P<%s>%s)" % (key, pattern)

    # core
    def build(self):

        built = self.trim(self.pattern)
        if len(built) > 1:
            import re
            paramkeys = re.findall('(:([a-z_\d]+))', built)
            for matches, key in paramkeys:
                if key in _default_patterns_:
                    newpattern = self.create_pattern(key, _default_patterns_[key])
                    built = built.replace(":%s" % key, newpattern)
                else:
                    for x in _default_patterns_:
                        if key.endswith('_%s' % x):
                            newpattern = self.create_pattern(key, _default_patterns_[x])
                            built = built.replace(":%s" % key, newpattern)
            if not built.endswith('/') and not built.endswith('$'):
                if self.exact or (not self.exact and self.father):
                    built += '/'

        result = self.normalize(built)
        return result

    @property
    def built(self):
        if not hasattr(self, '_built'):
            setattr(self, '_built', self.build())

        return getattr(self, '_built')

    def __str__(self):
        return self.built

    # compatibily with python 2
    def __unicode__(self):
        return self.__str__()


def register_pattern(key, pattern):
    _default_patterns_[key] = pattern


def url(pattern, view, kwargs=None, name=None):
    exact = True
    father = False
    v = view

    # Class Based Views
    if isinstance(view, type):
        if hasattr(view, 'as_view'):
            v = view.as_view()

    # include
    if isinstance(v, tuple):
        exact = False
        father = True

    from django.conf.urls import url as BaseUrl
    return BaseUrl(Djurl(pattern, exact=exact, father=father), v, kwargs=kwargs, name=name)
