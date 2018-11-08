import os
from setuptools import setup

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
    packages=['popcorn'],
    long_description=read('README.md'),
    classifiers=[],
)
