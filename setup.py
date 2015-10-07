#!/usr/bin/python
from setuptools import setup

setup(
  name = "post-cache",
  version = "0.1.0",
  description = """A Python library to cache data that is being 
  POSTed to a remote server in the JSON format (such as periodic log items 
    or measurements.""",
  packages = ["post-cache"],
  author='Peter Den Hartog',
  author_email='pddenhar@gmail.com',
  install_requires=[],
  url='https://github.com/pddenhar/python-post-cache')
