#!/usr/bin/env python3
from distutils.core import setup

from uri import name, version


setup(
    name=name,
    version=version,
    description='a web service for creating alternative uris that only last for a short period of time',
    license='MIT',
    author='Foster McLane',
    author_email='fkmclane@gmail.com',
    packages=['uri'],
    package_data={'uri': ['html/*.*']},
)
