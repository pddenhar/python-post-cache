#!/usr/bin/python
from setuptools import setup

setup(
  name = "postcache",
  version = "0.1.3",
  description = """A Python library to cache data that is being 
POSTed to a remote server in the JSON format (such as periodic log items 
or measurements.""",
  packages = ["postcache"],
  author='Peter Den Hartog',
  author_email='pddenhar@gmail.com',
  install_requires=["requests>=2.4.3"],
  url='https://github.com/pddenhar/python-post-cache')
