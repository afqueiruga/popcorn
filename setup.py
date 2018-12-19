import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "popcorn",
    version = "1.0",
    author = "Alejandro Francisco Queiruga",
    description = "",
    license = "GPL",
    keywords = "",
    test_suite="test",
    # packages=['popcorn'],
    packages=find_packages(exclude=['test']),
    long_description=read('README.md'),
    classifiers=[],
    install_requires=[
        'oset',
        'sympy'
    ]
)
