#!/usr/bin/env python3

from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ogn-control',
    version='0.0.1',
    description='A python module to control a Open Glider Network (OGN) receiver',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Meisterschueler/ogn-control',
    author='Konstantin Gründger aka Meisterschueler',
    author_email='kammermark@gmx.de',
    license='AGPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: GIS',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    keywords=['gliding', 'ogn'],
    packages=['ogn.{}'.format(package) for package in find_packages(where='ogn')],
    python_requires='>=3',
    install_requires=[
        'Flask==1.1.2',
        'Flask-SocketIO==4.3.1',
        'dnspython==1.16.0,<2.0',       # on rpi eventlet depends on dnspython which requires python 3.6
        'eventlet==0.25.2',
        'Flask-Bootstrap==3.3.7.1',
        'ogn-client==1.0.1'
        ],
    extras_require={
        'dev': [
            'nose==1.3.7',
            'coveralls==2.1.1',
            'flake8==5.0.4'
        ]
    },
    zip_safe=False
)
