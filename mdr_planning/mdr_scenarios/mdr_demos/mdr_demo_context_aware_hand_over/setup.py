#!/usr/bin/env python

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages=['mdr_demo_context_aware_hand_over'],
    package_dir={'mdr_demo_context_aware_hand_over': 'ros/src/mdr_demo_context_aware_hand_over'}
)

setup(**d)
