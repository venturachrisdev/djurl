from setuptools import setup, find_packages

def read(filename):
	import os
	return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
	name="djurl",
	version=__import__('djurl').get_version(),
	author="Christopher Ventura",
	author_email="venturachrisdev@gmail.com",
	description="Url prettyfier for django",
	url="https://github.com/venturachrisdev/djurl",
	license="MIT",
	keywords="django url urlparse web python regex",
	packages= find_packages(exclude=['tests']),
	include_packages_data=True,
	test_suite="tests",
	long_description= read('README.md'),
	install_requires=['django'],
	classifiers=[
		'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Pre-processors'
	]
)

print(read('README.md'))