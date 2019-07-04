"""
Setup file for led-controller
author: Luis Garcia Rodriguez 2017
Licence: GPLv3
"""
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='led-controller',
    version='3.0.0',
    description='A simple interface for controlling LEDs in circadian experiments',
    # The project's main homepage.
    url='https://github.com/polygonaltree/Led-control',

    # Author details
    author='Luis Garcia Rodriguez',
    author_email='luis.garcia@uni-muenster.de',
    license='GPLv3',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"]
    install_requires=['pyside2'],
    entry_points={
        'console_scripts': [
            'led-controller=gui:main',
        ],
    },
)
