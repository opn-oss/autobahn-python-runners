# coding=utf-8
################################################################################
# MIT License
#
# Copyright (c) 2017 OpenDNA Ltd.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
################################################################################
from __future__ import unicode_literals, absolute_import

import os

from setuptools import setup, find_packages

prefix = os.path.dirname(__file__)

# read version string
with open(os.path.join(prefix, 'opendna', 'autobahn', 'runners', '_version.py')) as f:
    exec(f.read())  # defines __version__

# read package long description
with open(os.path.join(prefix, 'README.rst')) as f:
    long_description = f.read()

setup(
    name='autobahn-python-runners',
    description='A collection of component runners for Autobahn Python',
    long_description=long_description,
    version=__version__,
    packages=find_packages(),
    url='https://github.com/opn-oss/autobahn-python-runners',
    license='MIT',
    author='Adam Jorgensen',
    author_email='adam.jorgensen.za@gmail.com',
    install_requires=[
        'autobahn>=17.3.1',
        'opn-oss-py-common>=17.8.4'
    ],
    entry_points={
        'console_scripts': [
            'run_asyncio_component = opendna.autobahn.runners.run_asyncio:run',
            'run_asyncio_components = opendna.autobahn.runners.multirun_asyncio:run',
            'run_twisted_component = opendna.autobahn.runners.run_twisted:run'
        ]
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Framework :: Twisted",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: Implementation :: Jython",
        "Topic :: Utilities",
    ],
    keywords='autobahn crossbar twisted asyncio'
)
