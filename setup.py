#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='tkit',
    version='0.1.0-beta',
    packages=['tkit', 'tkit.cli', 'tkit.gui', 'tkit.extras'],
    license='MIT',
    description="Double-click Python Script/Tool Toolkit",
    long_description=open('README.rst').read(),
    install_requires=[p for p in open("REQUIREMENTS.txt", 'r').readlines()],
    test_suit="tests",
    tests_require=["nose", "coverage"],
    platforms='Python 2.6.x',
    classifiers=[
            'Programming Language :: Python',
            'Development Status :: 2 - Pre-Alpha',
            'Natural Language :: English',
            'Environment :: Database',  #
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Operating System :: Windows',
            'Topic :: Scintific/Engineering'
            ],
)
