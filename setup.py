#!/usr/bin/env python

from setuptools import setup

setup(name='RPiProcessRig',
      version='1.0',
      description='A simple industrial rig that can be used for experimentation with a variety of different control algortithms',
      author='Alexander Leech',
      author_email='alex.leech@talktalk.net',
      license = 'MIT',
      keywords = "Raspberry Pi Process Control Industrial Rig Hardware Experimentation",
      url='https://github.com/FlaminMad/RPiProcessRig',
      packages=['RPiProcessRig'],      
      package_dir={'RPiProcessRig' : 'RPiProcessRig/src'},
      package_data={'RPiProcessRig': ['../cfg/*.yaml']}
      )