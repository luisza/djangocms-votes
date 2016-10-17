from setuptools import setup, find_packages
import os

CLASSIFIERS = [
    'Environment :: Web Environment',
	'Framework :: Django',
	'Framework :: Django :: 1.8',
	'Framework :: Django :: 1.9',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.5',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
	'Topic :: Software Development :: Libraries :: Python Modules',
	'Development Status :: 4 - Beta',
]

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))



setup(
    author='Luis Zarate',
    author_email='luis.zarate@solvosoft.com',
    name='djangocms-votes',
    version='0.0.6',
    description='Django cms comments, and rate system with stats.',
    long_description=README,
    url='https://github.com/luisza/djangocms-votes',
    license='GNU General Public License v3 (GPLv3)',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=[
		"django>=1.8",
		"django-cms>=3.3.2",
		"aldryn-newsblog==1.3.0",
		"django-ajax-selects==1.5.0",
		"djangoajax",
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False
)
