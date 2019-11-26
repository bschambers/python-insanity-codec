from setuptools import setup, find_packages

setup(name='insanity_codec',
      version='0.1',
      url='https://github.com/bschambers/python_insanity_codec',
      license='GPL',
      author='B. S. Chambers',
      author_email='ben@bschambers.info',
      description='Encoder/decoder for Insanity Code style text substitution ciphers',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.org').read(),
      zip_safe=False)
