#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

## version = open('thunderdome_flask/VERSION', 'r').readline().strip()

setup(name='picamstreamer',
	version='0.1',
	description='A simple web app to stream Pi Camera',
	long_description=read('README.md'),
	url='https://github.com/nioto/PiCamStreamer',
	author='Antonio Alves,
	author_email='nioto.org@gmail.com',
	license='BSD',
	py_modules=['picamstreamer'],
	install_requires=[
		'Flask>=0.7',
		'picam>=1.1'
	],
	zip_safe=False,
	classifiers=[
		'Development Status :: 4 - Beta',
		'Environment :: Web Environment',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: BSD License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
		'Topic :: Software Development :: Libraries :: Python Modules'
	]
)
