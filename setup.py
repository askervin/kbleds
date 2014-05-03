#!/usr/bin/env python

from distutils.core import setup

setup(name         = 'kbleds',
      version      = '0.1',
      description  = 'Keyboard LED control library and executable',
      author       = 'Antti Kervinen',
      author_email = 'antti.kervinen@gmail.com',
      scripts      = ['kbleds'],
      py_modules   = ['kbleds'],
      classifiers  = [
          'Development Status :: 4 - Beta',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 2 :: Only',
          'Programming Language :: Unix Shell'
          ]
)
