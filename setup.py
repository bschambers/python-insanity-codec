# Copyright 2019-present B. S. Chambers --- Distributed under GPL, version 3

from setuptools import setup, find_packages

setup(name='insanitycodec',
      version='0.1',
      url='https://github.com/bschambers/python_insanitycodec',
      license='GPL, version 3',
      author='B. S. Chambers',
      author_email='ben@bschambers.info',
      description='Encoder/decoder for Insanity Code style text substitution ciphers',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.org').read(),
      zip_safe=False)
