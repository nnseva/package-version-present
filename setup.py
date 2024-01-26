#!/usr/bin/python

"""
A setuptools based setup module.
"""

from setuptools import setup

from package_version_present import __version__ as version


setup(
    name='package-version-present',

    version=version,

    description='Check the package version present',
    long_description="""
Package Version Present

The utility checking presence of the package version. See https://github.com/nnseva/package-version-present
    """,

    url='https://github.com/nnseva/package-version-present',

    author='Vsevolod Novikov',
    author_email='nnseva@gmail.com',

    zip_safe=False,
    platforms="any",

    license='LGPL',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Utilities',

        'Environment :: Console',

        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='version pypi',
    py_modules=['package_version_present'],
    entry_points={
        'console_scripts': [
            'package-version-present=package_version_present:main',
        ],
    },
)
