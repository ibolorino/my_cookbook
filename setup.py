import os

from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='My Cookbook',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='Livro de receitas',
    long_description=README,
    author='Ivan Bolorino',
    author_email='ivan.bolorino@gmail.com',
    install_requires=[],
)
