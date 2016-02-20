"""Setup script for Schnibble."""
from setuptools import setup

setup(
    name="schnibble",
    version="0.0",
    packages=["schnibble"],
    author="Zygmunt Krynicki",
    author_email="me@zygoon.pl",
    description="Toolkit for processing Python bytecode",
    test_suite='schnibble',
    license="GPLv3",
    url='https://github.com/zyga/schnibble',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Compilers',
    ],
)
